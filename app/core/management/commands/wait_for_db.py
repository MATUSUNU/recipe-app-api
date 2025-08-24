"""
Django command to wait for the database to be available.
"""
import time
from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        # we assume that the database IS NOT
        # READY PUTTING THE VALUE BY DEFAULT=FALSE
        db_up = False
        while db_up is False:
            try:
                # TRY TO CHECK THE DATABASE READINESS
                # IF THE DATABASE IS NOT READY IT WILL
                # THROW ERROR [THIS IS MAGIC]
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
