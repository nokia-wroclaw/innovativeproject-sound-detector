from flask import Flask
from time import time
import os

from stack import Stack

app = Flask(__name__,
            static_url_path='', 
            static_folder='frontend')

stack = Stack()

treshold = 5 * 60
not_less_than = 10

@app.route("/knock", methods=["GET"])
def set():
    stack.knock()
    return "knock"

@app.route("/status", methods=["GET"])
def get():
    now = time()
    witin_5_minutes = [t for t in stack.history if now - t < treshold]
    if len(witin_5_minutes) >= not_less_than:
        return "taken"
    return "free"

if __name__ == "__main__":
    app.run()
