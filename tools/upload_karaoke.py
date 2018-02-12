import requests
import json
import httplib2, mimetypes
import os

from subprocess import Popen, PIPE


class Token:
    token_type = ''
    access_token = ''

    def __init__(self, data):
        self.token_type = data['token_type']
        self.access_token = data['access_token']

    def __str__(self):
        return '{} {}'.format(self.token_type, self.access_token)

    def token(self):
        return '{} {}'.format(self.token_type, self.access_token)


class Backtory:
    Storage_Id = '5a34d4a5e4b01a2810f0912b'
    Authentication_Id = '5a34d47de4b01a2810f08fce'
    Authentication_Key = '1c9354b1cd804420ab72a33c'
    token = ''

    def get_master_token(self):
        url = 'https://api.backtory.com/auth/login'
        headers = {
            'X-Backtory-Authentication-Id': self.Authentication_Id,
            'X-Backtory-Authentication-Key': self.Authentication_Key
        }
        response = requests.post(url=url, headers=headers)

        if response.status_code != 200:
            raise Exception('ERROR in get_master_token: Status Code is not 200')
        try:
            data = json.loads(response.content.decode('utf-8'))
        except:
            raise Exception('ERROR in get_master_token: Can not load the content')

        self.token = Token(data=data)

    def upload_file(self):
        try:
            self.get_master_token()
        except:
            print("Can't get the Master Token")
            return -1

        file = '/Users/pezzati/Desktop/job/Hootan/Project/musikhar/tools/test.jpg'
        path = '/path1/path2/'

        process = Popen(['tools/to_backtory.sh', self.token.access_token, self.Storage_Id, file, path], stdout=PIPE, stderr=PIPE)
        process.wait()
        for line in process.stdout.readlines():
            print(line)
        print('errors')
        for line in process.stderr.readlines():
            print(line)
        print('done')

    def send_post(self):
        url = 'https://storage.backtory.com/files'
        headers = {'X-Backtory-Storage-Id': self.Storage_Id}
        requests.post(url=url)

        # command = 'curl -X POST  --header "X-Backtory-Storage-Id: 5a34d4a5e4b01a2810f0912b" '
        # command += '--form fileItems[0].fileToUpload=@"/path/to/file1.txt" '
        # command += '--form fileItems[0].path="/path1/path2/" '
        # command += '--form fileItems[0].replacing=true '
        # command += '--form fileItems[1].fileToUpload=@"/path/to/file2.txt" '
        # command += '--form fileItems[1].path="/path1/path3/" '
        # command += '--form fileItems[1].replacing=true '
        # command += 'http://storage.backtory.com/files'
