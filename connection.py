pool = dict()

import imaplib
import base64
import email


def create_connection(user, password, host, port):
    imap_connection = imaplib.IMAP4_SSL(host, port)
    imap_connection.login(user, password)
    return imap_connection


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

# email_user = "test@gorzala.de"
# email_pass = "RniS09bu3a89u1iS"
#
# mail = imaplib.IMAP4_SSL("mail.your-server.de", 993);
# mail.login(email_user, email_pass)
# mail.select()
#
# result, data = mail.search(None, 'ALL');
# print("Result: " + str(("OK" == result)) + " - " + result)
# print("Data: " +str (data))
# print("Data0: " + str(data[0]))
# numbers = data[0].split()
# print("Numberds: " + str(numbers))
# mail_ids = data[0]
# id_list = mail_ids.split()
#
# for item in numbers:
#     print("type: " + str(type(item)))
#     print(" val: " + str(item))
#     res = mail.copy(item, "INBOX.foo")
#     print("On copy: " + str(res))


# for mail_id in id_list:
#     print ("-" * 100)
#     print(int(mail_id))
#     result, data = mail.fetch(mail_id, '(RFC822)')
#     raw_email = data[0][1]
#     email_message = email.message_from_bytes(raw_email)
#     print(email_message)
#     print("#" * 100)
#     print(str(email_message))


# res = mail.list()
# print("List result: " + str(res))


# res = mail.create("INBOX.foo")
# print("create resul: " + str(res))
