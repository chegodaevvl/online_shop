from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Enable FTS features PG'

    queries = [
        """CREATE EXTENSION IF NOT EXISTS pg_trgm""",
        """CREATE EXTENSION IF NOT EXISTS btree_gin""",
        """CREATE EXTENSION IF NOT EXISTS unaccent""",
    ]

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            for query in self.queries:
                cursor.execute(query)
