import imaplib
import email

pool = dict()

def create_connection(user, password, host, port):
    imap_connection = imaplib.IMAP4_SSL(host, port)
    imap_connection.login(user, password)
    return imap_connection

def move_mail(source, destination):
    print(f"Moving from: {source} to: {destination}");


def move_to_folder(connection, mail_id, folder):
    print("Moving: " + str(mail_id))
    res, data = connection.uid('copy', mail_id, folder)
    if "OK" == res:
        print("Now delete")
        res = connection.uid('store', mail_id, '+FLAGS', '\\Deleted')
        connection.expunge()
        print(str(res))
    else:
        print("Copy failed!")


def get_subject(mail):
    res = str(email.header.make_header(email.header.decode_header(mail['subject'])))
    return res


def get_from(mail):
    return mail['from']


def get_to(mail):
    return mail['to']


def get_cc(mail):
    if mail['cc']:
        return mail['cc']
    else:
        return ""


def get_mail_by_id(connection, mail_id):
    print("Getting mail with id: " + str(mail_id))
    result, data = connection.uid('fetch', mail_id, '(BODY.PEEK[])')
    raw_email = data[0][1]
    #    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_bytes(raw_email)
    return email_message
