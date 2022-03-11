from words import words_list
import tkinter as tk
import random
import copy


words_selected = []
text_selected = ""
words_left = []
words_deleted = []
correct_words = 0
incorrect_words = 0
countdown_started = False


# select 200 words and put them on screen
def reset_text():
    global words_selected, text_selected, words_left, correct_words, incorrect_words, countdown_started
    words_selected = copy.deepcopy(words_list)
    correct_words = 0
    incorrect_words = 0
    for n in range(0, 300):
        word_to_delete = random.choice(words_selected)
        words_selected.remove(word_to_delete)
    random.shuffle(words_selected)
    words_left = copy.deepcopy(words_selected)
    text_selected = " "
    text_selected = text_selected.join(words_selected)
    test_text.config(state="normal")
    test_text.delete(1.0, tk.END)
    test_text.insert(tk.END, text_selected)
    test_text.config(state="disabled")
    text_box.config(state="normal")
    text_box.delete(1.0, tk.END)
    correct_count.set(f"Correct words: 0")
    incorrect_count.set(f"Incorrect words: 0")
    timer_var.set("Seconds left: 60")
    wpm_var.set("Words per minute: 0")
    countdown_started = False


# check typed words on each key press
def check_text(*args):
    global words_left, correct_words, incorrect_words, words_deleted
    correct_words = 0
    incorrect_words = 0
    typed_text = text_box.get(1.0, tk.END)
    typed_list = typed_text.split(" ")
    typed_list[len(typed_list) - 1] = typed_list[len(typed_list) - 1].strip("\n")
    for n in range(0, len(typed_list)):
        if typed_list[n] == words_selected[n] and countdown_started:
            correct_words += 1
        elif countdown_started:
            incorrect_words += 1
    correct_count.set(f"Correct words: {correct_words}")
    incorrect_count.set(f"Incorrect words: {incorrect_words}")


# start timer if timer not already started
def start_timer(*args):
    global countdown_started
    if not countdown_started:
        countdown_started = True
        count_down(60)


# count down mechanism
def count_down(seconds_left):
    if seconds_left != 0 and countdown_started:
        try:
            app.after(1000, count_down, seconds_left - 1)
            timer_var.set(f"Seconds left: {seconds_left}")
            wpm_var.set(f"Words per minute: {int(correct_words//((60 - seconds_left)/60))}")
        except ZeroDivisionError:
            timer_var.set(f"Seconds left: {seconds_left}")
            wpm_var.set(f"Words per minute: 60")
    elif seconds_left == 0:
        timer_var.set(f"Seconds left: {seconds_left}")
        wpm_var.set(f"Words per minute: {int(correct_words // ((60 - seconds_left) / 60))}")
        text_box.config(state="disabled")


# app
app = tk.Tk()
app.minsize(width=950, height=600)
app.title("Check your typing speed in 60 seconds")
app.config(padx=50, pady=50)

# disabled entry with text for test
test_text = tk.Text(app, width=50, height=18, state="disabled", wrap="word", font=("arial", 14))
test_text.grid(row=0, column=0, padx=10, pady=10, sticky="we")

# entry for text
text_box = tk.Text(app, width=50, height=18, wrap="word", font=("arial", 14))
text_box.bind("<space>", check_text)
text_box.bind("<KeyRelease>", start_timer)
text_box.grid(row=0, column=1, padx=10, pady=10, sticky="we", columnspan=2)

# reset button
reset_btn = tk.Button(app, text="Reset", command=reset_text, width=8)
reset_btn.grid(row=1, column=0, padx=10, pady=10)

# labels for word count
correct_count = tk.StringVar(app, value=f"Correct words: 0")
correct_lbl = tk.Label(app, textvariable=correct_count)
incorrect_count = tk.StringVar(app, value=f"Incorrect words: 0")
incorrect_lbl = tk.Label(app, textvariable=incorrect_count)
correct_lbl.grid(row=1, column=1, padx=10, pady=10, sticky="e")
incorrect_lbl.grid(row=2, column=1, padx=10, pady=10, sticky="e")

# label for timer and words per minute
timer_var = tk.StringVar(app, value="Seconds left: 60")
timer = tk.Label(app, textvariable=timer_var)
wpm_var = tk.StringVar(app, value="Words per minute: 0")
wpm = tk.Label(app, textvariable=wpm_var)
timer.grid(row=1, column=2, padx=10, pady=10, sticky="e")
wpm.grid(row=2, column=2, padx=10, pady=10, sticky="e")

reset_text()

app.mainloop()
