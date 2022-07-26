from django.core.management.base import BaseCommand
from common.utils.import_utils import import_goods


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--files', nargs='+', type=str)
        parser.add_argument('--email', type=str)

    def handle(self, *args, **kwargs):
        import_goods(files=kwargs['files'], email=kwargs['email'])
