from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    content = request.get_json(silent=True)

    try:
        if content['payload']['platform'] == 'Ethereum':
            eth_sk = content['sig']
            eth_pk = content['payload']['pk']

            payload = json.dumps(content['payload'])
            eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
            eth_sig_obj = eth_account.Account.recover_message(eth_encoded_msg, eth_pk)

            # Check if signature is valid
            if eth_sig_obj.signature.hex() == eth_sk:
                result = True
            else:
                result = False

            return jsonify(result)

        if content['payload']['platform'] == 'Algorand':
            payload = json.dumps(content['payload'])

            algo_sk = content['sig']
            algo_pk = content['payload']['pk']
            algo_sig_str = algosdk.util.sign_bytes(payload.encode('utf-8'), algo_sk)

            result = algosdk.util.verify_bytes(payload.encode('utf-8'), algo_sig_str, algo_pk)
            return jsonify(result)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(e)


if __name__ == '__main__':
    app.run(port='5002')
