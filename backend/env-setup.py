from getpass import getpass
import secrets


if __name__ == '__main__':
    with open('.env.template', mode='r') as template_file, open('.env', mode='w') as env_file:
        print('This script will create a .env file.')

        print('\nPlease enter MongoDB Atlas connection information:')
        mongodb_username = getpass('MongoDB Username: ')
        mongodb_password = getpass('MongoDB Password: ')
        mongodb_cluster_address = getpass('MongoDB Cluster Address: ')

        print('\nA Flask secret key will be generated using secrets.token_hex().')
        flask_secret_key = secrets.token_hex()

        file_data = template_file.read()

        file_data = file_data.replace('<mongodb-username>', f'"{mongodb_username}"')
        file_data = file_data.replace('<mongodb-password>', f'"{mongodb_password}"')
        file_data = file_data.replace('<mongodb-cluster-address>', f'"{mongodb_cluster_address}"')
        file_data = file_data.replace('<flask-secret-key>', f'"{flask_secret_key}"')

        env_file.write(file_data)
