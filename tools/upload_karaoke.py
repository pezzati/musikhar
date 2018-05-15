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
        headers = {
            'Authorization': 'Bearer {}'.format(self.token.access_token),
            'X-Backtory-Storage-Id': self.Storage_Id,
            'Content-Type': 'application/json'
        }
        url = 'http://storage.backtory.com/files/fileInfo'
        path += file.split('/')[-1]
        path = path.replace('//', '/')
        data = {'url': path}
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        if res.status_code == 200:
            return True
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
            d = '/{}/{}'.format(path, file.split('/')[-1]).replace('//', '/')
            return json.dumps({'savedFilesUrls': [d]}).encode('utf-8'), ''

        process = Popen(self.gen_multi_part_post_comm(file=file, path=path), stdout=PIPE, stderr=PIPE, shell=True)
        (out, err) = process.communicate()
        if self.get_file_info(path=path, file=file):
            d = '/{}/{}'.format(path, file.split('/')[-1]).replace('//', '/')
            return json.dumps({'savedFilesUrls': [d]}).encode('utf-8'), ''
        return '', 'upload failed'

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
        if name[-4:] != '.csv':
            name += '.csv'
        if directory:
            source_path = '{}/{}'.format(directory, name).replace('//', '/')
            target_path = '{}/new_{}'.format(directory, name).replace('//', '/')
        else:
            source_path = '{}'.format(name).replace('//', '/')
            target_path = 'new_{}'.format(name).replace('//', '/')

        rows = []
        with open(source_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
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

        with open(target_path, 'w+', newline='') as target_csv:
            writer = csv.DictWriter(target_csv, fieldnames=fieldnames)
            writer.writeheader()

            settings.configure()
            time = timezone.now()
            upload_paths = {
                'file': '/posts/Canto/karaokes/{}-{}/'.format(time.year, time.month),
                'full_file': '/posts/Canto/karaokes/{}-{}/'.format(time.year, time.month),
                'cover_photo': '/posts/Canto/covers/{}-{}/'.format(time.year, time.month)
            }

            row_index = 1
            for row in rows:
                for field in upload_paths:
                    if row.get(field):
                        file_path = row.get(field)
                        path = Path(file_path)
                        if path.is_file():
                            if not path.is_absolute():
                                file_path = path.absolute()
                            try:
                                out, err = self.upload_file(file=file_path, path=upload_paths[field])
                            except Exception as e:
                                print('ERROR in row:{} : {}'.format(row_index, str(e)))
                                row[field] = '!!!ERROR!!!: {}'.format(err)
                            print(row_index)
                            print(out)
                            if out:
                                out = json.loads(out.decode('utf-8'))
                                uploaded_add = out.get('savedFilesUrls')[0]
                                row[field] = ('{}{}'.format(self.address, uploaded_add))
                            else:
                                row[field] = '!!!ERROR!!!: {}'.format(err)
                        else:
                            row[field] = '!!!ERROR!!!: Can not find the file'
                row_index += 1
                writer.writerow(row)


# print('Welcome  to Canto Upload files tool.')
# directory = input('Enter directory from source: (press enter for blank)\n')
# file_name = input('Enter Source CSV file name:\n')
#
# uploader = Backtory()
# uploader.read_file(directory=directory, name=file_name)
