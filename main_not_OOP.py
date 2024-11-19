import tkinter as tk
import random

word_positions = []
current_word_index = 0
score = 0
seconds = 60

def space_pressed(event=None):
    if current_word_index == 0:
        countdown()
    check_word()
    reset_entry()
    highlight_word()

def countdown():
    global seconds
    time_label.config(text=seconds)
    if seconds > 0:
        window.after(1000, countdown)
        seconds -= 1
    else:
        typing_entry.grid_remove()
        dict_label.grid_remove()
        time_label.grid_remove()
        score_label.grid_remove()
        end_label = tk.Label(window, text=f"End of time.\nYour score was: {score} words per minute!", bg="lightgreen")
        end_label.grid(row=0, column=0, pady=10)
        window.config(bg="lightgreen")


def check_word():
    global score
    typed_word = typing_entry.get().strip()
    if typed_word == words[current_word_index-1]:
        score += 1
        score_label.config(text=f"words: {score}")

def reset_entry():
    typing_entry.delete(0, 'end')

def highlight_word():
    global current_word_index
    if current_word_index < len(words):
        dict_label.tag_remove("highlight", "1.0", tk.END)

        word_start = f"1.0 + {word_positions[current_word_index][0]} chars"
        word_end = f"1.0 + {word_positions[current_word_index][1]} chars"

        dict_label.tag_add("highlight", word_start, word_end)
        current_word_index += 1

window = tk.Tk()
window.title("Typing Speed Test")
window.config(padx=40, pady=20, bg="lightblue")

time_label = tk.Label(window, text="Press <space> to start", width=18, bg="white", bd=2, relief="groove")
time_label.grid(row=0, column=1)

score_label = tk.Label(window, text=f"words: 0", width=10, bg="white", bd=2, relief="groove")
score_label.place(x=400,y=8)

dict_label = tk.Text(window, width=60, height=20, bg="white", bd=2, relief="groove", wrap="word")
dict_label.tag_config("highlight", background="yellow", foreground="black")
dict_label.grid(row=1, column=0, columnspan=3, pady=10)

with open("english words.txt", "r") as file:
    data = file.read()
    words = data.replace('\n', ' ').split()
    random.shuffle(words)

char_index = 0
for word in words:
    dict_label.insert(tk.END, word + " ")
    start = char_index
    end = start + len(word)
    word_positions.append((start, end))
    char_index += len(word) + 1

typing_entry = tk.Entry(window, width=20)
typing_entry.focus_set()
typing_entry.grid(row=2, column=0, columnspan=3)


window.bind("<space>", space_pressed)

window.mainloop()
