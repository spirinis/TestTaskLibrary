# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from unittest.mock import patch
import logging
from copy import deepcopy

# добавляем корень проекта в PYTHONPATH для запуска впервые на компьютере проверяющего
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import main


class Mock(TestCase):
    book = main.Book(1, 'title', 'author', 1)
    book2 = main.Book(2, 'title2', 'author2', 2)
    library = main.Library('name')
    library._Library__stored_ids.append(1)
    library._Library__stored_books.append(book)
    library2 = main.Library('name2')
    library2._Library__stored_ids.append(2)
    library2._Library__stored_books.append(book)


class BookTest(TestCase):
    def test_change_standard_status(self):
        book = deepcopy(Mock.book)
        book.change_standard_status()
        self.assertEqual(book.status, 'выдана')
        book.change_standard_status()
        self.assertEqual(book.status, 'в наличии')


class LibraryTest(TestCase):
    def test__find_book_by_id(self):
        self.assertEqual(Mock.library._find_book_by_id(1), Mock.book)

    def test__find_book_by_id_none(self):
        self.assertEqual(Mock.library._find_book_by_id(2), None)

    def test_load(self):
        empty_library = main.Library('name')
        empty_library.load([Mock.book, Mock.book2])

        self.assertIn(Mock.book, empty_library.stored_books)
        self.assertIn(Mock.book2, empty_library.stored_books)

    def test_load_asserts(self):
        with self.assertRaises(AssertionError):
            Mock.library.load([Mock.book, Mock.book2])
        with self.assertRaises(AssertionError):
            Mock.library.load([Mock.book, Mock.book])


class JsonConverterTest(TestCase):
    def test_default(self):
        libraries = (Mock.library, Mock.library2)
        self.assertEqual(main.JsonConverter.MyEncoder.default(libraries),
                         {'Library(name)': {'Book(title, author, 1, в наличии)': 1},
                          'Library(name2)': {'Book(title, author, 1, в наличии)': 2}})

    def test_open_json(self):
        self.assertEqual(main.JsonConverter.open_json('mock.json'),
                         {'Library(One_more_since_we_can)': {'Book(PEP 20, Тим Петерс, 1999, выдана)': 1}})

    def test_split_str(self):
        self.assertEqual(main.JsonConverter.split_str('Book(some, some1, some2)'),
                         ('some', 'some1', 'some2'))

    def test_add_books_from_dict(self):
        self.assertEqual(main.JsonConverter.add_books_from_dict(
            {Mock.book.__repr__(): 1, Mock.book2.__repr__(): 2}),
            [Mock.book, Mock.book2])


if __name__ == '__main__':
    unittest.main()
