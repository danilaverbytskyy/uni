import json
import requests

RPC_URL = "http://127.0.0.1:18443/wallet/labwallet"
RPC_USER = "student"
RPC_PASS = "labpassword123"


def rpc_call(method, params=None):
    headers = {"content-type": "application/json"}
    payload = {
        "jsonrpc": "1.0",
        "id": "lab3_task3",
        "method": method,
        "params": params or [],
    }
    response = requests.post(
        RPC_URL,
        headers=headers,
        data=json.dumps(payload),
        auth=(RPC_USER, RPC_PASS),
    )
    res_json = response.json()
    if res_json.get("error"):
        raise Exception(f"RPC Error in {method}: {res_json['error']}")
    return res_json["result"]


def main():
    utxos = rpc_call("listunspent")
    if not utxos:
        print("No UTXOs available to spend!")
        return

    selected_utxo = utxos[0]
    txid_in = selected_utxo["txid"]
    vout_in = selected_utxo["vout"]
    input_amount = selected_utxo["amount"]
    print(
        f"[DEBUG] Selected Input UTXO: {txid_in} (vout: {vout_in}), Amount: {input_amount} BTC"
    )

    recipient_address = rpc_call("getnewaddress")
    change_address = rpc_call("getnewaddress")
    print(f"[DEBUG] Recipient Address: {recipient_address}")
    print(f"[DEBUG] Change Address:    {change_address}")

    send_amount = 10.0
    fee = 0.0001
    change_amount = round(input_amount - send_amount - fee, 8)

    inputs = [{"txid": txid_in, "vout": vout_in}]
    outputs = {recipient_address: send_amount, change_address: change_amount}

    raw_tx = rpc_call("createrawtransaction", [inputs, outputs])
    print(f"\n1. Created Raw Transaction (HEX):\n{raw_tx}\n")

    signed_tx_obj = rpc_call("signrawtransactionwithwallet", [raw_tx])
    signed_hex = signed_tx_obj["hex"]
    print(
        f"2. Signed Transaction (Complete: {signed_tx_obj['complete']}):\n{signed_hex}\n"
    )

    broadcasted_txid = rpc_call("sendrawtransaction", [signed_hex])
    print("=" * 60)
    print(f"3. SUCCESS! Transaction Broadcasted. TXID:\n{broadcasted_txid}")
    print("=" * 60)


if __name__ == "__main__":
    main()
