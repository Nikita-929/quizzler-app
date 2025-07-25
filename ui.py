import os
import sys
from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

# 🔧 Add this function to resolve image paths correctly
def resource_path(relative_path):
    try:
        # For PyInstaller-created .exe
        base_path = sys._MEIPASS
    except Exception:
        # For normal Python run
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(bg=THEME_COLOR)
        self.score_label = Label(text="Score: 0", bg=THEME_COLOR, fg="white")
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(bg="WHITE", height=400, width=400)
        self.question_text = self.canvas.create_text(
            200,
            200,
            width=350,
            text="Quiz",
            font=("Arial", 20, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        # 🖼️ Use resource_path() here for images
        self.right_img = PhotoImage(file=resource_path("images/true.png"))
        self.right_button = Button(image=self.right_img, command=self.right_button_pressed)
        self.right_button.grid(row=2, column=0)

        self.cross_img = PhotoImage(file=resource_path("images/false.png"))
        self.cross_button = Button(image=self.cross_img, command=self.wrong_button_pressed)
        self.cross_button.grid(row=2, column=1)

        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(
                self.question_text,
                text=f"You've reached the end of the quiz having {self.quiz.question_number} questions."
            )
            self.right_button.config(state="disabled")
            self.cross_button.config(state="disabled")

    def right_button_pressed(self):
        is_right = self.quiz.check_answer("True")
        self.give_feedback(is_right)

    def wrong_button_pressed(self):
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)
