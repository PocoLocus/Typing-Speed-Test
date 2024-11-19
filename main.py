import tkinter as tk
import random

record = 0

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.score = 0
        self.seconds = 60
        self.words = []
        self.word_positions = []
        self.current_word_index = 0
        self.setup_ui()


    def setup_ui(self):
        self.window.title("Typing Speed Test")
        self.window.config(padx=40, pady=20, bg="lightblue")
        self.window.bind("<space>", self.space_pressed)

        self.time_label = tk.Label(self.window, text="60", width=18, bg="white", bd=2, relief="groove")
        self.time_label.grid(row=0, column=0, rowspan=2, columnspan=3)

        self.score_label = tk.Label(self.window, text="words: 0", width=10, bg="white", bd=2, relief="groove")
        self.score_label.grid(row=1, column=2)

        self.record_label = tk.Label(self.window, text=f"record: {record}", width=10, bg="white", bd=2, relief="groove")
        self.record_label.grid(row=0, column=2)

        self.dict_label = tk.Text(self.window, width=60, height=20, bg="white", bd=2, relief="groove", wrap="word")
        self.dict_label.tag_config("highlight", background="yellow", foreground="black")
        self.dict_label.grid(row=2, column=0, columnspan=3, pady=10)
        self.create_the_words_list()

        self.typing_entry = tk.Entry(self.window, width=20)
        self.typing_entry.focus_set()
        self.typing_entry.grid(row=3, column=0, columnspan=3)

        self.start_button = tk.Button(self.window, text="click to start", command=self.start_pressed)
        self.start_button.grid(row=3, column=2)

        self.window.mainloop()

    def create_the_words_list(self):
        with open("english words.txt", "r") as file:
            data = file.read()
            self.words = data.replace('\n', ' ').split()
            random.shuffle(self.words)
        char_index = 0
        for word in self.words:
            self.dict_label.insert(tk.END, word + " ")
            start = char_index
            end = start + len(word)
            self.word_positions.append((start, end))
            char_index += len(word) + 1

    def start_pressed(self):
        self.countdown()
        self.highlight_word()

    def space_pressed(self, event=None):
        self.check_word()
        self.reset_entry()
        self.highlight_word()

    def countdown(self):
        self.time_label.config(text=self.seconds)
        if self.seconds > 0:
            self.window.after(1000, self.countdown)
            self.seconds -= 1
        else:
            self.end_of_game()

    def highlight_word(self):
        if self.current_word_index < len(self.words):
            self.dict_label.tag_remove("highlight", "1.0", tk.END)

            word_start = f"1.0 + {self.word_positions[self.current_word_index][0]} chars"
            word_end = f"1.0 + {self.word_positions[self.current_word_index][1]} chars"

            self.dict_label.tag_add("highlight", word_start, word_end)
            self.current_word_index += 1

    def check_word(self):
        typed_word = self.typing_entry.get().strip()
        if typed_word == self.words[self.current_word_index-1]:
            self.score += 1
            self.score_label.config(text=f"words: {self.score}")

    def reset_entry(self):
        self.typing_entry.delete(0, 'end')

    def end_of_game(self):
        self.typing_entry.grid_remove()
        self.dict_label.grid_remove()
        self.time_label.grid_remove()
        self.score_label.grid_remove()
        self.start_button.grid_remove()
        self.record_label.grid_remove()
        self.window.config(bg="lightgreen")
        end_label = tk.Label(self.window, text=f"End of time.\nYour score was: {self.score} words per minute!\nThe record is: {record}", bg="lightgreen")
        end_label.grid(row=0, column=0, columnspan=2, pady=10)
        restart_button = tk.Button(self.window, text="restart", command=self.restart_game)
        restart_button.grid(row=1, column=0)
        exit_button = tk.Button(self.window, text="exit", command=self.exit_game)
        exit_button.grid(row=1, column=1)

    def restart_game(self):
        global record
        if self.score > record:
            record = self.score
        self.window.destroy()
        restarted_app = App()

    def exit_game(self):
        self.window.destroy()

app = App()
