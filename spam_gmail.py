# Import statements
import smtplib
from email.message import EmailMessage
import random
import time
import getpass
import sys
import os
from turtle import bgcolor
import requests
try:
    from tabulate import tabulate
except ModuleNotFoundError:
    table = False
else:
    table = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    loadingBar = False
else:
    loadingBar = True

# Colour Scheme

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    #-----
    ITALIC   = '\33[3m'
    URL      = '\33[4m'
    BLINK    = '\33[5m'
    BLINK2   = '\33[6m'
    SELECTED = '\33[7m'

    BLACK  = '\33[30m'
    RED    = '\33[31m'
    GREEN  = '\33[32m'
    YELLOW = '\33[33m'
    BLUE   = '\33[34m'
    VIOLET = '\33[35m'
    BEIGE  = '\33[36m'
    WHITE  = '\33[37m'

    BLACKBG  = '\33[40m'
    REDBG    = '\33[41m'
    GREENBG  = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG   = '\33[44m'
    VIOLETBG = '\33[45m'
    BEIGEBG  = '\33[46m'
    WHITEBG  = '\33[47m'

    GREY    = '\33[90m'
    BEIGE2  = '\33[96m'
    WHITE2  = '\33[97m'

    GREYBG    = '\33[100m'
    REDBG2    = '\33[101m'

# Functions

def checkInternet():
    url = "https://www.google.com"
    timeout = 10
    try:
        request = requests.get(url,timeout=timeout)
        status = 1
    except (requests.ConnectionError,requests.Timeout) as exception:
        status = 0
    return status

def validRecipientNum(to_addr,recipientNum):
    valid = False
    while not valid:
        message = False
        if recipientNum > 0:
            if recipientNum <= 500:
                valid = True
            else:
                message = True
        else:
            message = True
        if message:
            print (bcolors.FAIL + "Invalid number of recipients! You must start over.\n" + bcolors.ENDC)
            time.sleep(0.5)
            to_addr = []
            while True:
                addr = input(bcolors.OKGREEN + "Recipient(s) # hit enter to finish: " + bcolors.ENDC)
                if not addr:
                    break
                else:
                    to_addr.append(addr)
            recipientNum = len (to_addr)
            valid = False
    return to_addr,recipientNum

def validSend(send,recipientNum,numOfSenders):
    valid = False
    while not valid:
        message = False
        try:
            int (send)
        except ValueError:
            message = True
        else:
            send = int (send)
            if send > 0:
                if send % recipientNum == 0:
                    if (send * recipientNum) < (500 * numOfSenders):
                        valid = True
                    else:
                        message = True
                else:
                    time.sleep(0.5)
                    send = input(bcolors.FAIL + "Number of emails: " + bcolors.ENDC)
                    valid = False
            else:
                message = True
        if message:
            time.sleep(0.5)
            send = input(bcolors.FAIL + "Number of emails: " + bcolors.ENDC)
            valid = False
    return send

def validSpeed(s):
    valid = False
    while not valid:
        try:
            float (s)
        except ValueError:
            print (bcolors.FAIL + "Invalid number for speed!" + bcolors.ENDC)
            time.sleep(0.5)
            s = input(bcolors.FAIL + "Interval (seconds): " + bcolors.ENDC)
        else:
            s = float (s)
            valid = True
    return s

def validGmail(from_addr,cipher):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # Start TLS for security
    server.starttls()
    try:
        server.login(from_addr, cipher)
        server.quit()
    except smtplib.SMTPAuthenticationError:
        print(bcolors.FAIL + "\nThe email / password you have entered is incorrect! Try again" + bcolors.ENDC)
        valid = False
    else:
        valid = True
    return valid

# Surpass Limit with multiple emails (Gmail)
def gMultiple():
    global emailnum
    global passnum
    try:
        file = open("gmail.txt", "r")
        fileStuff = file.readline()
        gmail = fileStuff.split(",")
        emailnum += 1
        from_addr = gmail[emailnum]
        numOfSenders = len (gmail)
        if gmail[-1] == "\n" or gmail[-1] == "":
            numOfSenders -= 1
        passFile = open("gmailpass.txt", "r")
        passFileStuff = passFile.readline()
        passThing = passFileStuff.split(",")
        passnum += 1
        cipher = passThing[passnum]
        file.close()
    except IOError:
        print ("gmailpass.txt or gmail.txt not found! Exiting...")
        sys.exit()

    return from_addr,cipher,numOfSenders

# Send with limits (Gmail)
def gSingle():
    valid = False
    while not valid:
        from_addr = input(bcolors.OKGREEN + 'Your Google Email: ' + bcolors.ENDC)
        cipher = getpass.getpass(bcolors.OKGREEN + 'Password:' + bcolors.ENDC)
        valid = validGmail(from_addr,cipher)
    numOfSenders = 1
    return from_addr,cipher,numOfSenders

