import socket
import os


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

def get_url_post(answer):
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
    if len(params) == 3 and params[0] == 'POST' and params[2] == 'HTTP/1.1':
        url = params[1][1:]
    return url

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
        secret_message = get_secret_msg(data)
        secret_message += "\n"
        print(secret_message)
        with open(file_name, "w") as f:
            f.write(secret_message)
    elif mode == "get":
        if url is not None:
            if url == '':
                answer = open_files("index.html")
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