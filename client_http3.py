import socket
import os

my_sock = socket.socket()
try:
    my_sock.connect(("127.0.0.1",80))
except Exception as e:
    print("error didnt connect to server" + str(e))
    my_sock.close()


while True:
    inp_user = input("for secret message insert 1\nto send photo insert 2\nto disconnect insert 3\n")
    if inp_user =="1":
        inp_msg = input("please insert the secret message")
        msg = f"POST /http_work?secret HTTP/1.1\r\nContent-length: {len(inp_msg)}\r\n\r\n{inp_msg}"
        try:
            my_sock.send(msg.encode())
        except Exception as e:
            print("error in send message")
            my_sock.close()
    elif inp_user =="2":
        image_path = input("Please insert the image path: ")

        if os.path.exists(image_path):
            image_name = os.path.basename(image_path)
            with open(image_path, "rb") as f:
                image_data = f.read()
            msg = f"POST /http_work?img_name={image_name} HTTP/1.1\r\nContent-Length: {len(image_data)}\r\n\r\n"
            try:
                my_sock.sendall(msg.encode() + image_data)
                print("Image sent!")
            except Exception as e:
                print("Error sending image: " + str(e))
    elif inp_user == "3":
        my_sock.close()
        print("Disconnected from server")
        break
    else:
        print("invalid input")