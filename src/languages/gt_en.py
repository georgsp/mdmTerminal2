# Generated by scripts/localization_gen.py

LANG_CODE = {
    'IETF': 'en-US',
    'ISO': 'en',
    'aws': 'en-US',
}

YANDEX_EMOTION = {
    'good': 'good',
    'neutral': 'neutral',
    'evil': 'evil',
}

YANDEX_SPEAKER = {
    'jane': 'Jane',
    'oksana': 'Oksana',
    'alyss': 'Alyss',
    'omazh': 'Omazh',
    'zahar': 'Zahar',
    'ermil': 'Ermil',
}

RHVOICE_SPEAKER = {
    'alan': 'Alan',
    'bdl': 'bdl',
    'clb': 'clb',
    'slt': 'slt',
    'anna': 'Anna',
}

AWS_SPEAKER = {
    'Joey': 'Joey',
    'Justin': 'Justin',
    'Matthew': 'Matthew',
    'Ivy': 'Ivy',
    'Joanna': 'Joanna',
    'Kendra': 'Kendra',
    'Kimberly': 'Kimberly',
    'Salli': 'Salli',
}

_LNG = {  # google translate - it's a good idea!
    # config.py
    'Ошибка получения ключа для Yandex: {}': 'Error receiving key for Yandex: {}',
    'Ошибка сохранения {}: {}': 'Error saving {}: {}',
    # config.py backup.py
    'Файл не найден: {}': 'File not found: {}',
    # config.py
    'Ошибка загрузки {}: {}': 'Loading error {}: {}',
    'Конфигурация сохранена за {}': 'Configuration saved for {}',
    'Конфигурация сохранена!': 'Configuration saved!',
    'Директория с моделями не найдена {}': 'Model directory not found {}',
    'Загружено {} моделей': 'Uploaded {} models',
    'Файл настроек не найден по пути {}. Для первого запуска это нормально': 'Settings file not found on path {}. This is normal for the first run.',
    'Загружено {} опций за {}': 'Uploaded {} options for {}',
    'Конфигурация загружена!': 'Configuration uploaded!',
    'Ошибка инициализации языка {}: {}': 'Error initializing language {}: {}',
    'Локализация {} загружена за {}': 'Localization {} loaded for {}',
    'Конфигурация изменилась': 'Configuration changed',
    'Конфигурация не изменилась': 'The configuration has not changed',
    'Директория c tts кэшем не найдена {}': 'Directory with tts cache not found {}',
    'Удалены поврежденные файлы: {}': 'Corrupted files deleted: {}',
    'Размер tts кэша {}: {}': 'Size of tts cache {}: {}',
    'Ок.': 'OK.',
    'Удаляем...': 'Delete ...',
    'Удалено: {}': 'Deleted: {}',
    'Удалено {} файлов. Новый размер TTS кэша {}': 'Deleted {} files. New TTS cache size {}',
    'Директория {} не найдена. Создаю...': 'Directory {} not found. I create ...',
    # config.py terminal.py player.py
    'Файл {} не найден.': 'File {} not found.',
    # config.py
    'Это надо исправить!': 'This must be fixed!',
    'Терминал еще не настроен, мой IP адрес: {}': 'The terminal is not configured yet, my IP address is {}',
    # loader.py
    'Приветствую. Голосовой терминал настраивается, три... два... один...': 'Greetings. The voice terminal is configured, three ... two ... one ...',
    'Голосовой терминал завершает свою работу.': 'The voice terminal is shutting down.',
    # listener.py
    '{} слушает': '{} listening',
    'Голосовая активация по {}{}': 'Voice Activated by {} {}',
    # modules.py
    'блокировка': 'blocking',
    'Блокировка снята': 'The lock is released',
    'Блокировка включена': 'Lock On',
    'Блокировка': 'Lock',
    'Включение/выключение блокировки терминала': 'Turn on / off terminal lock',
    'выход': 'exit',
    'Внимание! Выход из режима разработчика': 'Attention! Exit Developer Mode',
    'режим разработчика': 'developer mode',
    "Внимание! Включён режим разработчика. Для возврата в обычный режим скажите 'выход'": "Attention! Developer mode is on. To return to normal mode, say 'exit'",
    # modules.py modules_manager.py
    'Отладка': 'Debugging',
    # modules.py
    'Режим настройки и отладки': 'Setup and Debug Mode',
    'Модуль {} не найден': 'Module {} not found',
    'Модуль {} системный, его нельзя настраивать': 'The module {} is system, it cannot be configured',
    'активировать': 'activate',
    'деактивировать': 'deactivate',
    'активировать везде': 'activate everywhere',
    'удалить': 'remove',
    'восстановить': 'reestablish',
    'Модуль {} удален. Вначале его нужно восстановить': 'The module {} has been removed. It must first be restored.',
    'Модуль {} уже в режиме {}': 'Module {} is already in {} mode',
    'Теперь модуль {} доступен в режиме {}': 'The {} module is now available in {} mode',
    'Модуль {} и так {}': 'Module {} and so {}',
    'Модуль {} {}': 'Module {} {}',
    'Это невозможно, откуда тут {}': 'It’s impossible, where is it from {}',
    'Менеджер': 'Manager',
    'Управление модулями': 'Module management',
    'Скажи': 'Tell me',
    'Произнесение фразы': 'Pronouncing Phrases',
    'Ничего': 'Nothing',
    'до': 'before',
    'от': 'from',
    'Это слишком много для меня - считать {} чисел.': "It's too much for me to count {} numbers.",
    'Я всё сосчитала': 'I counted everything',
    'считалка': 'reading room',
    'Считалка до числа. Или от числа до числа. Считалка произносит не больше 20 чисел за раз': 'Count to number. Or from number to number. The reader says no more than 20 numbers at a time',
    'сосчитай': 'count',
    'считай': 'count',
    'посчитай': 'count',
    'Ошибка': 'Error',
    'Не поддерживается для {}': 'Not supported for {}',
    ' Я очень {}.': ' I am very {}.',
    'Меня зовут {}.{}': 'My name is {}.{}',
    'Кто я': 'Who am I',
    'Получение информации о настройках голосового генератора (только для Яндекса и RHVoice)': 'Getting information about the settings of the voice generator (only for Yandex and RHVoice)',
    'кто ты': 'Who are you',
    'какая ты': 'what are you',
    'Теперь я': 'Now I',
    'Изменение характера или голоса голосового генератора (только для Яндекса и RHVoice)': 'Change the character or voice of a voice generator (Yandex and RHVoice only)',
    'теперь ты': 'now you',
    'стань': 'become',
    'Я уже {}.': "I'm already {}.",
    'Теперь меня зовут {}, а еще я {}.': 'Now my name is {}, and I am {}.',
    'без характера': 'without character',
    'Теперь я очень {} {}.': 'Now I am very {} {}.',
    'о': 'about',
    'про': 'about',
    'в': 'in',
    'Ищу в вики о {}': 'I look in the wiki about {}',
    'Уточните свой вопрос: {}': 'Specify your question: {}',
    'Я ничего не знаю о {}.': "I don't know anything about {}.",
    'Вики': 'Wiki',
    'Поиск в Википедии': 'Wikipedia Search',
    'расскажи': 'tell me',
    'что ты знаешь': 'what do you know',
    'кто такой': 'who it',
    'что такое': 'what',
    'зачем нужен': 'why do i need',
    'для чего': 'for what',
    'любую фразу': 'any phrase',
    '. Модуль удален': '. Module removed',
    'Модуль {} доступен в режиме {}. Для активации скажите {}. Модуль предоставляет {} {}': 'The {} module is available in {} mode. To activate, say {}. The module provides {} {}',
    'Всего {} модулей удалены, это: {}': 'Total {} modules removed, this: {}',
    'Скажите {}. Это активирует {}. Модуль предоставляет {}': 'Say {}. This will activate {}. The module provides {}',
    'Работа модуля помощь завершена.': 'Help module operation completed.',
    'Помощь': 'Help',
    'Справку по модулям (вот эту)': 'Module Help (this one)',
    'помощь': 'help',
    'справка': 'reference',
    'help': 'help',
    'хелп': 'help',
    'Come Along With Me.': 'Come Along With Me.',
    'Выход': 'Exit',
    'Завершение работы голосового терминала': 'Voice terminal shutdown',
    'завершение работы': 'completion of work',
    'завершить работу': 'to finish work',
    'завершить': 'to complete',
    'Терминал перезагрузится через 5... 4... 3... 2... 1...': 'The terminal will reboot in 5 ... 4 ... 3 ... 2 ... 1 ...',
    'Перезагрузка': 'Reboot',
    'Перезапуск голосового терминала': 'Voice terminal restart',
    'Ребут': 'Reboot',
    'Рестарт': 'Restart',
    'reboot': 'reboot',
    'громкость': 'volume',
    'Изменение громкости': 'Volume change',
    'громкость музыки': 'music volume',
    # modules.py modules_manager.py
    'Вы ничего не сказали?': 'You didn’t say anything?',
    # modules.py
    'IP сервера не задан.': 'Server IP is not set.',
    'IP сервера не задан, исправьте это! Мой IP адрес: {}': 'Server IP is not set, fix it! My IP Address: {}',
    'Скажи ': 'Tell me ',
    'Запрос был успешен: {}': 'The request was successful: {}',
    'Ошибка коммуникации с сервером: {}': 'Error communicating with server: {}',
    'Мажордом': 'Majordom',
    'Отправку команд на сервер': 'Sending commands to the server',
    'Соответствие фразе не найдено: {}': 'No matching phrase found: {}',
    'Терминатор': 'Terminator',
    'Информацию что соответствие фразе не найдено': 'Information that no matching phrase was found',
    # modules_manager.py
    'Обычный': 'Normal',
    'Любой': 'Any',
    'восстановлен': 'restored',
    'удален': 'deleted',
    'Отключенные модули: {}': 'Disabled modules: {}',
    'Неактивные модули: {}': 'Inactive modules: {}',
    'Активные модули: {}': 'Active Modules: {}',
    'Обнаружены конфликты в режиме {}: {}': 'Conflicts detected in {} mode: {}',
    'Захвачено {}': 'Captured {}',
    # terminal.py
    'Пустая очередь? Impossible!': 'An empty queue? Impossible!',
    'Получено {}:{}, lvl={} опоздание {} секунд.': 'Received {}: {}, lvl = {} delay {} seconds.',
    '{} Игнорирую.': '{} Ignore it.',
    'Не верный вызов, WTF? {}:{}, lvl={}': 'Wrong call, WTF? {}: {}, lvl = {}',
    'Недопустимое значение: {}': 'Invalid value: {}',
    'Не настроено': 'Not configured',
    'Громкость {} процентов': 'Volume {} percent',
    'Громкость музыки {} процентов': 'Music volume {} percent',
    'первого': 'the first',
    'второго': 'second',
    'третьего': 'third',
    'Ошибка записи - недопустимый параметр': 'Write Error - Invalid Parameter',
    'Запись {} образца на 5 секунд начнется после звукового сигнала': 'Recording {} of the sample for 5 seconds will start after a beep',
    'Запись {} образца завершена. Вы можете прослушать свою запись.': 'Recording {} of the sample is completed. You can listen to your recording.',
    'Ошибка сохранения образца {}: {}': 'Error saving sample {}: {}',
    'Ошибка воспроизведения - файл {} не найден': 'Playback Error - File {} Not Found',
    'Ошибка компиляции - файл {} не найден.': 'Compilation error - file {} was not found.',
    'Ошибка удаление модели номер {}': 'Error deleting model number {}',
    'Модель номер {} удалена': 'Model number {} deleted',
    'Модель номер {} не найдена': 'Model number {} not found',
    'Полный консенсус по модели {} не достигнут [{}/{}]. Советую пересоздать модель.': 'Full consensus on model {} not reached [{} / {}]. I advise you to recreate the model.',
    'Полный консенсус по модели {} не достигнут. Компиляция отменена.': 'Full consensus on model {} has not been reached. Compilation canceled.',
    'Компилирую {}': 'Compiling {}',
    'Ошибка компиляции модели {}: {}': 'Error compiling model {}: {}',
    'Ошибка компиляции модели номер {}': 'Error compiling model number {}',
    'Модель{} скомпилирована успешно за {}: {}': 'Model {} compiled successfully for {}: {}',
    'Модель{} номер {} скомпилирована успешно за {}': 'Model {} number {} compiled successfully for {}',
    # logger.py
    'Логгирование в {} невозможно - отсутствуют права на запись. Исправьте это': 'Logging in {} is not possible - there are no write permissions. Fix it',
    # stts.py
    'Неизвестный провайдер: {}': 'Unknown provider: {}',
    '{} за {}{}: {}': '{} behind {}{}: {}',
    '{}найдено в кэше': '{} found in cache',
    '{}сгенерированно {}': '{} generated {}',
    "Ошибка синтеза речи от {}, ключ '{}'. ({})": "Speech synthesis error from {}, key '{}'. ({})",
    'Микрофоны не найдены': 'No microphones found',
    'Доступны {}, от 0 до {}.': 'Available are {}, from 0 to {}.',
    'Не верный индекс микрофона {}. {}': 'Invalid microphone index {}. {}',
    'Голос записан за {}': 'Voice recorded for {}',
    'Во время записи произошел сбой, это нужно исправить': 'There was a failure while recording, it needs to be fixed',
    'Ошибка распознавания - неизвестный провайдер {}': 'Recognition Error - Unknown Provider {}',
    'Для распознавания используем {}': 'For recognition we use {}',
    'Произошла ошибка распознавания': 'Recognition Error Occurred',
    "Ошибка распознавания речи от {}, ключ '{}'. ({})": "Speech recognition error from {}, key '{}'. ({})",
    'Распознано за {}': 'Recognized for {}',
    'Распознано: {}. Консенсус: {}': 'Recognized: {}. Consensus: {}',
    'Привет': 'Hi',
    'Слушаю': "I'm listening",
    'На связи': 'In touch',
    'Привет-Привет': 'Hi Hi',
    'Я ничего не услышала': "I didn't hear anything",
    'Вы ничего не сказали': "You didn't say anything",
    'Ничего не слышно': 'Can not hear anything',
    'Не поняла': 'I did not get that',
    'Ничего не слышно, повторите ваш запрос': 'Hearing nothing, repeat your request',
    # player.py
    'Неизвестный тип файла: {}': 'Unknown file type: {}',
    'Играю {} ...': "I'm playing {} ...",
    'Стримлю {} ...': 'Streaming {} ...',
    # updater.py
    'Выполнен откат.': 'Rollback completed.',
    'Во время обновления возникла ошибка': 'An error occurred while updating',
    'Вы используете последнюю версию терминала.': 'You are using the latest version of the terminal.',
    'Файлы обновлены: {}': 'Files updated: {}',
    'Терминал успешно обновлен.': 'The terminal has been updated successfully.',
    'Требуется перезапуск.': 'Restart required.',
    'Во время обработки обновления или установки зависимостей возникла ошибка': 'An error occurred while processing the update or installing dependencies',
    'Выполняется откат обновления.': 'Updates are rolled back.',
    'Во время отката обновления возникла ошибка: {}': 'An error occurred while rolling back the update: {}',
    'Откат невозможен.': 'Rollback is not possible.',
    'Откат обновления выполнен успешно.': 'The rollback of the update was successful.',
    'Зависимости {} {}обновлены: {}': 'Dependencies {} {} updated: {}',
    'не ': 'not ',
    # server.py
    'Ошибка запуска сервера{}.': 'Error starting server {}.',
    ' - адрес уже используется': ' - the address is already in use',
    'Ошибка запуска сервера на {}:{}: {}': 'Error starting server on {}: {}: {}',
    # backup.py
    'Запущено восстановление из бэкапа {}...': 'Restored from backup {} ...',
    'Восстановление не возможно: {}': 'Recovery is not possible: {}',
    'Восстановление не удалось: {}': 'Recovery failed: {}',
    'бэкап не создан': 'backup not created',
    'Восстановление завершено за {}, восстановлено {} файлов': 'Recovery completed in {}, restored {} files',
    'Демон еще работает': 'The daemon is still running',
    'Некорректное имя файла: {}': 'Invalid file name: {}',
    'Архив поврежден: {}: {}': 'Archive damaged: {}: {}',
    'Ошибка создания бэкапа': 'Error creating backup',
    'Файл {} уже существует, отмена.': 'File {} already exists, cancel.',
    'файл уже существует': 'file already exists',
    'Бэкап {} создан за {} [size: {}, compressed: {}, rate: {}%]': 'Backup {} was created for {} [size: {}, compressed: {}, rate: {}%]',
    'Бэкап успешно создан': 'Backup successfully created',
    'Ошибка удаления старого бэкапа {}: {}': 'Error deleting old backup {}: {}',
    'Удален старый бэкап {}': 'Deleted old backup {}',
    # lib/base_music_controller.py
    'Ошибка подключения к {}-серверу': 'Error connecting to {} server',
}
