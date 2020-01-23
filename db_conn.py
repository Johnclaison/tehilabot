import urllib2, urllib
from twilio.twiml.messaging_response import MessagingResponse

path='https://tehilapharma.com/tehilabot/query.php'    #the url you want to POST to

#GET DATABASE CONNECTION.
def dbConn():
    pass

def getUsers(number, fallBack):
    #search = [('user','{}'.format(number))]
    #search = urllib.urlencode(search)
    #req = urllib2.Request(path, search)
    #page = urllib2.urlopen(req).read()
    #return str(page)
    pass

#SET USER IN THE DATABASE.
def setUser():
    pass

#GET LIST OF SUPPLIERS.
def getSuppliers():
    mydata=[('suplier','list suppliers')]    #The first is the var name the second is the value
    mydata=urllib.urlencode(mydata)
    req=urllib2.Request(path, mydata)
    page=urllib2.urlopen(req).read()
    return str('*Here is the list of Tehila Pharmaceuticals Suppliers*\n\n{}'.format(page))

def getProduct(product):
    return product

#CREAT TABLE.
def createTable():
    cursor.execute('CREATE TABLE IF NOT EXISTS users(phone TEXT, name TEXT)')
    #setUser()
    getUsers(number, sms)
