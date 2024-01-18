from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
	return 'App 2'

if __name__ == "__main__":
	app.run(debug=True, port=8080, host='0.0.0.0')