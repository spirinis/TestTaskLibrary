# -*- coding: utf-8 -*-
import re
import logging
import json


class Book:
    """Класс работы с типом данных книга"""
    def __init__(self, id_: int, title: str, author: str, year: int, status: str | None = None) -> None:
        self.__id: int = id_
        self.__title: str = title
        self.__author: str = author
        self.__year: int = year
        if status:
            self.__status: str = status
        else:
            self.__status: str = 'в наличии'

    def __repr__(self) -> str:
        return f'Book({self.__title}, {self.__author}, {self.__year}, {self.__status})'

    def __str__(self) -> str:
        return (f'{self.__id:>5}: Книга \'{self.__title}\' автора \'{self.__author}\''
                f' {self.__year} года: {self.__status}')

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return (self.__id == other.__id and self.__title == other.__title and
                self.__author == other.__author and self.__year == other.__year)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def author(self) -> str:
        return self.__author

    @property
    def year(self) -> int:
        return self.__year

    @property
    def status(self) -> str:
        return self.__status

    def change_standard_status(self) -> None:
        """Меняет статус книги с 'в наличии' на 'выдана' и обратно"""
        if self.__status == 'в наличии':
            self.__status = 'выдана'
            print('[INFO] Статус изменён:')
        elif self.__status == 'выдана':
            self.__status = 'в наличии'
            print('[INFO] Статус изменён:')
        else:
            print('[WARNING] У книги не стандартный статус. Операция не произведена')
        print(f'[INFO] {self.__str__()}')

    def set_special_status(self) -> None:
        """Меняет статус книги на введённый, переспрашивает, если ввели не статус 'в наличии' или 'выдана'"""
        status = input('Введите новый статус\n>>> ')
        logger.debug('Введено: %s' % status)
        if status != 'в наличии' and status != 'выдана':
            print(f'[WARNING] Вы устанавливаете не стандартный статус: {status}\n'
                  f'Подтвердить - пустой ввод/Y/y\n'
                  f'Отменить - всё остальное')
            answer = input('>>> ')
            logger.debug('Введено: %s' % answer)
            if answer in ('', 'Y', 'y'):
                self.__status = status
                print(f'[INFO] Статус \'{status}\' установлен')
            else:
                print(f'[INFO] Статус не изменён')
                return
        else:
            self.__status = status
            print(f'[INFO] Статус {status} установлен')


