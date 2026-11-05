from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, P2wshAddress, P2trAddress
from bitcoinutils.script import Script
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
import requests

setup('testnet4')

alice_priv = PrivateKey()
bob_priv = PrivateKey()

alice_pub = alice_priv.get_public_key().to_hex()
bob_pub = bob_priv.get_public_key().to_hex()

print(f"Публичный ключ Алисы: {alice_pub}")
print(f"Публичный ключ Боба: {bob_pub}")

multisig_script = Script([2, alice_pub, bob_pub, 2, 'OP_CHECKMULTISIG'])

p2wsh_addr = P2wshAddress.from_script(multisig_script)
multisig_address = p2wsh_addr.to_string()
print(f"\n✅ Ваш 2-из-2 мультисиг-адрес (P2WSH): {multisig_address}")

print("\n" + "="*60)
print("ШАГ 1: Пополните этот адрес через кран (faucet).")
print("Скопируйте адрес выше и запросите тестовые монеты (например, 50000 сатоши).")
print("Ссылка на кран: https://mempool.space/testnet4/faucet")
print("="*60)

input("Нажмите Enter после того, как монеты появятся на адресе (подождите 1-2 минуты)...")

print("\nИщем UTXO на мультисиг-адресе...")
utxo_url = f"https://mempool.space/testnet4/api/address/{multisig_address}/utxo"
response = requests.get(utxo_url)

if response.status_code != 200:
    print(f"❌ Ошибка при запросе UTXO: {response.text}")
    exit()

utxos = response.json()
if not utxos:
    print("❌ На адресе нет монет. Убедитесь, что вы пополнили его, и подождите пару минут.")
    exit()

utxo = utxos[0]
utxo_txid = utxo['txid']
utxo_vout = utxo['vout']
utxo_value = utxo['value']
print(f"Найден UTXO: TXID: {utxo_txid}, VOUT: {utxo_vout}, Сумма: {utxo_value} сатоши")

recipient_address = 'tb1pumwese3hl8lq42xk9g8ka6k5mgj6l999d9pap5syqfhrnw5l246q6l9yfu'
fee = 1000
amount_to_send = utxo_value - fee

if amount_to_send <= 0:
    print("❌ Недостаточно средств для покрытия комиссии.")
    exit()

txin = TxInput(utxo_txid, utxo_vout)

recipient_address = (
    'tb1pumwese3hl8lq42xk9g8ka6k5mgj6l999d9pap5syqfhrnw5l246q6l9yfu'
)

txout = TxOutput(
    amount_to_send,
    P2trAddress(recipient_address).to_script_pub_key()
)
tx = Transaction([txin], [txout], has_segwit=True)

print("\nПодписываем транзакцию двумя ключами...")

signature_alice = alice_priv.sign_segwit_input(tx, 0, multisig_script, utxo_value)
signature_bob = bob_priv.sign_segwit_input(tx, 0, multisig_script, utxo_value)

witness = TxWitnessInput(['', signature_alice, signature_bob, multisig_script.to_hex()])
tx.witnesses.append(witness)

tx_hex = tx.serialize()
print(f"\nГотовая транзакция (hex):\n{tx_hex}")

print("\nОтправка транзакции в сеть...")
url = 'https://mempool.space/testnet4/api/tx'
headers = {'Content-Type': 'text/plain'}
try:
    response = requests.post(url, data=tx_hex, headers=headers)
    response.raise_for_status()
    txid = response.text
    print(f"✅ Транзакция успешно отправлена!")
    print(f"TXID: {txid}")
    print(f"Ссылка для проверки: https://mempool.space/testnet4/tx/{txid}")
except requests.exceptions.RequestException as e:
    print(f"❌ Ошибка при отправке: {e}")
    if response.text:
        print(f"Ответ сервера: {response.text}")