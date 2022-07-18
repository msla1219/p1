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
        '''
        if content['payload']['platform'] == 'Ethereum':
            eth_sk = content['sig']
            eth_pk = content['payload']['pk']

            payload = json.dumps(content['payload'])
            eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
            eth_sig_obj = eth_account.Account.recover_message(eth_encoded_msg, eth_sk)

            print("payload:", payload)
            print("eth_encoded_msg:", eth_encoded_msg)
            print("eth_sig_obj:", eth_sig_obj)

            # Check if signature is valid
            if payload.strip() == eth_sig_obj:
                result = True
            else:
                result = False

            return jsonify(result)
        '''
        if content['payload']['platform'] == 'Algorand':
            algo_sig = content['sig']
            algo_pk = content['payload']['pk']
            payload = json.dumps(content['payload'])

            result = algosdk.util.verify_bytes(payload.encode('utf-8'), algo_sig, algo_pk)
            return jsonify(result)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(e)


if __name__ == '__main__':
    app.run(port='5002')