class Library:
    """Класс для работы с типом данных библиотека"""
    def __init__(self, name: str) -> None:
        self.__name = name
        self.__stored_ids: list[int] = []
        self.__stored_books: list[Book] = []

    def __str__(self) -> str:
        count = len(self.__stored_ids)
        if count == 1:
            return f'Библиотека {self.__name}, содержащая {count} книгу'
        elif count in (2, 3, 4):
            return f'Библиотека {self.__name}, содержащая {count} книги'
        else:
            return f'Библиотека {self.__name}, содержащая {count} книг'

    def __repr__(self) -> str:
        return f'Library({self.__name})'

    @property
    def name(self) -> str:
        return self.__name

    @property
    def stored_ids(self) -> list[int]:
        return self.__stored_ids

    @property
    def stored_books(self) -> list[Book]:
        return self.__stored_books

    @staticmethod
    def _ask_id_input() -> int:
        """Спросит у пользователя и вернёт id"""
        not_done = True
        while not_done:
            id_ = input('Введите номер книги\n>>> ')
            logger.debug('Введено: %s' % id_)
            try:
                if isinstance(id_, float):
                    raise ValueError
                id_ = int(id_)
                not_done = False
            except ValueError:
                print('[WARNING] Нужно одно целое число. Повторите попытку.')
                continue
        # noinspection PyUnboundLocalVariable
        return id_

    def _find_book_by_id(self, id_: int) -> Book | None:
        """Вернёт книгу с введённым id"""
        if id_ in self.__stored_ids:
            book = self.__stored_books[self.__stored_ids.index(id_)]
            return book
        else:
            print(f'[WARNING] Книги с номером {id_} нет в этой библиотеке')
            return None

    def load(self, books_to_load: list) -> None:
        """Запишет в библиотеку книги из списка"""
        assert len(self.__stored_books) == 0, f'{self.__str__()} не пуста в момент загрузки'
        ids = []
        for book in books_to_load:
            ids.append(book.id)
        assert len(set(ids)) == len(ids), f"Дублирование номеров книг в момент загрузки библиотеки {self.__name}"
        self.__stored_ids.extend(ids)
        self.__stored_books.extend(books_to_load)

    def add_book(self) -> None:
        """Пользовательская функция. Добавляет введённую книгу в библиотеку"""
        not_done = True
        while not_done:
            print('[INFO] Добавление книги:')
            user_input = input("Введите через запятую и пробел или через запятую:"
                               " заголовок, автор, год выпуска книги\n>>> ")
            logger.debug('Введено: %s' % user_input)
            # попытка считывания входных данных через запятую и пробел, запятую
            try:
                split_user_input = user_input.split(', ')
                if len(split_user_input) not in (3, 4):
                    split_user_input = user_input.split(',')
                title, author, year, *some = split_user_input
                logger.debug('split на: %s %s %s и это вот: %s' % (title, author, year, str(*some)))
                # обработка ввода с разделителем в конце
                if some not in ([], ['']):
                    raise ValueError
            except ValueError:
                print('[WARNING] Нужны 3 значения, написанные раздельно через допустимый разделитель.'
                      ' Повторите попытку.')
                continue
            try:
                if type(year) is float:
                    raise ValueError
                year = int(year)
                not_done = False
            except ValueError:
                print('[WARNING] Год должен быть целым числом и стоять третьим по счёту. Повторите попытку.')
        # Поддерживаем нумерацию от 1 до длинны не обновлённого списка + 1
        for id_ in range(1, len(self.__stored_ids) + 2):
            if not (id_ in self.__stored_ids):
                break
        # noinspection PyUnboundLocalVariable
        created_book = Book(id_, title, author, year)
        self.__stored_books.append(created_book)
        self.__stored_ids.append(id_)
        print(f'\'[INFO] {created_book.__str__()}\' добавлена.')

    def delete_book(self) -> None:
        """Пользовательская функция. Удаляет введённую книгу из библиотеки"""
        print('[INFO] Удаление книги:')
        id_ = self._ask_id_input()
        deleted_book = self._find_book_by_id(id_)
        if deleted_book is not None:
            deleted_book = self.__stored_books.pop(self.__stored_ids.index(id_))
            self.__stored_ids.pop(self.__stored_ids.index(id_))
            print(f'[INFO] \'{deleted_book.__str__()}\' удалена')

    def find_book(self, title: str = None, author: str = None, year: int = None) -> None:
        """Пользовательская функция. Поиск введённой книги в библиотеке"""
        def _print_books_from_set(books_set: set[tuple[int, Book]], find_message: str, not_find_message: str,
                                  something_found: bool) -> None:
            """Функция оформления. Выведет результат конкретного поиска"""
            if books_set is not None:
                if bool(books_set):
                    print(find_message)
                    for _, book_ in books_set:
                        print(book_.__str__())
                else:
                    if not something_found:
                        print(not_find_message)

        output = '[INFO] Поиск книги по:'
        if title:
            output += f' заголовку \'{title}\','
        if author:
            output += f' автору \'{author}\','
        if year or (year == 0):
            output += f' {year} года,'
        output = output[:-1] + ':'
        print(output)

        title_matches = []
        author_matches = []
        year_matches = []
        for book in self.__stored_books:
            if (title is not None) and (title == book.title):
                title_matches.append((book.id, book))
            if (author is not None) and (author == book.author):
                author_matches.append((book.id, book))
            if (year is not None) and (year == book.year):
                year_matches.append((book.id, book))
        tms = {*title_matches}
        ams = {*author_matches}
        yms = {*year_matches}
        found = set()
        full_match = title_author_matches = title_year_match = author_year_match = None
        if year == 0:  # ибо bool(0) = False
            year = True
        if title and author and year:
            full_match = tms & ams & yms
            found.update(full_match)
        if title and author:
            title_author_matches = tms & ams - found
            found.update(title_author_matches)
        if title and year:
            title_year_match = tms & yms - found
            found.update(title_year_match)
        if author and year:
            author_year_match = ams & yms - found
            found.update(author_year_match)
        tms = tms - found
        ams = ams - found
        yms = yms - found

        is_something_found = bool(found)
        _print_books_from_set(full_match, 'Полное совпадение:',
                              'Нет полных совпадений', is_something_found)
        _print_books_from_set(title_author_matches, 'Совпадения заголовка и автора:',
                              'Нет совпадений заголовка и автора', is_something_found)
        _print_books_from_set(title_year_match, 'Совпадения заголовка и года:',
                              'Нет совпадений заголовка и года', is_something_found)
        _print_books_from_set(author_year_match, 'Совпадения автора и года:',
                              'Нет совпадений автора и года', is_something_found)
        if title:
            _print_books_from_set(tms, 'Совпадения заголовка:',
                                  'Нет совпадений заголовка', is_something_found)
        if author:
            _print_books_from_set(ams, 'Совпадения автора:',
                                  'Нет совпадений автора', is_something_found)
        if year:
            _print_books_from_set(yms, 'Совпадения года:',
                                  'Нет совпадений года', is_something_found)

    def view_all_books(self) -> None:
        """Пользовательская функция. Выведет оформленный список книг в библиотеке"""
        if len(self.__stored_books) > 0:
            print(f'[INFO] В библиотеке \'{self.__name}\' содержаться следующие книги:')
            for book in self.__stored_books:
                print(book.__str__())
        else:
            print(f'[INFO] В библиотеке \'{self.__name}\' нет книг:')

    def change_book_status(self, want_to_print_it_yourself: bool = False) -> None:
        """Пользовательская функция. Изменит статус книги двумя способами"""
        print('[INFO] Изменение статуса книги:')
        id_ = self._ask_id_input()
        book = self._find_book_by_id(id_)
        if book is not None:
            if want_to_print_it_yourself:
                book.set_special_status()
            else:
                book.change_standard_status()


