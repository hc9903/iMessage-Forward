import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

def remove_unwanted_chars(text):
    return re.sub(r'^�?[\x00-\x7F]+', '', text)

# Import the iMessage script
from imessage_tools import read_messages

# Database location
db_location = "/Users/XXX/Library/Messages/chat.db"
# The number of messages you want to read at a time
num_messages = 10
# Your number in iMessage
self_number = 'Me'

# Function to get already forwarded messages
def get_forwarded_messages():
    conn = sqlite3.connect('imessage_forwarder/forwarded_messages.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS forwarded(rowid INTEGER)')
    conn.commit()
    cursor.execute('SELECT rowid FROM forwarded')
    return [row[0] for row in cursor.fetchall()]

# Function to add a message to the forwarded messages
def add_forwarded_message(rowid):
    conn = sqlite3.connect('imessage_forwarder/forwarded_messages.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO forwarded(rowid) VALUES (?)', (rowid,))
    conn.commit()

# Get the messages from iMessage
messages = read_messages(db_location, n=num_messages, self_number=self_number)

# Get the already forwarded messages
forwarded_messages = get_forwarded_messages()

# Filter the messages to get only the ones not already forwarded
messages_to_forward = [message for message in messages if message['rowid'] not in forwarded_messages]

# Set up the email
email = 'your email address'
password = 'your email password'
smtp_server = 'smtp.163.com'
smtp_port = '25'

# Send the messages
for message in messages_to_forward:
    message['body'] = remove_unwanted_chars(message['body'])
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'iMessage Forward'
    body = f"RowID: {message['rowid']}\nBody: {message['body']}\nPhone Number: {message['phone_number']}\nIs From Me: {message['is_from_me']}\nCache Roomname: {message['cache_roomname']}\nGroup Chat Name: {message['group_chat_name']}\nDate: {message['date']}\n"
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, text)
    server.quit()
    
    # Add the message to the forwarded messages
    add_forwarded_message(message['rowid'])
