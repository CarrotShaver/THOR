import requests

if __name__=="__main__":
    from sys import argv

    if len(argv) == 3:
        ip = str(argv[1])
        port = str(argv[2])

    while(True):
        messageInput = input("message: ")
        message = requests.post(
            ("http://%s:%s" %(ip, port)), 
            data={
                "to": 0,
                "from": 0,
                "message": messageInput
                }
            )
        print(message.status_code, message.reason)
        