class JsonConverter:
    """Класс для работы с Json"""
    class Encoder(json.JSONEncoder):
        """Класс для модификации создания Json"""
        # По сути так нужно делать, но я не понял как переопределить обработку кортежей для себя
        def default(self, obj):
            """Функция, добавляющая пользовательские типы к JSONEncoder"""
            if isinstance(obj, Library):
                logger.debug('Books')
                books = {}
                for (book, id_) in zip(obj.stored_books, obj.stored_ids):
                    books.update({book.__repr__(): id_})
                return {obj.__repr__(): books}
            elif isinstance(obj, tuple):  # Обработка кортежей
                logger.debug('Tuples')
                return list(obj)
            elif isinstance(obj, list):
                logger.debug('Lists')
                libraries_ = {}
                for library in obj:
                    libraries_.update(default(library))
                return libraries_  # Обработка списков
            return json.JSONEncoder.default(self, obj)

    class MyEncoder:
        """Класс для создания Json из пользовательского типа вручную"""
        @classmethod
        def default(cls, obj: tuple[Library, ...] | Library) -> dict:
            """Создаст json из tuple[Library, ...]"""
            if isinstance(obj, Library):
                logger.debug('Libraries')
                books = {}
                for (book, id_) in zip(obj.stored_books, obj.stored_ids):
                    books.update({book.__repr__(): id_})
                return {obj.__repr__(): books}
            elif isinstance(obj, tuple):  # Обработка кортежей
                logger.debug('Tuples')
                libraries_ = {}
                for library in obj:
                    libraries_.update(cls.default(library))
                return libraries_
            # return cls.default(obj)

    @staticmethod
    def open_json(path: str) -> dict:
        """Загрузит json в dict"""
        try:
            with open(path, 'r', encoding='cp1251') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            logger.error(f'Не найден файл {path}')
            print(f'[ERROR] Не найден файл {path}')

    @classmethod
    def save_json(cls, libraries: tuple[Library, ...], path: str) -> None:
        """Сохранит данные в json"""
        with open(path, 'w') as file:
            json.dump(cls.MyEncoder.default(libraries), file, indent=2, ensure_ascii=False)
        print(f'[INFO] Данные сохранены в файл \'{path}\'')

    @staticmethod
    def print_json(data: dict) -> None:
        """Напечатает json читаемо"""
        print(json.dumps(data, indent=2, ensure_ascii=False))

    @staticmethod
    def split_str(obj_str: str) -> tuple[str, ...]:
        """Получит данные из Library и Book .__repr__ """
        match = re.search(r"\((.*?)\)", obj_str)
        if match:
            obj_str = match.group(1)
            obj_list = obj_str.split(", ")
            obj_tuple = tuple(obj_list)
            return obj_tuple
        else:
            logger.error('Ошибка расшифровки json')

    @staticmethod
    def add_books_from_dict(books_dict: dict) -> list:
        """Создаст объекты Book из {Book.__repr__(): int, ...}"""
        books_list = []
        for current_book, book_id in books_dict.items():
            title, author, str_year, status = JsonConverter.split_str(current_book)
            books_list.append(Book(int(book_id), title, author, int(str_year), status))
        return books_list


