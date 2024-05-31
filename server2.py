### Код сервера
import socket
import os

# Параметры сервера
HOST = '0.0.0.0'  # Слушать на всех интерфейсах
PORT = 80
DIRECTORY = 'www'  # Рабочая директория сервера

# Создание и настройка сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)


def handle_request(client_socket):
    # Чтение запроса
    request = client_socket.recv(1024).decode()
    print(f'Request: {request}')

    # Разбор запроса
    try:
        first_line = request.split('\n')[0]
        method, path, _ = first_line.split()

        if method != 'GET':
            response = 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
            client_socket.sendall(response.encode())
            return

        if path == '/':
            path = '/index.html'

        file_path = DIRECTORY + path
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                content = file.read()
            response = 'HTTP/1.1 200 OK\r\n'
            response += f'Content-Length: {len(content)}\r\n'
            response += 'Content-Type: text/html\r\n\r\n'
            client_socket.sendall(response.encode() + content)
        else:
            response = 'HTTP/1.1 404 Not Found\r\n\r\n'
            client_socket.sendall(response.encode())

    except Exception as e:
        print(f'Error: {e}')
        response = 'HTTP/1.1 500 Internal Server Error\r\n\r\n'
        client_socket.sendall(response.encode())

    client_socket.close()


# Главный цикл
print(f'Server running on port {PORT}...')
while True:
    client_socket, addr = server_socket.accept()
    print(f'Connected by {addr}')
    handle_request(client_socket)
