# client.py (Run this to join an online game)
import socket
import threading

HOST = input("Enter server IP: ")
PORT = 65432

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(f"\nOpponent: {msg}")
                print("Your guess: ", end="", flush=True)
        except:
            print("\n[!] Connection lost.")
            sock.close()
            break

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except:
        print("[!] Unable to connect to server.")
        return

    print("[✔] Connected to the game server.")
    name = input("Enter your name: ")

    thread = threading.Thread(target=receive, args=(s,), daemon=True)
    thread.start()

    while True:
        try:
            msg = input("Your guess: ")
            s.send(f"{name}: {msg}".encode())
        except:
            print("[!] Disconnected.")
            break

if __name__ == "__main__":
    main()
