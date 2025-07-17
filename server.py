import socket
import threading
import random
import nltk
from nltk.corpus import wordnet, words

# Only do this once (comment after first run)
# nltk.download('words')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

# Prepare the word list
word_list = [w.lower() for w in words.words() if w.isalpha() and 4 <= len(w) <= 8]

def get_word_and_clue():
    while True:
        word = random.choice(word_list)
        synsets = wordnet.synsets(word)
        if synsets:
            clue = synsets[0].definition()
            return word, clue

HOST = '0.0.0.0'
PORT = 65432

players = []
names = []
turn = 0
word = ""
clue = ""
progress = []
guessed_letters = set()
lock = threading.Lock()
game_started = threading.Event()

def broadcast(message):
    for player in players:
        try:
            player.send(message.encode())
        except:
            pass

def update_progress(guess):
    global progress
    updated = False
    for i, letter in enumerate(word):
        if letter == guess and progress[i] == "_":
            progress[i] = guess
            updated = True
    return updated

def display_progress():
    return " ".join(progress)

def handle_client(conn, addr):
    global turn, word, clue, progress, guessed_letters

    try:
        name = conn.recv(1024).decode().strip()
        with lock:
            names.append(name)
            players.append(conn)
        print(f"[+] {name} connected from {addr}")

        if len(players) == 2:
            word, clue = get_word_and_clue()
            progress = ["_"] * len(word)
            guessed_letters = set()
            game_started.set()
            broadcast(f"\n🎯 The word has {len(word)} letters.")
            broadcast(f"💡 Clue: {clue}")
            broadcast(f"🧩 Word: {display_progress()}")
            broadcast(f"\n🔁 It's {names[turn]}'s turn.")
            players[turn].send("Your guess: ".encode())

        else:
            conn.send("⏳ Waiting for another player to join...".encode())
            game_started.wait()  # Wait until 2 players connected

        while True:
            msg = conn.recv(1024).decode().strip().lower()
            if not msg:
                break

            with lock:
                player_idx = players.index(conn)
                if player_idx != turn:
                    conn.send("[!] Not your turn.\nYour guess: ".encode())
                    continue

                response = f"{names[player_idx]} guessed: {msg}"

                if len(msg) == 1:  # Single letter
                    if msg in guessed_letters:
                        conn.send("❗ Letter already guessed.\nYour guess: ".encode())
                        continue

                    guessed_letters.add(msg)
                    if update_progress(msg):
                        response += " ✅"
                    else:
                        response += " ❌"

                else:  # Word guess
                    if msg == word:
                        broadcast(f"\n🏆 {names[player_idx]} guessed the word correctly: '{word}'!")
                        break
                    else:
                        response += " ❌"

                broadcast("\n" + response)
                broadcast(f"🧩 Word: {display_progress()}")

                if "_" not in progress:
                    broadcast(f"\n🎉 The word was fully guessed! Well played!")
                    break

                # Change turn
                turn = 1 - turn
                broadcast(f"\n🔁 It's {names[turn]}'s turn.")
                players[turn].send("Your guess: ".encode())

    except Exception as e:
        print(f"[!] Error from {addr}: {e}")
    finally:
        conn.close()
        with lock:
            if conn in players:
                idx = players.index(conn)
                print(f"[-] {names[idx]} disconnected.")
                del players[idx]
                del names[idx]

def start_server():
    print(f"[🟢] Starting Word Guess Game Server on port {PORT}...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"[🔌] Listening on {HOST}:{PORT}... Waiting for 2 players.")

    while len(players) < 2:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

    # Block main thread until game ends
    while threading.active_count() > 1:
        pass

if __name__ == "__main__":
    start_server()
