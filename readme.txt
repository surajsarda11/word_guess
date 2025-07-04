---

## 🎮 Word Guess Game (Command-Line Version)

**Word Guess Game** is an engaging Python-based word puzzle that supports:

* 🧑‍🎓 Single Player (age-based difficulty + dictionary clues)
* 👯‍♂️ Local Two Player (alternating turns, funny punishments)
* 🌐 Online Two Player (client-server based play over LAN/internet)
* 🏆 Local Leaderboard (cumulative score tracking)
* 🎓 Post-game learning (meaning & synonyms)
* 🎉 Achievement system

---

## 🛠️ Features

* ✅ **Age-based word difficulty** (child, teen, adult)
* 🧠 **Smart clues** powered by [WordNet](https://wordnet.princeton.edu/)
* 🧩 **Word meaning & synonyms** shown after each game
* 🔁 **Letter reveal** after 2 wrong guesses
* 🧍‍♂️ **Single player mode** with achievements
* 👥 **Two player local mode** with turn-based gameplay
* 🌐 **Two player online mode** via `server.py` and `client.py`
* 📊 **Local leaderboard** (persistent and accumulative)

---

## 🐍 Requirements

* Python 3.7+
* Dependencies:

  ```bash
  pip install nltk colorama
  ```
* For first-time use of NLTK:

  ```python
  import nltk
  nltk.download('wordnet')
  nltk.download('omw-1.4')
  nltk.download('words')
  ```

## ▶️ How to Play

### 🔹 1. Launch the Game

In your terminal or command prompt:

```bash
python word_guess.py
```

### 🔹 2. Choose an Option

You'll be presented with:

```
1. Single Player
2. Two Player
3. Leaderboard
4. Exit
```

---

## 🧍 Single Player Mode

1. Enter your **name** and **age**.
2. Select difficulty: `easy`, `medium`, or `hard`.
3. Try to guess the word using:

   * Hints like word meanings
   * Optional letter reveals after two wrong guesses
4. Final score is saved to your local leaderboard.

---

## 👥 Two Player - Local Mode

1. Choose “Two Player” → then choose `Local Play`.
2. Enter both players’ names.
3. A challenging word is selected and turns are taken.
4. Player who guesses the word earns the score.
5. Funny punishments are randomly shown for incorrect guesses.

---

## 🌐 Two Player - Online Mode

### On Host PC:

1. Run the server:

   ```bash
   python server.py
   ```

### On Friend’s PC:

2. Run the client and enter host's IP:

   ```bash
   python client.py
   ```

Both players can now play remotely in turn-based mode.

---

## 🏅 Leaderboard

Choose “Leaderboard” from the main menu to view the top 5 players and their scores.

Leaderboard is cumulative — your progress stays saved between sessions.

---

## ✨ Example Gameplay

```
🧩 Clue: feline mammal usually having thick soft fur and no ability to roar: domestic cats; wildcats (Length: 3)
Word: _ _ _
Guess a letter or word: c
✅ 'c' is in the word.
...
🎉 Great! You revealed the whole word!
```

---
