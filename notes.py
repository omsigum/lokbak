from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
@app.route("/bla")
def bla():
	return "hello bla test"
if __name__ == "__main__":
    app.run(host='0.0.0.0')
