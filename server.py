# server.py (Host this file to enable 2-player online mode)
import socket
import threading

HOST = '0.0.0.0'
PORT = 65432

clients = []

def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"{addr}: {msg}")
            for client in clients:
                if client != conn:
                    client.send(msg.encode())
        except:
            break
    conn.close()
    clients.remove(conn)
    print(f"[-] Disconnected {addr}")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print(f"[🔌] Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
