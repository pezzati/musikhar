from django.core.management import BaseCommand

from tools.upload_karaoke import Backtory


class Command(BaseCommand):
    help = 'Upload Backtory related Files that specified in given CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, default='tools', help='Directory of the CSV file',)
        parser.add_argument('file', type=str, default='upload_list.csv', help='Name of CSV file')

    def handle(self, *args, **options):
        uploader = Backtory()
        uploader.read_file(name=options.get('file'), directory=options.get('directory'))

