from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from datetime import datetime
from app_goods.models import Goods, Shops, GoodsInShops, GoodsStorages
from app_categories.models import Categories
import json
import os


class FileManager:
    @staticmethod
    def check_dirs():
        directories = ('to_import', 'successful', 'failed', 'logs')
        for directory in directories:
            os.makedirs(f'import/{directory}', exist_ok=True)

    @staticmethod
    def move_file(file, to):
        os.replace(f'import/to_import/{file}', f'import/{to}/{file}')


class EmailSender:
    @staticmethod
    def send(message, email, title, errors=None):
        if errors:
            message = '\n'.join((message, 'The following errors were encountered:', ';\n'.join(errors)))
        send_mail(
            title,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )


class Logger:
    def __init__(self):
        self.__log_file = f'import_from_{datetime.now()}.log'
        self.__messages = []

    @property
    def messages(self):
        return self.__messages

    def write_log(self, message, to_email=False):
        with open(f'import/logs/{self.__log_file}', 'a') as f:
            f.write(''.join((message, '\n')))
        if to_email:
            self.__messages.append(message)


class ImportGoods:
    MODELS = {'Goods': Goods, 'Shops': Shops, 'GoodsInShops': GoodsInShops, 'GoodsStorages': GoodsStorages}
    FOREIGN_KEYS = {'categoryidx': Categories, 'goodsidx': Goods, 'shopidx': Shops}

    def __init__(self, files, file_manager, logger):
        if not files:
            files = os.listdir('import/to_import')
        self.__files = files
        self.__file_manager = file_manager
        self.__logger = logger
        self.__import_files()

    def __import_files(self):
        for file in self.__files:
            if not file.endswith('.json'):
                self.__logger.write_log(f'Critical error! File {file} is not in json', to_email=True)
                self.__file_manager.move_file(file, 'failed')
                continue
            try:
                with open(os.path.join('import', 'to_import', file), 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                self.__logger.write_log(f'Critical error! File {file} is not decrypted', to_email=True)
                self.__file_manager.move_file(file, 'failed')
                continue
            self.__parse_file(data, file)
            self.__file_manager.move_file(file, 'successful')

    def __parse_file(self, data, file):
        for entry in data:
            try:
                model = self.MODELS[entry['model']]
            except KeyError:
                self.__logger.write_log(f'File {file}, the entry has the wrong model: {entry}', to_email=True)
                continue
            try:
                fields = entry['fields']
            except KeyError:
                self.__logger.write_log(f'File {file}, the entry has no fields: {entry}', to_email=True)
                continue
            self.__preparing_entry(fields)
            self.__save_instance(model, fields, file)

    def __preparing_entry(self, fields):
        fields.pop('id', None)
        for field in fields:
            if field in self.FOREIGN_KEYS:
                try:
                    fields[field] = self.FOREIGN_KEYS[field].objects.get(id=fields[field])
                except (ValueError, ObjectDoesNotExist):
                    pass

    def __save_instance(self, model, fields, file):
        try:
            instance = model.objects.create(**fields)
        except TypeError as err:
            self.__logger.write_log(f'File {file}, the entry has the wrong field: {err}', to_email=True)
        except Exception as err:
            self.__logger.write_log(f'File {file}, the entry has an incorrect field value: {err}', to_email=True)
        else:
            self.__logger.write_log(f'File {file}, instance {instance} has been created')


def import_goods(email, files):
    file_manager = FileManager()
    logger = Logger()
    file_manager.check_dirs()
    ImportGoods(files=files, file_manager=file_manager, logger=logger)
    if email:
        EmailSender.send(email=email, message='The download is completed',
                         title='Online shop import', errors=logger.messages)
