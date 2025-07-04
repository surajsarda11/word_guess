# word_guess.py (Final Version Without Timer & Improved Clue Format)
import random
import json
import os
import platform
import nltk
from nltk.corpus import wordnet as wn, words
from colorama import init, Fore

init(autoreset=True)
nltk.download('wordnet', quiet=True)
nltk.download('words', quiet=True)
nltk.download('omw-1.4', quiet=True)

leaderboard_file = "leaderboard.json"
word_list = words.words()

AGE_WORD_LEVELS = {
    'child': (3, 5),
    'teen': (5, 7),
    'adult': (7, 12)
}

funny_punishments = [
    "Sing a song out loud!",
    "Do 10 jumping jacks!",
    "Act like a chicken for 10 seconds!",
    "Tell a joke (good or bad).",
    "Say 'I love Word Guess' loudly!"
]

# Leaderboard functions
def load_leaderboard():
    return json.load(open(leaderboard_file)) if os.path.exists(leaderboard_file) else {}

def save_leaderboard(data):
    with open(leaderboard_file, "w") as f:
        json.dump(data, f, indent=4)

def update_leaderboard(name, score):
    data = load_leaderboard()
    if name in data:
        if isinstance(data[name], int):
            data[name] = {"score": data[name] + score, "games": 1}
        else:
            data[name]["score"] += score
            data[name]["games"] += 1
    else:
        data[name] = {"score": score, "games": 1}
    save_leaderboard(data)

def display_leaderboard():
    data = load_leaderboard()
    sorted_data = sorted(data.items(), key=lambda x: x[1]['score'], reverse=True)
    print(Fore.YELLOW + "\n🏆 Leaderboard 🏆")
    for i, (name, stats) in enumerate(sorted_data[:5], 1):
        print(f"{i}. {name} - {stats['score']} pts in {stats['games']} games")

# Word logic
def get_word_by_difficulty(age, difficulty):
    level = 'child' if age < 12 else 'teen' if age < 18 else 'adult'
    min_len, max_len = AGE_WORD_LEVELS[level]
    if difficulty == 'easy':
        max_len = min_len + 2
    elif difficulty == 'hard':
        min_len += 2

    filtered = [w for w in word_list if w.isalpha() and min_len <= len(w) <= max_len and wn.synsets(w)]
    word = random.choice(filtered).lower()
    syn = wn.synsets(word)[0]
    meaning = syn.definition()
    synonyms = [lemma.name() for lemma in syn.lemmas()][1:4]
    return word, meaning, synonyms

def get_clue(word, meaning):
    return f"🧩 Clue: {meaning} (Length: {len(word)})"

def post_game_learning(word, meaning, synonyms):
    print(Fore.CYAN + f"\n📘 Word: {word}")
    print(f"Meaning: {meaning}")
    print(f"Synonyms: {', '.join(synonyms)}\n")

def check_achievements(score, attempts):
    if score >= 30:
        print(Fore.MAGENTA + "🏅 Achievement Unlocked: Word Wizard!")
    if attempts == 1:
        print(Fore.MAGENTA + "🏅 Achievement Unlocked: Clutch Saver!")

def play_game(word, clue, player, meaning, synonyms):
    guesses = []
    attempts = len(word) + 3
    score = 0
    wrong_streak = 0

    print(Fore.CYAN + f"\n{clue}")
    print(f"You have {attempts} attempts.\n")

    while attempts > 0:
        display = [c if c in guesses else '_' for c in word]
        print("Word:", " ".join(display))
        guess = input("Guess a letter or word: ").strip().lower()

        if not guess:
            print(Fore.RED + "❌ Invalid input!")
            continue

        if guess == word:
            print(Fore.GREEN + "🎉 Correct! You guessed the word!")
            score += 10 + attempts
            break
        elif len(guess) == 1:
            if guess in word:
                print(Fore.GREEN + f"✅ '{guess}' is in the word.")
                guesses.append(guess)
                wrong_streak = 0
            else:
                print(Fore.RED + f"❌ '{guess}' is not in the word.")
                attempts -= 1
                wrong_streak += 1
        else:
            print(Fore.RED + "❌ Wrong full word guess!")
            attempts -= 2
            wrong_streak += 1

        if all(c in guesses for c in word):
            print(Fore.GREEN + "🎉 You revealed the word!")
            score += 10 + attempts
            break

        if wrong_streak >= 2 and attempts > 1:
            reveal_choice = input("Reveal a letter? (y/n): ").strip().lower()
            if reveal_choice == 'y':
                unrevealed = [c for c in set(word) if c not in guesses]
                if unrevealed:
                    reveal = random.choice(unrevealed)
                    guesses.append(reveal)
                    print(Fore.CYAN + f"🔍 Letter revealed: {reveal}")
            wrong_streak = 0

        print(f"Remaining Attempts: {attempts}\n")

    if attempts <= 0:
        print(Fore.RED + f"💀 Game Over! The word was: {word}")

    print(Fore.CYAN + f"Your score: {score} points\n")
    update_leaderboard(player, score)
    post_game_learning(word, meaning, synonyms)
    check_achievements(score, attempts)

def play_single():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    diff = input("Choose difficulty (easy/medium/hard): ").lower()
    while diff not in ['easy', 'medium', 'hard']:
        diff = input("Invalid. Choose difficulty (easy/medium/hard): ").lower()
    word, meaning, synonyms = get_word_by_difficulty(age, diff)
    clue = get_clue(word, meaning)
    play_game(word, clue, name, meaning, synonyms)

def main():
    while True:
        print(Fore.MAGENTA + "\n🎮 Word Guess Game 🎮")
        print("1. Single Player")
        print("2. View Leaderboard")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            play_single()
        elif choice == '2':
            display_leaderboard()
        elif choice == '3':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
