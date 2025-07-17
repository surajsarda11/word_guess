import socket

def main():
    HOST = input("Enter server IP: ").strip()
    PORT = 65432

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except Exception as e:
        print(f"[!] Unable to connect to server: {e}")
        return

    print("[✔] Connected to the game server.")
    name = input("Enter your name: ").strip()
    client.send(name.encode())  # Send player name to server

    while True:
        try:
            data = client.recv(2048).decode()

            if not data:
                print("[!] Connection closed by server.")
                break

            # Handle different kinds of server messages
            if data.startswith("START"):
                _, clue, masked, attempts = data.split("|")
                print(f"\n🧠 Clue: {clue}")
                print(f"📝 Word: {masked}")
                print(f"🔁 Attempts remaining: {attempts}")

            elif data.startswith("TURN"):
                _, masked, attempts = data.split("|")
                print(f"\n📝 Word: {masked}")
                print(f"🔁 Attempts remaining: {attempts}")
                guess = input("Your guess: ").strip().lower()
                client.send(guess.encode())

            elif data.startswith("MSG"):
                _, message = data.split("|", 1)
                print(f"\n💬 {message}")

            elif data.startswith("RESULT"):
                _, final_word, winner = data.split("|")
                print(f"\n✅ Final Word: {final_word}")
                if winner == name:
                    print("🎉 You won!")
                elif winner == "None":
                    print("😞 No one guessed the word.")
                else:
                    print(f"🏆 {winner} won the game.")
                break

            elif data.startswith("EXIT"):
                print("\n🔚 Game has ended.")
                break

            else:
                print(f"\n[Server]: {data}")

        except Exception as e:
            print(f"[!] Error: {e}")
            break

    client.close()


if __name__ == "__main__":
    main()
