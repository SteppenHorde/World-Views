# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.core.files.base import ContentFile, File

import yadisk



# приложение может работать только со своей папкой на диске
@deconstructible
class YAStorage(Storage):
    def __init__(self, options=None):
        if not options:
            options = settings.YA_STORAGE_OPTIONS
        self.APP_ID = options['APP_ID']
        self.APP_SECRET = options['APP_SECRET']
        self.TOKEN = options['TOKEN']
        self.MAIN_PATH = options['MAIN_PATH']

        self.disk = yadisk.YaDisk(self.APP_ID, self.APP_SECRET, self.TOKEN)

    def _open(self, name, mode='rb'):
        file_name = name.split(r'/')[-1]
        self.disk.download(self.MAIN_PATH + name, file_name)
        with open(file_name, 'r') as file_handler:
            file = ContentFile(file_handler.read())
        file.name = file_name
        file.mode = 'r'
        return file

    def _save(self, name, content):
        self.disk.upload(content, self.MAIN_PATH + name, overwrite=True)
        return name

    def __eq__(self, other):
        return (self.APP_ID == other.APP_ID) and (self.APP_SECRET == other.APP_SECRET) and (self.TOKEN == other.TOKEN) and (self.MAIN_PATH == other.MAIN_PATH)

    def delete(self, name):
        self.disk.remove(self.MAIN_PATH + name)
        return

    def exists(self, name):
        return self.disk.is_file(self.MAIN_PATH + name)

    def listdir(path):
        files = list()
        dirs = list()
        content = self.disk.listdir(self.MAIN_PATH + path)
        for resourse in content:
            if resourse.type == 'file':
                files.append(resourse.name)
            elif resourse.type == 'dir':
                dirs.append(resourse.name)

        return (dirs, files)

    def url(self, name):
        return self.disk.get_download_link(self.MAIN_PATH + name)
