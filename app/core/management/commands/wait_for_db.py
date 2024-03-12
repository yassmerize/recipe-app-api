from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error
import time


class Command(BaseCommand):
    """Django command to wait for db."""

    def handle(self, *args, **options):
        self.stdout.write("Checking the database ...")

        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database is not available. Waiting for 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database is available!"))
