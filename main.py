from flask import Flask, request, session 
from twilio.twiml.messaging_response import MessagingResponse
from configparser import ConfigParser
from funcs import mainMenu, getProduct, getProductImage
from db_conn import getUsers
import random

parser = ConfigParser()
parser.read('./utility_methods/config.ini')
symbols = ['!','?','.','*','-','_']

possibleGreetings = [
    'hie','hi','just going to say hi','heya','hello hi','howdy','hey there','hi there','greetings','hey','long time no see',
    'hello','lovely day isn`t it','I greet you','hello again','hello there','a good day','good day']
greetingResponse = [
'''*Welcome to Tehila Pharmaceuticals*\n
Get the best deals, everything you need, All in one play.\n
Type *menu* to see what I can help you with.
https://tehilapharma.com/
    '''
    ]
menuList = [
    'I didn`t get that. Can you say it again?',
    'I missed what you said. What was that?',
    'Sorry, could you say that again?',
    'Sorry, can you say that again?',
    'Can you say that again?',
    'Sorry, I didn`t get that. Can you rephrase?',
    'Sorry, what was that?',
    'One more time?',
    'What was that?',
    'Say that one more time?',
    'I didn`t get that. Can you repeat?',
    'I missed that, say that again?'
]

defaultResponse = ['''
_*Select an option by typing a number or name of that option*_\n
1) Search Products
2) List of suppliers
3) About Us
4) Register
''']

customerList = ['+263785858682']

#APP INITIALISATION.
app = Flask(__name__)

#CHECKING FOR MATCHES.
def inList(message, possibleGreetings):
    match = False
    if message in possibleGreetings[0:]:
        match = True
    return match

#PROCESS ALL REQUESTS.
def process(message, number):
    fallBack = message
    #CHECKS TO SEE IF WE RECIEVED A MESSAGE WITH TEXT.
    if message == 'None':
        fallBack = ''
    elif 'whatsapp:' in number:
        number = number.replace('whatsapp:', '')

    #REMOVING PANCTUATIONS.
    for i in symbols:
        fallBack = fallBack.replace(i, '')

    response = 0
    #0: We are checking through chatBot for matches.
    #1: We didn't anything in the chatBot.
    #2: We did find something in the chatBot.
    i = 0
    #------------ Checking for matches -----------
    while response == 0:
        if inList(fallBack.lower(), possibleGreetings):
            response = 2
            if getUsers(number, fallBack):
                fallBack = getUsers(number, fallBack)
            else:
                fallBack = random.choice(greetingResponse)
        elif mainMenu(fallBack.lower(), number):
            response = 2
            fallBack = mainMenu(fallBack.lower(), number)
        i += 1
        if (i*2) == len(possibleGreetings) and response == 0:
            response = 1

    #------------ Default response ---------------
    if response == 1:
        fallBack = random.choice(defaultResponse)

    return fallBack

#APPICATION STARTS
@app.route('/', methods=['GET', 'POST'])
def recieve_sms():
    message = str(request.form.get('Body'))
    client = str(request.form.get('From'))
    resp = MessagingResponse()
    message = message.lower()
    if 'search' in message:
        msg = resp.message(getProduct(message))
        msg.media(getProductImage(message.lower()))
        return str(resp)
    else:
        resp.message(process(message, client))
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)