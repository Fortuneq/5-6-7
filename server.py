import socket
import pickle
import random

def calculate_key(p, g, A, b):
    B = (g ** b) % p
    K = (A ** b) % p
    return B, K

def decrypt_message(encrypted_message, K):
    decrypted_message = ''.join([chr(ord(char) - K) for char in encrypted_message])
    return decrypted_message

def encrypt_response(response, K):
    encrypted_response = ''.join([chr(ord(char) + K) for char in response])
    return encrypted_response

HOST = '127.0.0.1'
PORT = 8081

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()

msg = pickle.loads(conn.recv(1024))
p, g, A = msg

b = random.randint(2, 10)
B, K = calculate_key(p, g, A, b)
conn.send(pickle.dumps(B))

print("Server's calculated key:", K)

encrypted_message = conn.recv(1024).decode()
decrypted_message = decrypt_message(encrypted_message, K)
print("Client's message:", decrypted_message)

print("Client's message:", decrypted_message)


response = "Hi, client!"
encrypted_response = encrypt_response(response, K)
conn.send(encrypted_response.encode())

conn.close()
