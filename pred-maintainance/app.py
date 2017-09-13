from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():

return 'alexa solar pm welcome!'

if __name__ == "__main__":
	app.run()