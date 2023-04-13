"""
Django command to wait for the database to be available
"""

import time

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

from django.db import connections

class Command(BaseCommand):
    """Django command to wait for database"""
    help = "Command to wait for databases to be available"
    def handle(self, *args, **kwargs):
        """Entrypoint for command."""
        time_to_wait = 5 #seconds
        self.stdout.write(f'Waiting {time_to_wait} secs for database ...')
        time.sleep(time_to_wait)
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
                self.stdout.write(db_conn)
            except Exception as e:
                self.stdout.write(f'Exception: {e}')
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS('Database available!'))