# Main structure (subject, body, etc.)
def structure(numOfSenders):
    to_addr = []
    addr = ""
    number = random.randint(0, 10000)
    while True:
        addr = input(bcolors.OKGREEN + "Recipient(s) # hit enter to finish: " + bcolors.ENDC)
        if not addr:
            break
        else:
            to_addr.append(addr)
    recipientNum = len (to_addr)
    to_addr,recipientNum = validRecipientNum(to_addr,recipientNum)
    send = input(bcolors.FAIL + "Number of emails: " + bcolors.ENDC)
    send = validSend(send,recipientNum,numOfSenders)
    try:
        p_reader = open("subject.txt", 'r')
        subject = p_reader.readline()
        index = len(subject) - 1
        subject = subject[0:index]
        p_reader.close()
        length = len (subject)
        subject += ' (' + str(number) + ')'
        f = open("body.txt", "r")
        body = f.read()
        f.close()
    except IOError:
        print ("body.txt or subject.txt not found! Exiting...")
        sys.exit()
        
    speed = input(bcolors.FAIL + "Interval (seconds): " + bcolors.ENDC)
    speed = validSpeed(speed)

    print(bcolors.WARNING + "Email Sending...." + bcolors.ENDC)
    time.sleep(1)
    return speed,to_addr,body,subject,length,recipientNum,send

# Main Spammer (Gmail)
def gmailSpam(speed,from_addr,to_addr,body,subject,length,cipher,recipientNum):
        global sent
        global Sent
        number = random.randint(0, 10000)
        subject = subject[0:length] + " (" + str(number) + ")"
        # Construct email
        msg = EmailMessage()
        msg.add_header('From', from_addr)
        msg.add_header('To', ', '.join(to_addr))
        msg.add_header('Subject', subject)
        msg.set_payload(body)
        # Connect
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # Start TLS for security
        server.starttls()
        try:
            server.login(from_addr, cipher)
            server.send_message(msg, from_addr=from_addr, to_addrs=to_addr)
            server.quit()
            sent += (1*recipientNum)
            Sent += (1*recipientNum)
            time.sleep(speed)
        except smtplib.SMTPAuthenticationError:
            print(bcolors.FAIL + "\nThe email / password you have entered is incorrect! Exiting..." + bcolors.ENDC)
            sys.exit()
        except smtplib.SMTPRecipientsRefused:
            print(bcolors.FAIL + "\nThe recipient's email adress is invalid! Exiting..." + bcolors.ENDC)
            sys.exit()

# Main Program
try:
    sent = 0
    Sent = 0
    emailnum = -1
    passnum = -1

    internet = checkInternet()

    if internet==1:
        from_address,password,numOfSenders = gMultiple()
        sendSpeed,to_address,body,subject,length,recipientNum,send = structure(numOfSenders)
        if loadingBar and send != float ("inf"):
            pbar = tqdm(total=(send/recipientNum))
        elif table and recipientNum <= 2:
            print (tabulate([[from_address,to_address,Sent]], headers=["From:", "To:","Sent:"], tablefmt="github"))
        else:
            print ("\nFrom:",from_address,"\tTo:",to_address,"\tSent:",Sent)
        spam = True
        while spam is True and Sent < send:
            if from_address == "" or from_address == "\n":
                spam = False
            else:
                try:
                    gmailSpam(sendSpeed,from_address,to_address,body,subject,length,password,recipientNum)
                    if loadingBar and send != float ("inf"):
                        pbar.update(1)
                    elif table and recipientNum <= 2:
                        print (tabulate([[from_address,to_address,Sent]], headers=["     ","   ","     "], tablefmt="github"))
                    else:
                        print ("\nFrom:",from_address,"\tTo:",to_address,"\tSent:",Sent)
                except smtplib.SMTPSenderRefused:
                    print ("Limit reached. Switching emails...")
                    from_address,password,numOfSenders = gMultiple()
                    spam = True
                    sent = 0
                except smtplib.SMTPDataError:
                    print ("Limit reached. Switching emails...")
                    from_address,password,numOfSenders = gMultiple()
                    spam = True
                    sent = 0
                if sent == 500:
                    from_address,password,numOfSenders = gMultiple()
                    spam = True
                    sent = 0
        if loadingBar and send != float ("inf"):
            pbar.close()
    else:
        print(bcolors.FAIL + "No internet connection, try again later." + bcolors.ENDC)
except KeyboardInterrupt:
    print(bcolors.FAIL + "\nQuit" + bcolors.ENDC)
    sys.exit()

# Add an option to give a submenu to user to choose from predefined recipient list
