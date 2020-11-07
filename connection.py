import imaplib
import email

pool = dict()

def create_connection(user, password, host, port):
    imap_connection = imaplib.IMAP4_SSL(host, port)
    imap_connection.login(user, password)
    return imap_connection

def __get_connection_for_folder__(config, folder):
    imap_connection_id = folder.split("/")[0]
    if imap_connection_id in pool:
        return pool[imap_connection_id]
    else:
        pool[imap_connection_id] = __create_connection_from_config__(
            config['imap_accounts'][imap_connection_id])
        return pool[imap_connection_id]


def __create_connection_from_config__(server_config):
    return create_connection(server_config['user_name'],
                             server_config['user_pass'],
                             server_config['host_name'],
                             server_config['port'])

def move_mail(raw_message, destination):
    print("+"*100)
    subject = get_subject(email.message_from_bytes(raw_message))
    print(f"Current pool: {pool}")
    print(f"Moving \"{subject}\" from to: {destination}!!!!!!!");
    server_id, folder = extract_server_and_folder(destination)
    print(f"To server: {server_id} and folder: {folder}")
    connection = pool[server_id]
    print("Using connection: " + str(connection))

    res, data = connection.append(folder, None, None, raw_message)
    if "OK" == res:
        print("")
    print(pool)


def extract_server_and_folder(destination):
    return destination.split("/", 1)


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

def get_raw_message(connection, mail_id):
    print("Getting mail with id: " + str(mail_id))
    result, data = connection.uid('fetch', mail_id, '(BODY.PEEK[])')
    return data[0][1]


def get_mail_by_id(connection, mail_id):
    email_message = email.message_from_bytes(get_raw_message(connection, mail_id))
    return email_message
