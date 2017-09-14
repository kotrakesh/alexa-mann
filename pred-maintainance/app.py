from flask import Flask
app = Flask(__name__)
app.logger.debug('A called')
@app.route('/')
def index():
	return 'alexa solar pm working working!'
if __name__ == "__main__":
	app.logger.debug('A main called')
	app.run(debug=True)
