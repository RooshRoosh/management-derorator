# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

import commands
import re
import os

#from settings import PID_PATH
PID_PATH = ''

def check_pid(function, callback):
    def wrapper(self, *args, **options):
        def run_function(): # ^- #Создаём/Удаляем pid Вызываем handle для работы
            open(pid_filename,'wb').close()
            try:
                function(self, *args, **options)
            except Exception, q:
                os.remove(pid_filename)
                raise Exception('Fail command because of %s' % q) # Логируeм отказ handle
            os.remove(pid_filename) # Удаляем pid-file после удачного завершения работы


        #======================================================================#
        command_name = self.__module__.split('.')[-1] # Вытащили имя команды        
        pid_filename = os.path.join(PID_PATH, command_name+'.pid')
        if os.path.exists(pid_filename): # Проверяем наличие файла
            # Нашли
            # Проверяем если ли в работе старый процесс.
            st = 'ps ax| grep "python manage.py %s"' % command_name
            commandOutput = commands.getoutput(st) # Нашли все процессы с этой фразой
            feed = [string for string in commandOutput.split('\n')
                if re.search(r'\d\d?:\d\d python manage.py %s' % command_name, string)] # Отсеяли лишние процессы
        
            if len(feed) == 1: # Оценили количество "истинных" процессов
                # 1 означает что в работе только текущий процесс
                return run_function()
            else:
                # В работе уже есть такие процессы
                # Пид-файл соответствует процессу
                return callback() # Обрабатываем 
        else:
            run_function()
    return wrapper

