import imaplib_connect
from base64 import b64encode
import re

# obtener regex y email emisor
archivo = open("regexAndEmail.txt","r")
emailFrom = (archivo.readline()).replace("\n","")
regex = (archivo.readline()).replace("\n","")
date = archivo.readline()
archivo.close()

# abre la conexion
with imaplib_connect.open_connection() as c:
    c.select('INBOX')
    tmp, data = c.search(None, 'FROM '+'"'+emailFrom+'"')
    for num in data[0].split():
        #obtenemos el message ID 
        tmp, data = c.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
        print("message: {0}".format(num))

        #se obtiene el messageId primero pasandolo de byte a string 
        # y despues quitandole los caracteres que no pertenecen al message id 
        msgId = data[0][1].decode('UTF-8')
        msgId = (msgId[12:]).replace("<","")
        msgId = msgId.replace(">","")
        msgId = (msgId.replace("\n","")).replace("\r","")
        
        if re.search(regex, msgId):
            print("correo con message ID: \n"+msgId+"\n veridico.\n")
        else:
            print("correo con message ID: \n"+msgId+"\n es FALSO.\n")
    print("Message Id comprobado desde último correo enviado el: "+date)