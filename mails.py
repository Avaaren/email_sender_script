from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = ''
PASSWORD = ''

# Get contacts from file and return 2 arrays
def get_contacts(filename):
    names = []
    emails = []

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            names.append(line.split()[0])
            emails.append(line.split()[1])
        return names, emails

# Get email template from file
def get_template(filename):
    with open(filename, 'r', encoding='utf-8') as template:
        template_content = template.read()
    return Template(template_content)


def main():
    # Connecting to yandex
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.set_debuglevel(1)
    server.ehlo(MY_ADDRESS) 
    # server.starttls()
    server.login(MY_ADDRESS, PASSWORD)
    # Getting data from files
    names, emails = get_contacts('contacts.txt')  # read contacts
    message_template = get_template('message.txt')

    # for every name and email in array
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="This is TEST"

        # add in the message body
        # We can attach files if we need it
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        server.send_message(msg)
        
        del msg
    server.quit()
    
if __name__ == '__main__':
    main()