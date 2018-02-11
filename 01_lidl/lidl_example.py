from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")


# logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def invoke():
    # welcome_msg = render_template('welcome')

    return question('What kind of dinner do you want?')


@ask.intent('RomanticIntent')
def romantic():
    return question('Do you want to have a vegetarian dinner?')


@ask.intent("AMAZON.StopIntent")
def stop():
    return statement('Bye')


if __name__ == '__main__':
    app.run(debug=True)