class Client:
    """Класс для взаимодействия с пользователем"""
    __libraries: tuple[Library, ...] = ()

    @property
    def libraries(self):
        return __libraries

    @classmethod
    def start(cls, data_json_path: str, save_json_path: str):
        """Mainloop, Функция запуска программы, управления меню"""
        print('[INFO] Система управления библиотекой запущена')
        libraries_json = JsonConverter.open_json(data_json_path)
        if libraries_json:
            for library_obj_name, books_dict in libraries_json.items():
                library: Library = Library(JsonConverter.split_str(library_obj_name)[0])
                cls.__libraries += (library,)
                library.load(JsonConverter.add_books_from_dict(books_dict))
            print(f'[INFO] Загружены данные из файла {data_json_path}')
            cls.print_libraries()
        else:
            print('[INFO] В системе не содержится ни одной библиотеки')
            cls.__libraries += (cls.create_library(),)
        current_library: Library = cls.__libraries[0]
        previous_choice = None
        work = True
        while work:
            print(f'{'МЕНЮ':=^84}\n'
                  f'[INFO] Работа с библиотекой \'{current_library.name}\'')
            print('Введите цифру - номер требуемого действия:\n'
                  '1 - ДОБАВЛЕНИЕ книги\n'
                  '2 - УДАЛЕНИЕ книги\n'
                  '3 - ПОИСК книги\n'
                  '4 - Отображение ВСЕХ книг\n'
                  '5 - Стандартное изменение СТАТУСа книги\n'
                  '6 - ВВЕСТИ нестандартный СТАТУС книги\n'
                  '7 - СМЕНИТЬ библиотеку\n'
                  '8 - СОЗДАТЬ библиотеку\n'
                  '9 - УДАЛИТЬ библиотеку\n'
                  '10 - ЗАВЕРШИТЬ работу\n'
                  '11 - Убери это, я - Программист (Остановить mainloop, посмотреть инкапсуляцию)')
            print(f'{'':=^84}')
            not_done = True
            while not_done:
                choice = input('>>> ')
                logger.debug('Выбор действия, введено: %s' % choice)
                try:
                    if isinstance(choice, float):
                        raise ValueError
                    choice = int(choice)
                    if (choice < 1) or (choice > 11):
                        raise ValueError
                    not_done = False
                except ValueError:
                    print('[WARNING] Нужно одно целое число от 1 до 11. Повторите попытку.')
                    continue
            # noinspection PyUnboundLocalVariable
            match choice:
                case 1:  # Добавление книги
                    current_library.add_book()
                case 2:  # Удаление книги
                    if previous_choice != 4:  # Выведем список книг для удобства
                        current_library.view_all_books()
                    current_library.delete_book()
                case 3:  # Поиск книги
                    title, author, year = cls.what_to_find()
                    current_library.find_book(title, author, year)
                case 4:  # Отображение всех книг
                    current_library.view_all_books()
                case 5:  # Изменение статуса книги
                    if previous_choice != 4:  # Выведем список книг для удобства
                        current_library.view_all_books()
                    current_library.change_book_status(want_to_print_it_yourself=False)
                case 6:  # Ввести нестандартный статус книги
                    if previous_choice != 4:  # Выведем список книг для удобства
                        current_library.view_all_books()
                    current_library.change_book_status(want_to_print_it_yourself=True)
                case 7:  # Сменить библиотеку
                    current_library = cls.change_library()
                case 8:  # Создать библиотеку
                    cls.__libraries += (cls.create_library(),)
                    current_library = cls.__libraries[-1]
                case 9:  # Удалить библиотеку
                    deleted_library = cls.delete_library()
                    if deleted_library is current_library:
                        if len(cls.__libraries) != 0:
                            current_library = cls.__libraries[0]
                        else:
                            print('[WARNING] В системе не осталось библиотек')
                            cls.__libraries += (cls.create_library(),)
                            current_library = cls.__libraries[-1]
                case 10:  # Завершить работу
                    print('[INFO] Завершение работы')
                    JsonConverter.save_json(cls.__libraries, save_json_path)
                    work = False
                    print('[INFO] Программа остановлена')
                case 11:  # Отстань, я - Программист
                    print('Обращение к тому, кто это читает:\n'
                          'А можно мне пожалуйста в любом случае какой-то фитбек по коду?\n'
                          'Не хватает вот этого самого код-ревью от более умных\n'
                          'Хоть какой-то, можно матом.\n'
                          'https://t.me/spirinis')
                    work = False
            previous_choice = choice

    @staticmethod
    def what_to_find() -> tuple[str, str, int]:
        """Функция интерфейса. Сформирует запрос для поиска книги"""
        not_done = True
        while not_done:
            print('[INFO] Поиск книги:')
            user_input_title = input("Введите заголовок книги или пустой ввод, если по заголовку не искать\n>>> ")
            user_input_author = input("Введите имя автора книги или пустой ввод, если по автору не искать\n>>> ")
            user_input_year = input("Введите год выпуска книги или пустой ввод, если по году выпуска не искать\n>>> ")
            logger.debug('Введено: заголовок %s, автор %s, год %s' %
                         (user_input_title, user_input_author, user_input_year))
            if bool(user_input_year):
                try:
                    if type(user_input_year) is float:
                        raise ValueError
                    year = int(user_input_year)
                    not_done = False
                except ValueError:
                    print('[WARNING] Год должен быть целым числом. Повторите попытку.')
                    continue
            else:
                not_done = False
                year = None
        # noinspection PyUnboundLocalVariable
        return user_input_title, user_input_author, year

    @classmethod
    def print_libraries(cls) -> None:
        """Пользовательская функция. Выведет список библиотек"""
        print('[INFO] В системе содержатся следующие библиотеки:')
        library_number = 1
        for library in cls.__libraries:
            print(f'{library_number:>5} ' + library.__str__())
            library_number += 1

    @classmethod
    def change_library(cls) -> Library:
        """Пользовательская функция. Установит выбранную библиотеку текущей"""
        print('[INFO] Выбор библиотеки:')
        cls.print_libraries()
        not_done = True
        while not_done:
            user_input_number = input("Введите номер требуемой библиотеки\n>>> ")
            logger.debug('Введено: %s' % user_input_number)
            try:
                if type(user_input_number) is float:
                    raise ValueError
                number = int(user_input_number)
                if (number < 1) or (number > len(cls.__libraries)):
                    raise ValueError
                not_done = False
            except ValueError:
                print(f'[WARNING] Номер должен быть целым числом в диапазоне от 1 до {len(cls.__libraries)}.'
                      f' Повторите попытку.')
                continue
        # noinspection PyUnboundLocalVariable
        return cls.__libraries[number - 1]

    @staticmethod
    def create_library() -> Library:
        """Пользовательская функция. Создаст библиотеку"""
        print('[INFO] Создание библиотеки:')
        library_name = input('Введите имя новой библиотеки\n>>> ')
        logger.debug('Введено: %s' % library_name)
        library: Library = Library(library_name)
        print(f'[INFO] Библиотека \'{library.name}\' создана:')
        return library

    @classmethod
    def delete_library(cls) -> Library | None:
        """Пользовательская функция. Удалит библиотеку"""
        print('[INFO] Выбор библиотеки:')
        cls.print_libraries()
        not_done = True
        while not_done:
            user_input_number = input("Введите номер удаляемой библиотеки\n>>> ")
            logger.debug('Введено: %s' % user_input_number)
            try:
                if type(user_input_number) is float:
                    raise ValueError
                number = int(user_input_number)
                if (number < 1) or (number > len(cls.__libraries)):
                    raise ValueError
                not_done = False
            except ValueError:
                print(f'[WARNING] Номер должен быть целым числом в диапазоне от 1 до {len(cls.__libraries)}.'
                      f' Повторите попытку.')
                continue
        # noinspection PyUnboundLocalVariable
        number -= 1
        print(f'[WARNING] Вы удаляете библиотеку: \'{cls.__libraries[number].name}\'\n'
              f'Подтвердить - пустой ввод/Y/y\n'
              f'Отменить - всё остальное')
        answer = input('>>> ')
        logger.debug('Введено: %s' % answer)
        if answer in ('', 'Y', 'y'):
            libraries_list = list(cls.__libraries)
            deleted_library = libraries_list.pop(number)
            cls.__libraries = tuple(libraries_list)
            print(f'[INFO] {deleted_library.__str__()} удалена')
            return deleted_library
        else:
            print(f'[INFO] Библиотека не удалена')
            return None


def create_logger(level: int) -> logging.Logger:
    """Создание и настройка логера"""
    logger_ = logging.getLogger(__name__)
    logger_.setLevel(level)
    # noinspection SpellCheckingInspection
    log_format = "%(asctime)s | %(levelname)s | %(funcName)s() | %(message)s"
    formatter = logging.Formatter(log_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger_.addHandler(stream_handler)
    file_handler = logging.FileHandler(filename="logs/main.log", mode="w")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger_.addHandler(file_handler)
    return logger_


logger = create_logger(logging.ERROR)
if __name__ == '__main__':
    Client.start('libraries.json', 'libraries.json')
