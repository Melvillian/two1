import os
import requests
import json

DEFAULT_WALLET_PATH = os.path.join(os.path.expanduser('~'),
                                   ".two1",
                                   "wallet",
                                   "multisig_wallet.json")

# ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

ACCESS_TOKEN = 'f3b510d6c8902b0af05b453b32be980f85579ea1b015dbfa81deaeb64ec74cec'

class multisig_wallet(object):

    @staticmethod
    def create_wallet(username, passphrase):
        ## Create a new wallet using BitGo Express 
        payload = json.dumps({ "passphrase": passphrase, "label": username })
        r = requests.post('http://localhost:3080/api/v1/wallets/simplecreate',
                          headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'},
                          data = payload)
        ## Setup wallet parameters
        walletId = r.json()['wallet']['id']
        user = r.json()['wallet']['label']
        keychain = r.json()['wallet']['private']        
        newWallet = json.dumps({user: { "walletId": walletId, "keychain": keychain }})

        ## Save new wallet to bitgo_wallet.json
        with open(DEFAULT_WALLET_PATH, 'r') as read_file:
            data = json.load(read_file)
            user = newWallet
            data.append(user)
        print(data)
        with open(DEFAULT_WALLET_PATH, 'w') as write_file:
            json.dump(data, write_file)
            
    @staticmethod        
    def send_bitcoin(sender, address, amount, passphrase):
        print('Sending Bitcoin')
        with open(DEFAULT_WALLET_PATH, 'r') as wallet:
          data = json.loads(wallet.read())
        for user in data:
          try:
            if user[sender]:
              print('Wallet found')
              walletId = user[sender]['walletId']
          except:
            print('Loading wallet..')
        print('Amount is: ' + amount)
        payload = json.dumps({"address": address, "amount": int(amount), "walletPassphrase": passphrase})
        #use the sender username to look up the sender id
        r = requests.post('http://localhost:3080/api/v1/wallet/' + walletId + '/sendcoins',
                        headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'},
                        data = payload)
        print(r.json())

    @staticmethod
    def generate_address(username):
        # use username to look up wallet Id
        with open(DEFAULT_WALLET_PATH, 'r') as wallet:
          data = json.loads(wallet.read())
        for user in data:
          try:
            if user[username]:
              print('Wallet found')
              walletId = user[username]['walletId']
          except:
            print('Loading wallet..')        
        r = requests.post('http://localhost:3080/api/v1/wallet/' + walletId + '/address/0',
                        headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'})                          
        print(r.json()['address'])

    @staticmethod        
    def ping():
        r = requests.post('http://localhost:3080/api/v1/ping', headers = {'Authorization': 'Bearer ' + access_token})
        print(r.json())
