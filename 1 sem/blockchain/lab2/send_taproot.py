from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, P2trAddress
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
import requests


private_key_hex = '224be73fef4754689af3aea105b1af91e281e041df86181d3e6133a3a0362d70'
recipient_address = 'tb1pfs0qzsemqfsuu579m005z503amyrj9k3evq4aes4hcetwjq6gshs5yqgau'
FEE = 1000
setup('testnet4')

priv = PrivateKey(secret_exponent=int(private_key_hex, 16))
my_address = priv.get_public_key().get_taproot_address()
my_address_str = my_address.to_string()
print(f"Ваш Taproot адрес (отправитель): {my_address_str}")

print("Ищем UTXO в сети...")
utxo_url = f"https://mempool.space/testnet4/api/address/{my_address_str}/utxo"
response = requests.get(utxo_url)

if response.status_code != 200:
    print(f"❌ Ошибка при запросе UTXO: {response.text}")
    exit()

utxos = response.json()
if not utxos:
    print("❌ На этом адресе нет непотраченных монет (UTXO). Подождите подтверждения или получите монеты снова.")
    exit()

utxo = utxos[0]
utxo_txid = utxo['txid']
utxo_vout = utxo['vout']
utxo_value = utxo['value']

print(f"Найден UTXO: TXID: {utxo_txid}, VOUT: {utxo_vout}, Сумма: {utxo_value} сатоши")

amount_to_send = utxo_value - FEE

if amount_to_send <= 0:
    print("❌ Недостаточно средств для покрытия комиссии.")
    exit()

txin = TxInput(utxo_txid, utxo_vout)
txout = TxOutput(amount_to_send, P2trAddress(recipient_address).to_script_pub_key())

tx = Transaction([txin], [txout], has_segwit=True)

my_script_pub_key = my_address.to_script_pub_key()
signature = priv.sign_taproot_input(
    tx,
    0, # индекс входа
    [my_script_pub_key],
    [utxo_value]
)

tx.witnesses.append(TxWitnessInput([signature]))

tx_hex = tx.serialize()
print(f"\nГотовая транзакция (hex):\n{tx_hex}")

print("\nОтправка транзакции в сеть...")
url = 'https://mempool.space/testnet4/api/tx'
headers = {'Content-Type': 'text/plain'}
try:
    response = requests.post(url, data=tx_hex, headers=headers)
    response.raise_for_status()
    txid = response.text
    print(f"Транзакция успешно отправлена!")
    print(f"TXID: {txid}")
    print(f"Ссылка для проверки: https://mempool.space/testnet4/tx/{txid}")
except requests.exceptions.RequestException as e:
    print(f"Ошибка при отправке: {e}")
    if response.text:
        print(f"Ответ сервера: {response.text}")