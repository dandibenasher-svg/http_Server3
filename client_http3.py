import socket

my_sock = socket.socket()
try:
    my_sock.connect(("127.0.0.1",80))
except Exception as e:
    print("error didnt connect to server" + str(e))
    my_sock.close()


while True:
    inp_user = input("for secret message insert 1\nto send photo insert 2")
    if inp_user =="1":
        inp_msg = input("please insert the secret message")
        msg = f"POST /http_work?secret HTTP/1.1\r\nContent-length: {len(inp_msg)}\r\n\r\n{inp_msg}"
        try:
            my_sock.send(msg.encode())
        except Exception as e:
            print("error in send message")
            my_sock.close()
    elif inp_user =="2":
        pass
    else:
        print("invalid input")