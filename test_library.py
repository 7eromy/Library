import unittest
import os
import json
from library import Library  # Импортируем ваш класс Library

class TestLibrary(unittest.TestCase):
    def setUp(self):
        """
        Настройка перед каждым тестом.
        Создаем тестовый файл библиотеки.
        """
        self.test_file = "test_library.json"
        self.library = Library(self.test_file)

    def tearDown(self):
        """
        Очистка после каждого теста.
        Удаляем тестовый файл библиотеки.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self):
        """Проверка добавления книги."""
        self.library.add_book("Тестовая книга", "Автор", "2023")
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0]["title"], "Тестовая книга")

    def test_add_duplicate_book(self):
        """Проверка обработки добавления дубликата."""
        self.library.add_book("Тестовая книга", "Автор", "2023")
        self.library.add_book("Тестовая книга", "Автор", "2023")
        self.assertEqual(len(self.library.books), 1)

    def test_remove_book(self):
        """Проверка удаления книги."""
        self.library.add_book("Книга для удаления", "Автор", "2022")
        book_id = self.library.books[0]["id"]
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_remove_nonexistent_book(self):
        """Проверка удаления несуществующей книги."""
        self.library.remove_book(999)
        self.assertEqual(len(self.library.books), 0)

    def test_search_books(self):
        """Проверка поиска книг."""
        self.library.add_book("Книга 1", "Автор 1", "2020")
        self.library.add_book("Книга 2", "Автор 2", "2021")
        results = self.library.search_books("title", "Книга")
        self.assertEqual(len(results), 2)
        results = self.library.search_books("author", "Автор 2")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Книга 2")

    def test_update_status(self):
        """Проверка обновления статуса книги."""
        self.library.add_book("Книга для изменения статуса", "Автор", "2023")
        book_id = self.library.books[0]["id"]
        self.library.update_status(book_id, "выдана")
        self.assertEqual(self.library.books[0]["status"], "выдана")

    def test_invalid_update_status(self):
        """Проверка попытки установки некорректного статуса."""
        self.library.add_book("Книга с некорректным статусом", "Автор", "2023")
        book_id = self.library.books[0]["id"]
        self.library.update_status(book_id, "недоступна")
        self.assertNotEqual(self.library.books[0]["status"], "недоступна")

    def test_load_and_save_books(self):
        """Проверка сохранения и загрузки данных."""
        self.library.add_book("Сохраненная книга", "Автор", "2023")
        self.library.save_books()

        # Создаем новый экземпляр библиотеки и загружаем из файла
        new_library = Library(self.test_file)
        self.assertEqual(len(new_library.books), 1)
        self.assertEqual(new_library.books[0]["title"], "Сохраненная книга")


if __name__ == "__main__":
    unittest.main()
