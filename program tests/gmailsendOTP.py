import random
import smtplib

OTP = random.randint(100000,999999)      #generating a randomm 6-digit OTP

#setting up server
server = smtplib.SMTP('smtp.gmail.com',587)
#server = smtplib.SMTP('64.233.184.108',587)           #IP address of smtp.gmail.com to bypass DNS resolution
server.starttls()

receiver_email = "santhosh18412@gmail.com"


# password = "stqqwjqoocucknsx"
# server.login("priyanshu25122002@gmail.com",password)

password = "succyohrfxgyuhdv"
server.login("santhoshvaraprasad.u@gmail.com",password)

body = "OTP working"
subject = "OTP verification using python"
message = f'subject:{subject}\n\n{body}'

server.sendmail("priyanshu25122002@gmail.com",receiver_email,message)


print("OTP has been sent to "+receiver_email)


server.quit()


# import base64
# from email.mime.text import MIMEText
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from requests import HTTPError

# SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
# flow = InstalledAppFlow.from_client_secrets_file('credentails.json', SCOPES)
# creds = flow.run_local_server(port=0)

# service = build('gmail', 'v1', credentials=creds)
# message = MIMEText('This is the body of the email')
# message['to'] = 'recipient@gmail.com'
# message['subject'] = 'Email Subject'
# create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

# try:
#     message = (service.users().messages().send(userId="me", body=create_message).execute())
#     print(F'sent message to {message} Message Id: {message["id"]}')
# except HTTPError as error:
#     print(F'An error occurred: {error}')
#     message = None
