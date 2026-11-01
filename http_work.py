import socket
import os
def get_url(answer):
    """
    returns url from client request
    param answer: the request
    returns: the url
    """
    url = None
    lines1 = answer.split('\r\n')[0]
    params = lines1.split(' ')
    if len(params) == 3 and params[0] == 'GET' and params[2] == 'HTTP/1.1':
        url = params[1][1:]
    return url

def get_secret_msg(data):
    """
    returns the message inside the secret message
    param data: the data we got from the client
    returns: the secret message itself without the post template
    """
    return data.split('\r\n\r\n')[1]


def test_get_post(answer):
    """
    returns url from client request
    param answer: the request
    returns: the url
    """
    lines1 = answer.split('\r\n')[0]
    params = lines1.split(' ')
    if params[0] == 'GET':
        return "get"
    elif params[0] == 'POST':
        return "post"
    else:
        return "none"

def open_files(file_name):
    """
    opens file
    param file_name: the name of the file we want to open
    ans with the new file
    """
    with open(file_name, 'rb') as f:
        file_data = f.read()

    file_data_len = str(len(file_data)).zfill(6)
    return f"HTTP/1.1 200 OK\r\nContent-Length: {file_data_len}\r\n\r\n".encode() + file_data

server_soc = socket.socket()
server_soc.bind(("0.0.0.0", 80)) #8080 if it doesnt work
server_soc.listen(3)

banlist = ["banned%20file.jpg"]
moved_dict = {"move1.jpg":"/move2.jpg"}
while True:
    client_sock, addr = server_soc.accept()
    print(f"{addr[0]} - connected")
    while True:
        try:
            data = client_sock.recv(1024).decode()
        except Exception as e:
            print(f"error in recv {str(e)}")
            client_sock.close()
            print("closed the connection")
            continue

        file_name="secret_keep.txt"
        url = get_url(data)
        mode = test_get_post(data)
        if mode == "post":
            if "?secret" in data:
                secret_message = get_secret_msg(data)
                secret_message += "\n"
                print(secret_message)
                with open(file_name, "r") as f:
                    secret_info = f.read()
                with open(file_name, "w") as f:
                    f.write(secret_info + secret_message)
            elif "?image" in url:
                pass
        elif mode == "get":
            if url is not None:
                print("=============================================" + url +"========" + "/E:/other cyber work/move1.jpg")
                if url == '':
                    answer = open_files("index.html")
                elif url =="calculate-next":
                    answer = "HTTP/1.1 200 OK\r\nContent-Length: 1\r\n\r\n5".encode()
                elif url.split("=")[0] == "calculate-next?num":
                    num=url.split("=")[1]
                    if num.isdigit():
                        num=int(num)
                        num=num+1
                        answer = f"HTTP/1.1 200 OK\r\nContent-Length: {len(str(num))}\r\n\r\n{str(num)}".encode()
                elif url.split("?")[0] == "calculate-area":
                    if not ((url.split("&")[0].split("?")[1].split("=")[0] == "height" and url.split("&")[1].split("=")[0] == "width") or
                        (url.split("&")[0].split("?")[1].split("=")[0] == "width" and url.split("&")[1].split("=")[0] == "height")):
                        answer = "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n".encode()
                    else:
                        num1=url.split("=")[1]
                        num1=num1.split("&")[0]
                        num2=url.split("=")[2]
                        if num1.isdigit()&num2.isdigit():
                            ans=int(num1)*int(num2)/2
                            answer = f"HTTP/1.1 200 OK\r\nContent-Length: {len(str(ans))}\r\n\r\n{str(ans)}".encode()
                elif url in banlist:
                    answer = f"HTTP/1.1 403 forbidden file\r\nContent-Length: 0\r\n\r\n".encode()
                elif url in moved_dict:
                    answer = f"HTTP/1.1 301 Moved Permanently\r\nLocation: " + moved_dict[url] + "\r\nContent-Length: 0\r\n\r\n"
                    answer=answer.encode()
                elif url.split(".")[-1] == "server":
                    answer = "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n".encode()
                elif os.path.exists(url):
                    answer = open_files(url)
                else:
                    answer = f"HTTP/1.1 404 not found\r\nContent-Length: 0\r\n\r\n".encode()
                try:
                    client_sock.send(answer)
                except Exception as e:
                     print(f"error in send {str(e)}")
            client_sock.close()
            print("closed the connection")