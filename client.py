import socket
import pickle
import random

def decrypt_message(encrypted_message, K):
    decrypted_message = ''.join([chr(ord(char) - K) for char in encrypted_message])
    return decrypted_message

def encrypt_response(response, K):
    encrypted_response = ''.join([chr(ord(char) + K) for char in response])
    return encrypted_response

HOST = '127.0.0.1'
PORT = 8081

sock = socket.socket()
sock.connect((HOST, PORT))

p, g = random.randint(2, 73), random.randint(2, 73)
a = random.randint(2, 10)
A = (g ** a) % p
sock.send(pickle.dumps((p, g, A)))

msg = pickle.loads(sock.recv(1024))
B = msg

K = (B ** a) % p
print("Client's calculated key:", K)

message = "Hello, server!"
encrypted_message = encrypt_response(message, K)
sock.send(encrypted_message.encode())

encrypted_response = sock.recv(1024).decode()
decrypted_response = decrypt_message(encrypted_response, K)
print("Server's response:", decrypted_response)

sock.close()