import json
import requests

RPC_URL = "http://127.0.0.1:18443/wallet/labwallet"
RPC_USER = "student"
RPC_PASS = "labpassword123"

MY_ADDRESS = "bcrt1q8zpt9h0egxn6t8pt0d75y6njw78q037dxa3hxe"


def rpc_call(method, params=None):
    headers = {"content-type": "application/json"}
    payload = {
        "jsonrpc": "1.0",
        "id": "lab3_task2",
        "method": method,
        "params": params or [],
    }
    response = requests.post(
        RPC_URL,
        headers=headers,
        data=json.dumps(payload),
        auth=(RPC_USER, RPC_PASS),
    )
    return response.json()


def main():
    print(f"Checking UTXOs for address: {MY_ADDRESS}\n")

    response = rpc_call("listunspent", [1, 9999999, [MY_ADDRESS]])

    if response.get("error"):
        print("RPC Error:", response["error"])
        return

    utxos = response["result"]

    print(f"Found {len(utxos)} unspent transaction outputs (UTXOs):")

    total_sum = 0.0
    for i, utxo in enumerate(utxos, 1):
        amount = utxo["amount"]
        txid = utxo["txid"]
        vout = utxo["vout"]
        total_sum += amount
        print(f"  {i}. TXID: {txid} | vout: {vout} | Amount: {amount} BTC")

    print("-" * 60)
    print(f"Total Unspent Balance for address: {total_sum:.8f} BTC")


if __name__ == "__main__":
    main()
