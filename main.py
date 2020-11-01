import yaml
import connection


def get_config(file_name):
    with open(file_name, "r") as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)


def __get_connection_for_folder__(config, folder):
    imap_connection_id = folder.split("/")[0]
    if imap_connection_id in connection.pool:
        return connection.pool[imap_connection_id]
    else:
        connection.pool[imap_connection_id] = __create_connection_from_config__(
            config['imap_accounts'][imap_connection_id])
        return connection.pool[imap_connection_id]


def __create_connection_from_config__(server_config):
    return connection.create_connection(server_config['user_name'],
                                        server_config['user_pass'],
                                        server_config['host_name'],
                                        server_config['port'])


def __get_messages_from_folder__(config, folder_string):
    imap_connection = __get_connection_for_folder__(config, folder_string)
    server_id, folder = folder_string.split("/", 1)
    imap_connection.select(folder)
    result, data = imap_connection.uid('search', None, 'ALL');
    return data[0].split()


def invoke_rules(config):
    for folder in config['folders']:
        print("Processing Folder: " + folder['name'])
        all_messages_in_folder = __get_messages_from_folder__(config, folder['name'])
        for message_id in all_messages_in_folder:
            imap_connection = __get_connection_for_folder__(config, folder['name'])
            mail_message = connection.get_mail_by_id(imap_connection, message_id)
            print(connection.get_subject(mail_message))
            for rule in folder['rules']:
                predicate = rule['predicate']
                action = rule['action']
                if eval(predicate):
                    print("Match!")
                    eval(action)


if __name__ == '__main__':
    config = get_config("marc@becheftigt.de.yaml")
    invoke_rules(config)
    for folder in connection.pool:
        conn = connection.pool[folder]
        conn.close()
        conn.logout()
