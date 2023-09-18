# quiz_control.py

from __future__ import annotations
import time
from prettytable import PrettyTable
from termcolor import colored


class Model:
    def __init__(self, text: str, answer: str):
        self.question: str = text
        self.answer: str = answer


class QuizControl:
    TRUTH_LITERALS = {
        "T",
        "t",
        "TRUE",
        "True",
        "true",
        "yes",
        "Yes",
        "y",
        "Y",
        "YES",
    }

    FALSE_LITERALS = {
        "F",
        "f",
        "False",
        "false",
        "FALSE",
        "no",
        "No",
        "n",
        "N",
        "NO",
    }

    def __init__(self, positive_marks: int, negative_marks: int):
        self.questions: dict = {}
        self.score: int = 0
        self.stats: dict = {
            "curr_streak": 0,
            "streak_arr": [],
            "correct_questions": 0,
            "incorrect_questions": 0,
            "time_intervals": [],
        }
        self.plus: int = positive_marks
        self.minus: int = negative_marks
        self.unasked_questions: set = set()
        self.asked_questions: set = set()
        self.timing: dict = {"time_start": 0.0, "time_end": 0.0}

    def add_model(self, question: str, answer: str) -> int:
        """
        Adds a Model to the questions instance attribute

        Adds a new entry to the questions dictionary, where the key
        is a tuple containing 'question' and 'answer', and the
        corresponding value is an instance of the Model class
        initialized with the provided question and answer

        Args:
            question (str): The text of the question
            answer (str): The answer to the question

        Returns:
            int: Always return 0 to indicate successfull addition
        """

        self.questions[(question, answer)] = Model(question, answer)
        self.unasked_questions.add((question, answer))
        return 0

    def remove_model(self, question: str, answer: str) -> int:
        """
        Removes a Model from the questions instance attribute

        Args:
            question (str): The text of the question
            answer (str): The answer to the question

        Returns:
            int: Always return 0 to indicate successfull removal
        """

        if (question, answer) in self.questions:
            del self.questions[(question, answer)]
            self.unasked_questions.discard((question, answer))
            self.asked_questions.discard((question, answer))
        return 0

    def mod_score(self, status: bool) -> int:
        """
        Modifies the score instance attribute

        Adds or Subtracts points from the total score
        based on whether status is False (wrong answer)
        or stats is True (correct answer)

        Args:
            status (bool): Whether or not the answer was right

        Returns:
            int: Always return 0 if the score was modified correctly
        """

        if status is False:
            self.score += self.minus
            self.mod_streak(status)
            self.stats["incorrect_questions"] += 1
            return 0
        self.score += self.plus
        self.stats["correct_questions"] += 1
        self.mod_streak(status)
        return self.score

    def mod_streak(self, status: bool) -> int:
        """
        Modifies the streak array and current streak instance attributes

        Appends the most recent streak to the 'streak_arr' if the
        question was answered incorrectly (status False), and sets the
        'curr_streak' to zero. If the question was answered correctly
        then the 'curr_streak' is simply incremented
        Also prints the status of the answer and the current streak
        in both cases

        Args:
            status (bool): Whether or not the question was answered correctly

        Returns:
            int: Always return 0 if the modification occurs succesfully
        """

        if status is False:
            self.stats["streak_arr"].append(self.stats["curr_streak"])
            self.stats["curr_streak"] = 0
            print(colored("Incorrect answer", "red", attrs=["bold"]))
            print("Current Streak: ", self.stats["curr_streak"], "\n")
            return 0
        self.stats["curr_streak"] += 1
        print(colored("Correct Answer", "green", attrs=["bold"]))
        print("Current Streak: ", self.stats["curr_streak"], "\n")
        return 0

    def evaluate_response(self, question: str, answer: str, response: str) -> int:
        """
        Evaluates the response with the question and corresponding answer

        Calls the 'mod_score' instance attribute after evaluating the
        correctness of 'response' with respect to 'question' and its
        corresponding 'answer'

        Args:
            question (str): The text of the question
            answer (str): The text containing the answer to the question
            response (str): The text containing possible user input

        Returns:
            int: -1 if the question is not described by the "questions" attribute instance
                and 0 if the evaluation was done completely
        """

        model = self.questions.get((question, answer))
        if model is None:
            return -1
        self.mod_score(model.answer == response)
        return 0

    def ask_question(self) -> tuple:
        """
        Prints out a question that is not in the 'asked_questions' instance attribute

        Checks if an unanswered question exists, and if so, prints out a question
        and then adds it to the set of answered questions.

        Args:
            None

        Returns:
            tuple: An integer and the question text. The integer is the status and is
                   0 for a successfull retreival of a question, -1 otherwise
        """

        if self.unasked_questions:
            model_tuple = self.unasked_questions.pop()
            self.asked_questions.add(model_tuple)
            model = self.questions.get(model_tuple)
            print("Q" + str(len(self.asked_questions)) + ": " + model.question)
            return 0, model.question

        return -1, None

    def get_answer(self, question: str) -> str | int:
        """
        Obtains the answer for a given question

        Access the 'questions' instance attribute and finds the corresponding
        answer to a given question

        Args:
            question (str): The text of the question

        Returns:
            str | int: A string containing the answer, or -1 if no answer was found
        """

        for _, model in self.questions.items():
            if model.question == question:
                return model.answer
        return -1

    def assert_time(self, state="start") -> int:
        """
        Asserts the time when called relative to the UNIX epoch

        Evaluates the time when this function is called, either in a
        start state or an end state. In the end state, the time interval
        relative to when this function was called in the start state is
        appended to the 'time_intervals' key of the 'stats' instance attribute

        Args:
            state (str): Defaults to "start", string denoting the state

        Returns:
            int: Always return 0 for a succesfull assertion
        """

        if state == "start":
            self.timing["time_start"] = time.time()
            return 0
        self.timing["time_end"] = time.time()
        self.stats["time_intervals"].append(
            self.timing["time_end"] - self.timing["time_start"]
        )
        return 0

    def get_response(self) -> str:
        """
        Get's user input for the question and returns "True" or "False" based on it's veracity

        Obtains variable input and assesses if it is equivalent to "True" or "False"
        using the class constants 'TRUTH_LITERALS' and 'FALSE_LITERALS'. If it is
        neither, the user is persisted for another input

        Args:
            None

        Returns:
            str: Returns "True" or "False"
        """

        while True:
            self.assert_time()
            res = str(input("Enter your answer: "))
            if res in self.TRUTH_LITERALS:
                self.assert_time("end")
                return "True"
            if res in self.FALSE_LITERALS:
                self.assert_time("end")
                return "False"

            print("Invalid input, try again \n")

    def questions_remain(self) -> bool:
        """
        Returns true if there are some unanswered questions if they remain

        The function returns True if unasked questions remain, and False otherwise

        Args:
            None

        Returns:
            bool: True or False based on whether unasked questions remain
        """
        return len(self.unasked_questions) != 0

    def get_stats(self) -> None:
        """
        Get's statistics for the quiz

        Prints out a detialed description of the stats of the quiz in a prettytable
        format with the following columns:
            [
                "Correct questions",
                "Incorrect questions",
                "Highest Streak",
                "Accuracy",
                "Average Time",
                "Total score",
            ]

        Args:
            None
        """

        self.stats["streak_arr"].append(self.stats["curr_streak"])
        print("Compiling statistics...\n")
        accuracy = round(
            (
                self.stats["correct_questions"]
                / (self.stats["correct_questions"] + self.stats["incorrect_questions"])
            )
            * 100,
            2,
        )
        highest_streak = max(self.stats["streak_arr"])
        average_time = round(
            sum(self.stats["time_intervals"]) / len(self.stats["time_intervals"]), 2
        )
        time.sleep(0.5)
        display_table = PrettyTable(
            [
                "Correct questions",
                "Incorrect questions",
                "Highest Streak",
                "Accuracy",
                "Average Time",
                "Total score",
            ]
        )
        display_table.add_row(
            [
                self.stats["correct_questions"],
                self.stats["incorrect_questions"],
                highest_streak,
                str(accuracy) + " %",
                str(average_time) + " s",
                self.score,
            ]
        )
        print(display_table)
