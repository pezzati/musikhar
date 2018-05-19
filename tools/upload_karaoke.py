import requests
import json
import csv
from pathlib import Path
from subprocess import Popen, PIPE

from django.conf import settings
from django.utils import timezone


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
    bucket_name = 'cantotest'
    address = 'http://storage.backtory.com/cantotest'
    cached_files = {}


    def get_master_token(self):
        if self.token:
            return
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

    def get_dir_info(self, path):
        if path in self.cached_files and self.cached_files[path]:
            return self.cached_files[path]
        headers = {
            'Authorization': 'Bearer {}'.format(self.token.access_token),
            'X-Backtory-Storage-Id': self.Storage_Id,
            'Content-Type': 'application/json'
                   }
        url = 'http://storage.backtory.com/files/directoryInfo'
        data = {'url': path, "pageNumber": 0, "pageSize": 50, "sortingType": "ASC"}
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        res_data = json.loads(res.content.decode('utf-8'))
        files = [x['url'] for x in res_data.get('files')]
        self.cached_files[path] = files
        return self.cached_files[path]

    def get_file_info(self, path, file):
        if not isinstance(file, str):
            file = str(file)
        headers = {
            'Authorization': 'Bearer {}'.format(self.token.access_token),
            'X-Backtory-Storage-Id': self.Storage_Id,
            'Content-Type': 'application/json'
        }
        url = 'http://storage.backtory.com/files/fileInfo'
        path += file.split('/')[-1]
        path = path.replace('//', '/')
        data = {'url': path}
        print('get file info: {}'.format(path))
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        if res.status_code == 200:
            print('HIT')
            return True
        print('MISS')
        return False

    def gen_multi_part_post_comm(self, file, path):
        command = 'curl -X POST --header "Authorization: Bearer {}" '.format(self.token.access_token)
        command += '--header "X-Backtory-Storage-Id: {}" '.format(self.Storage_Id)
        command += '--form fileItems[0].fileToUpload=@"{}" '.format(file)
        command += '--form fileItems[0].path="{}" '.format(path)
        command += '--form fileItems[0].replacing=true http://storage.backtory.com/files'
        return command

    # def check_file_exists(self, path, file):
    #     files = self.get_dir_info(path=path)
    #     for dir_file in files:
    #         if dir_file.endswith(file):
    #             return dir_file
    #     return False

    def upload_file(self, file='', path=''):
        try:
            self.get_master_token()
        except:
            raise Exception("Can't get the Master Token")

        if not file:
            file = '/Users/pezzati/Desktop/job/Hootan/Project/musikhar/tools/test.jpg'
        if not path:
            path = '/path1/path2/'

        # dir = self.check_file_exists(path=path, file=file.split('/')[-1])
        if self.get_file_info(path=path, file=file):
            d = '/{}/{}'.format(path, str(file).split('/')[-1]).replace('//', '/')
            return json.dumps({'savedFilesUrls': [d]}).encode('utf-8'), ''

        process = Popen(self.gen_multi_part_post_comm(file=file, path=path), stdout=PIPE, stderr=PIPE, shell=True)
        (out, err) = process.communicate()
        # if self.get_file_info(path=path, file=file):
        #     d = '/{}/{}'.format(path, file.split('/')[-1]).replace('//', '/')
        #     return json.dumps({'savedFilesUrls': [d]}).encode('utf-8'), ''
        return out, err

    @staticmethod
    def _remove_space(val):
        try:
            while val and val[0] == ' ':
                val = val[1:]
            return val
        except Exception as e:
            print('remove space')
            print(val)
            raise e

    def read_file(self, name, directory=None):
        try:
            self.get_master_token()
        except:
            raise Exception("Can't get the Master Token")
        if name[-4:] != '.csv':
            name += '.csv'
        if directory:
            source_path = '{}/{}'.format(directory, name).replace('//', '/')
            target_path = '{}/new_{}'.format(directory, name).replace('//', '/')
            error_path = '{}/error_{}'.format(directory, name).replace('//', '/')
        else:
            source_path = '{}'.format(name).replace('//', '/')
            target_path = 'new_{}'.format(name).replace('//', '/')
            error_path = 'error_{}'.format(name).replace('//', '/')

        rows = []
        with open(source_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            # fieldnames = reader.fieldnames
            fieldnames = ['name', 'description', 'cover_photo', 'tags', 'genre', 'file', 'full_file', 'artist', 'lyric', ' lyric_poet', ' lyric_name', ' error']
            i_row = 0
            for row in reader:
                i_row += 1
                j_in_row = 0
                for k in row:
                    j_in_row += 1
                    try:
                        row[k] = self._remove_space(row[k])
                    except Exception as e:
                        print('i: {}, j: {}'.format(i_row, j_in_row))
                        print(str(e))
                rows.append(row)

        # with open(target_path, 'w+', newline='') as target_csv:
        target_csv = open(target_path, 'w+', newline='')
        writer = csv.DictWriter(target_csv, fieldnames=fieldnames)
        writer.writeheader()

        error_csv = open(error_path, 'w+', newline='')
        error_writer = csv.DictWriter(error_csv, fieldnames=fieldnames)
        error_writer.writeheader()

        settings.configure()
        time = timezone.now()
        upload_paths = {
            'file': '/posts/Canto/karaokes/{}-{}/',
            'full_file': '/posts/Canto/karaokes/{}-{}/',
            'cover_photo': '/posts/Canto/covers/{}-{}/'
        }

        row_index = 1
        for row in rows:
            print(row_index)
            add_row = True
            for field in upload_paths:
                if row.get(field):
                    file_path = row.get(field)
                    file_name = file_path.split('/')[-1]
                    file_name = file_name.replace(' ', '+')
                    year = time.year
                    month = time.month
                    file_exists = False
                    for i in range(0, 3):
                        if self.get_file_info(path=upload_paths[field].format(year, month - i), file=file_name):
                            row[field] = self.address + upload_paths[field].format(year, month - i) + file_name
                            file_exists = True
                            break
                    add_row = add_row and file_exists

            row_index += 1
            if add_row:
                writer.writerow(row)
            else:
                error_writer.writerow(row)

        error_csv.close()
        target_csv.close()


print('Welcome  to Canto Upload files tool.')
directory = input('Enter directory from source: (press enter for blank)\n')
csv_file = input('Enter Source CSV file name:\n')

uploader = Backtory()
uploader.read_file(directory=directory, name=csv_file)
