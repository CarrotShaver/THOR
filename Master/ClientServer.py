import requests
from Crypto.PublicKey import RSA
import random, string
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from sys import argv

class ClientServer():
    # Variables
    data={ "to": 0, "from": 0, "message": "" }
    nodeList = [ 12300 ] # Change whenever new nodes are added
    nodePath = []
    keyList = []
    message = ""

    def build_path(self, nodeList, nodePath ):
        # while ( len(nodeList) > 0 and len(nodePath) < 3 ):
        #     print(len(nodeList))
        #     randomNode = random.randint(0, len(nodeList)-1)
        #     nodePath.append(nodeList[randomNode])
        #     nodeList.pop(randomNode)
        if len(nodeList) >= 3:
            nodePath = random.sample(nodeList, 3)
        else: 
            nodePath = random.sample(nodeList, len(nodeList))
        return nodePath

    def get_keys(self, nodePath):
        for node in client.nodePath:
            print(node)
            message = requests.post(
            ("http://127.0.0.1:%s" %(node)), 
            data={
                "to": 0,
                "from": 0,
                "message": "keyrequest"
                }
            )
            # print(message.status_code, message.reason)
            print(message.status_code, message.reason)
            print(message.text)
            filename = ("%s_receiver.pem" %node)
            receiver = open(filename, "w")
            receiver.write(message.text)
            receiver.close()



if __name__=="__main__":
    client = ClientServer()
    # Messaging service
    while(True):
        # message input
        message = input("Message: ")
        print("Message saved...")
        # Build path
        print("Building Path...")
        client.nodePath = client.build_path( client.nodeList, client.nodePath )
        print("Path:", client.nodePath)
        # Get keys
        print("Requesting Keys...")
        client.get_keys( client.nodePath )
        # Build and encrypt layers
        # Send
        # print(message.status_code, message.reason)