from flask import Flask, request
from Wilson_detector import process_data
from state_keepers import DetectorState, PlotsState

app = Flask(__name__)

@app.route("/")
def welcome():
    return "Witaj uzytkowniku!"


czy_ktos_gra = DetectorState()


@app.route("/gra/<stan>", methods=["GET"])
def set(stan):
    global czy_ktos_gra
    czy_ktos_gra = stan == "tak"
    return "ustawiono na {}".format(czy_ktos_gra)


@app.route("/stan", methods=["GET"])
def get():
    #request.json()
    return "Pilkazyki zajete? {}".format("tak" if czy_ktos_gra else "nie")


if __name__ == "__main__":
    app.run()

# def memoize(f)
#     pamiec = {}
#     def wrapped(*args, **kwargs):
#         if istnieje:
#             return pamiec[args+kwargs]
#         else:
#             pamiec[args+kwargs] = f(args, kwargs)
#             return pamiec[args+kwargs]
#     return wrapped

# @memoize
# def test(x):
#     return x**(1/2)
