import urllib.request
import urllib.error
import json


def get_bitcoin_balance(address):
    network_path = "api"
    if address.startswith(("m", "n", "2", "tb1")):
        network_path = "testnet4/api"
        print("[Info] Обнаружен адрес тестовой сети. Используем API Testnet4.")

    url = f"https://mempool.space/{network_path}/address/{address}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            raw_data = response.read().decode("utf-8")
            data = json.loads(raw_data)

            print("=== RAW JSON RESPONSE ===")
            print(json.dumps(data, indent=4))
            print("=========================\n")

            chain_stats = data.get("chain_stats", {})
            mempool_stats = data.get("mempool_stats", {})

            confirmed_balance_sats = chain_stats.get(
                "funded_txo_sum", 0
            ) - chain_stats.get("spent_txo_sum", 0)
            unconfirmed_balance_sats = mempool_stats.get(
                "funded_txo_sum", 0
            ) - mempool_stats.get("spent_txo_sum", 0)

            print("=== SUMMARY ===")
            print(f"Address: {address}")
            print(f"Confirmed Balance: {confirmed_balance_sats / 100_000_000} BTC")
            print(f"Unconfirmed Balance: {unconfirmed_balance_sats / 100_000_000} BTC")
            print("===============")

    except urllib.error.URLError as e:
        print(f"Failed to fetch data. Error: {e}")


if __name__ == "__main__":
    print("--- Программа для получения баланса Bitcoin ---")

    target_address = input(
        "Введите Bitcoin адрес (например, tb1... или 1A1...): "
    ).strip()

    if not target_address:
        print("Ошибка: Адрес не может быть пустым.")
    else:
        print(f"\nЗапрашиваем данные для адреса: {target_address}...\n")
        get_bitcoin_balance(target_address)
