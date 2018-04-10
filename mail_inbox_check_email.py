import email
import imaplib
from bs4 import BeautifulSoup
import os
import mimetypes

username = '***'
password = '***'
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(username, password)

mail.select('inbox')

# Create folder
# mail.create('Item2')

# list of folders
# mail.list()

result, data = mail.uid('search', None, 'ALL')
inbox_item_list = data[0].split()
most_recent = inbox_item_list[-1]
oldest = inbox_item_list[0]

for item in inbox_item_list:
    result2, email_data = mail.uid('fetch', oldest, '(RFC822)')
    raw_email = email_data[0][1].decode('utf-8')
    email_message = email.message_from_string(raw_email)
    to_ = email_message['To']
    from_ = email_message['From']
    subject_ = email_message['Subject']
    date_ = email_message['data']
    email_message.get_payload()
    counter = 1
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        filename = part.get_filename()
        content_type = part.get_content_type()
        if not filename:
            ext = mimetypes.guess_extension(content_type)
            if not ext:
                ext = '.bin'
            if 'text' in content_type:
                ext = '.txt'
            elif 'html' in content_type:
                ext = '.html'
            filename = 'msg-part-%08d%s' % (counter, ext)
        counter += 1
    with open(os.path.join(os.getcwd(), filename), 'wb') as fp:
        fp.write(part.get_payload(decode=True))
    if 'plain' in content_type:
        html_ = part.get_payload()
        soup = BeautifulSoup(html_, 'html.parser')
        text = soup.get.text()
        print(text)
    else:
        pass
