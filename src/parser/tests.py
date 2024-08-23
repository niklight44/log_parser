from django.test import TestCase
from django.core.management import call_command
from io import StringIO
from parser.models import NginxLog
from unittest.mock import mock_open, patch
from .management.commands.parse_nginx_logs import Command

class TestParseNginxLogs(TestCase):
    def setUp(self):
        # List to keep tracking of created log entries
        self.created_logs = set()
        self.command = Command()

    def tearDown(self):
        # Cleanup that runs after each test for deleting the logs created during the test.
        NginxLog.objects.filter(id__in=self.created_logs).delete()

    def test_empty(self):
        # Testing with an empty log file
        initial_count = NginxLog.objects.count()
        with patch('builtins.open', mock_open(read_data="")) as mocked_file:
            self.command.parse_log_file('dummy_path')
            mocked_file.assert_called_once_with('dummy_path', 'r')
            final_count = NginxLog.objects.count()
            self.assertEqual(final_count, initial_count)
            print("Test for empty file passed.")

    def test_wrong_format(self):
        # Test with a log file with incorrectly formatted entries
        initial_count = NginxLog.objects.count()
        invalid_log_data = """
        {"time": "invalid_date", "remote_ip": "80.91.33.133", "request": "GET /downloads/product_1 HTTP/1.1"}
        """
        with patch('builtins.open', mock_open(read_data=invalid_log_data)):
            with self.assertRaises(ValueError):  # Assuming ValueError would be raised for invalid date format
                self.command.parse_log_file('dummy_path')
            final_count = NginxLog.objects.count()
            self.assertEqual(final_count, initial_count)
            print("Test for wrong format passed.")

    def test_valid_entries(self):
        # Test with correctly formatted log entries
        initial_count = NginxLog.objects.count()
        valid_log_data = """
        {"time": "17/May/2015:08:05:24 +0000", "remote_ip": "80.91.33.133", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0}
        {"time": "17/May/2015:08:05:34 +0000", "remote_ip": "217.168.17.5", "request": "GET /downloads/product_1 HTTP/1.1", "response": 200, "bytes": 490}
        """
        with patch('builtins.open', mock_open(read_data=valid_log_data)):
            self.command.parse_log_file('dummy_path')
            new_entries = NginxLog.objects.exclude(id__in=self.created_logs)
            self.created_logs.update(new_entries.values_list('id', flat=True))
            final_count = NginxLog.objects.count()
            self.assertEqual(final_count, initial_count + 2)  # 2 new entries should be added
            log1 = NginxLog.objects.get(ip="80.91.33.133")
            self.assertEqual(log1.response_code, 304)
            print("Test for valid entries passed.")

    def test_mixed_valid_and_invalid_entries(self):
        # Test with a mix of valid and invalid entries
        initial_count = NginxLog.objects.count()
        mixed_log_data = """
        {"time": "17/May/2015:08:05:24 +0000", "remote_ip": "80.91.33.133", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0}
        {"time": "invalid_date", "remote_ip": "80.91.33.133", "request": "GET /downloads/product_1 HTTP/1.1"}
        """
        with patch('builtins.open', mock_open(read_data=mixed_log_data)):
            with self.assertRaises(ValueError):  # Invalid date should raise ValueError
                self.command.parse_log_file('dummy_path')
            final_count = NginxLog.objects.count()
            # Since the exception is raised, no entries should be added.
            self.assertEqual(final_count, initial_count)
            print("Test for mixed valid and invalid entries passed.")

    def test_large_log_file(self):
        # Test with a large log file to ensure scalability
        initial_count = NginxLog.objects.count()
        large_log_data = "\n".join([
            '{"time": "17/May/2015:08:05:24 +0000", "remote_ip": "80.91.33.133", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0}'
            for _ in range(10000)
        ])
        with patch('builtins.open', mock_open(read_data=large_log_data)):
            self.command.parse_log_file('dummy_path')
            new_entries = NginxLog.objects.exclude(id__in=self.created_logs)
            self.created_logs.update(new_entries.values_list('id', flat=True))  # Track new entries
            final_count = NginxLog.objects.count()
            self.assertEqual(final_count, initial_count + 1000)  # 1000 new entries should be added
            print("Test for large log file passed.")
