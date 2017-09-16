from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")


# logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def invoke():
    msg = render_template('welcome')

    return question(msg)


@ask.intent('DinnerIntent')
def dtone():

    msg = render_template('dinnertype1')

    return question(msg)

@ask.intent('RomanticIntent')
def dttwo():

    msg = render_template('dinnertype2')

    return question(msg)

@ask.intent('VegetarianIntent')
def dtthree():

    msg = render_template('dinnerproposal1')

    return question(msg)

@ask.intent('WineIntent')
def dtwine():

    msg = render_template('wineproposal1')

    return question(msg)

@ask.intent('ConfirmwineIntent')
def dtconf():

    msg = render_template('anythingelse')

    return question(msg)

@ask.intent('CompletedIntent')
def dtone():

    msg = render_template('prepared')

    return question(msg)



@ask.intent("AMAZON.StopIntent")
def stop():
    return statement('Bye')


if __name__ == '__main__':
    app.run(debug=True)
