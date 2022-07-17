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

    # test object
    json_object = {'sig': '0x3718eb506f445ecd1d6921532c30af84e89f2faefb17fc8117b75c4570134b4967a0ae85772a8d7e73217a32306016845625927835818d395f0f65d25716356c1c',
        'payload': {'message': 'Ethereum test message',
        'pk': '0x9d012d5a7168851Dc995cAC0dd810f201E1Ca8AF',
        'platform': 'Algorand'}}

    json_object = content

    if json_object['payload']['platform'] == 'Ethereum':
        eth_account.Account.enable_unaudited_hdwallet_features()
        acct, mnemonic = eth_account.Account.create_with_mnemonic()

        eth_pk = acct.address
        eth_sk = acct.key

        payload = json.dumps(json_object['payload'])
        eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
        eth_sig_obj = eth_account.Account.sign_message(eth_encoded_msg, eth_sk)

        # Check if signature is valid
        result = eth_account.Account.recover_message(eth_encoded_msg, signature=eth_sig_obj.signature.hex()) == eth_pk
        return jsonify(result)

    if json_object['payload']['platform'] == 'Algorand':
        eth_account.Account.enable_unaudited_hdwallet_features()
        acct, mnemonic = eth_account.Account.create_with_mnemonic()

        eth_pk = acct.address
        eth_sk = acct.key

        payload = json.dumps(json_object['payload'])

        eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
        eth_sig_obj = eth_account.Account.sign_message(eth_encoded_msg, eth_sk)

        result = eth_account.Account.recover_message(eth_encoded_msg, signature=eth_sig_obj.signature.hex()) == eth_pk
        return jsonify(result)


if __name__ == '__main__':
    app.run(port='5002')

