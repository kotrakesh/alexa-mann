from flask import Flask
app.logger.debug('A called')
app = Flask(__name__)
@app.route('/')
def index():
	return 'alexa solar pm working working!'
if __name__ == "__main__":
	app.logger.debug('A main called')
	app.run(debug=True)
