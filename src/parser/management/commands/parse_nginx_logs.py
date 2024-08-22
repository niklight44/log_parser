import json

from django.core.management import BaseCommand
from datetime import datetime
from parser.models import NginxLog


class Command(BaseCommand):
    help = 'Parse Nginx Log File into DB'

    def add_arguments(self, parser):
        parser.add_argument('--log_path', type=str)

    def handle(self, *args, **options):
        log_path = options.get('log_path')
        self.parse_log_file(log_path)
        print('File was parsed')

    def parse_log_file(self, log_path:str) -> None:
        """Parsing Nginx Log File

        :param log_path: string
        """
        with open(log_path, 'r') as log_file:
            for line in log_file:
                log_data = json.loads(line.strip())

                # Parsing date and time
                date_str = log_data['time'].split()[0]
                date_obj = datetime.strptime(date_str, "%d/%b/%Y:%H:%M:%S")

                # Parsing HTTP method and URI from request
                method, request_URI, _ = log_data['request'].split()

                # Saving data to the DB
                NginxLog.objects.create(
                    ip=log_data['remote_ip'],
                    date=date_obj,
                    method=method,
                    request_URI=request_URI,
                    response_code=log_data['response'],
                    response_size=log_data['bytes']
                )