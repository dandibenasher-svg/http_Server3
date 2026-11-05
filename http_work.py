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
    if len(params) == 3 and (params[0] == 'GET' or params[0] == 'POST') and params[2] == 'HTTP/1.1':
        url = params[1][1:]
    return url

def keep_image(image_name, image_data):
    with open("image_keep", "a") as f:
        f.write(image_name + "\n")
    os.makedirs("image_folder", exist_ok=True)
    with open(os.path.join("image_folder", image_name), "wb") as f:
        f.write(image_data)


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
            data = client_sock.recv(1024)
            if not data:
                client_sock.close()
                print("closed the connection")
                break

            while b"\r\n\r\n" not in data:
                more_data = client_sock.recv(1024)
                if not more_data:
                    break
                data += more_data
            if b"\r\n\r\n" not in data:
                client_sock.close()
                break

            image_name = data.split(b"\r\n\r\n", 1)[0]
            image_data = data.split(b"\r\n\r\n", 1)[1]
            content_length = 0
            for line in image_name.decode().split("\r\n"):
                if "Content-Length" in line:
                    content_length = int(line.split(":")[1])

            while len(image_data) < content_length:
                more_data = client_sock.recv(min(1024, content_length - len(image_data)))
                if not more_data:
                    break
                image_data += more_data

        except Exception as e:
            print(f"error in recv {str(e)}")
            client_sock.close()
            print("closed the connection")
            continue


        url = get_url(image_name.decode())
        mode = test_get_post(image_name.decode())
        if mode == "post":
            if "?secret" in url:
                file_name = "secret_keep.txt"
                secret_message = get_secret_msg(data.decode())
                secret_message += "\n"
                print(secret_message)
                with open(file_name, "a") as f:
                    f.write(secret_message)

            elif "img_name=" in url:
                image_file_name = url.split("img_name=")[1]
                keep_image(image_file_name, image_data)
                print(os.path.abspath(os.path.join("image_folder", image_file_name)))
                print("Image saved")
                continue

        elif mode == "get":
            if url is not None:
                print("=============================================" + url +"========" + "/E:/other cyber work/move1.jpg")
                if url.split("?")[0] == "image":
                    image_file_name = url.split("img-name=")[1]
                    image_path = os.path.join("image_folder", image_file_name)
                    if os.path.exists(image_path):
                        answer = open_files(image_path)
                    else:
                        answer = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n".encode()

                elif url == '':
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