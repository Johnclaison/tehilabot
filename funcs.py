from db_conn import getSuppliers, getProduct
import urllib2, urllib
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import random
import re
menu = ['1','2','3','4','search products','list of suppliers','about us','register']
about = ['''
*What we really do?*

Tehila Pharmaceuticals is based in Harare, Zimbabwe. We have a network of pharmaceuticals
manufactures across the globe and wide range of in-house stocks at our premises which
enables us to rapidly respond to the health care needs at all levels from all the smallest local
medical facilities to projects at national level.

*Our Vision*

Healthy communities in Zimbabwe and
beyond sustained through guaranteed access to quality, affordable and effective
heath care products.

*Our Mission*

To provide quality, affordable, effective
and accessible medicines, consumables, medical equipment and allied
products.
https://tehilapharma.com/about-us/
''']

#CHECK TO SEE IF THE MESSAGE IF IN MENU LIST.
def mainMenu(sms, number):
    path='https://tehilapharma.com/tehilabot/query.php'
    replay = ''
    if sms in menu[0:]:
        if sms == '1' or sms == menu[4]:
            replay = 'What`s the name of the product that you want me to search for you?\nType *`search product name`*'
        elif sms == '2' or sms == menu[5]:
            replay = getSuppliers()
        elif sms == '3' or sms == menu[6]:
            replay = random.choice(about)
        elif sms == '4' or sms == menu[7]:
            replay = 'I`m not registering new users at the moment but you can visit https://tehilapharma.com/my-account/ and register'
    return replay

#CHECK TO SEE IF THE MESSAGE IS A PRODUCT OR NOT.
def getProduct(search):
    path='https://tehilapharma.com/tehilabot/query.php'
    data = search.replace('search ', '')
    search = [('caption','{}'.format(data))]
    search = urllib.urlencode(search)
    req = urllib2.Request(path, search)
    page = urllib2.urlopen(req).read()
    return str(page)

def getProductImage(searchImg):
    data = searchImg.replace('search ', '')
    path='https://tehilapharma.com/tehilabot/query.php'
    search = [('image',''+data+ '')]
    search = urllib.urlencode(search)
    req = urllib2.Request(path, search)
    page = urllib2.urlopen(req).read()
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', page)
    image= random.choice(urls)
    return(image)
