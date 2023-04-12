from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        if options['short']:
            print('Hello world')
        else:
            import this

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--short',
            action='store_true',
            default=False,
            help='Вывод короткого сообщения'
        )
