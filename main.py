import yaml
import connection


def get_config(file_name):
    with open(file_name, "r") as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)

def __get_messages_from_folder__(config, folder_string):
    imap_connection = connection.__get_connection_for_folder__(config, folder_string)
    server_id, folder = folder_string.split("/", 1)
    imap_connection.select(folder)
    result, data = imap_connection.uid('search', None, 'ALL');
    return data[0].split()


def invoke_rules(config):
    for folder in config['folders']:
        print("Processing Folder: " + folder['name'])
        all_messages_in_folder = __get_messages_from_folder__(config, folder['name'])
        for message_id in all_messages_in_folder:
            imap_connection = connection.__get_connection_for_folder__(config, folder['name'])
            raw_message = connection.get_raw_message(imap_connection, message_id)
            print("Type of raw message: " + str(type(raw_message)))
            mail_message = connection.get_mail_by_id(imap_connection, message_id)
            print(connection.get_subject(mail_message))
            for rule in folder['rules']:
                predicate = rule['predicate']
                action = rule['action']
                if eval(predicate):
                    print("Match!")
                    eval(action)

def init_connections(config):
    for imap_account in config['imap_accounts']:
        account_name = str(imap_account)
        print(f"Initialiszing: {account_name}")
        if not account_name in connection.pool:
            print(f"Adding {account_name}")
            connection.pool[account_name] = connection.__create_connection_from_config__(config['imap_accounts'][imap_account])

if __name__ == '__main__':
    config = get_config("marc@becheftigt.de.yaml")
    init_connections(config)
    invoke_rules(config)
    print(connection.pool)
    for folder in connection.pool:
        conn = connection.pool[folder]
        try:
            conn.close()
            conn.logout()
        except:
            pass
