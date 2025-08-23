"""
Test custom Django management commands.
"""
# MOCK TO MAKE FAST AND DO IN SHORTCUT
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check') # we going to mock this "check" method    TO SIMULATE THE PROCESS
class CommandTests(SimpleTestCase):
    """Test commands."""

    # This is the magic where the "patch" decorator pass an argument "patched" with name of the method "check"    "patced_check"
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(database=['default'])

    # WE DON'T ACTUALLY WANTED TO SLEEP DURING TESTING
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # THE POSTGRESQL HAVEN'T EVEN STARTED SO, "Pysopg2Error"    THE POSTGRESQL READY BUT NOT ACCEPTING THE TESTING DATABASE FROM DJANGO SO, "OperationalError"
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(database=['default'])