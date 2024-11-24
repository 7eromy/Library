import json
from typing import List,  Dict, Union

Book = Dict[str, Union[int, str]]
class Library:
    def __init__(self, filename: str = "library.json"):
        """
        Инициализация библиотеки.
        :param filename: Имя файла для хранения данных.
        """
        self.filename = filename
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Загрузка данных из файла."""
        try:
            with open(self.filename, "r") as file:
                self.books = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books(self) -> None:
        """Сохранение данных в файл."""
        with open(self.filename, "w") as file:
            json.dump(self.books, file, indent=4, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: str) -> None:
        """
        Добавление книги в библиотеку.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания.
        """
        if any(book for book in self.books if book["title"].lower() == title.lower()
                                              and book["author"].lower() == author.lower() and book["year"] == year):
            print("Данная книга уже существует в библиотеке.")
            return
        if not title.strip():
            print("Ошибка: Название книги не может быть пустым.")
            return
        if not author.strip():
            print("Ошибка: Автор книги не может быть пустым.")
            return
        try:
            int(year)
        except ValueError:
            print("Ошибка: Год издания должен быть числом.")
            return
        # Находим первый свободный ID
        existing_ids = {book["id"] for book in self.books}
        new_id = 1
        while new_id in existing_ids:
            new_id += 1
        new_book = {
            "id": new_id,
            "title": title,
            "author": author,
            "year": year,
            "status": "в наличии"
        }
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' успешно добавлена!")

    def remove_book(self, book_id: int) -> None:
        """
        Удаление книги по ID.
        :param book_id: ID книги.
        """
        book = next((b for b in self.books if b["id"] == book_id), None)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга с ID {book_id} успешно удалена!")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, key: str, value: str) -> List[Book]:
        """
        Поиск книг по заданному полю.
        :param key: Поле для поиска ('title', 'author', 'year').
        :param value: Значение для поиска.
        :return: Список найденных книг.
        """
        if key in ["title", "author", "year"]:
            return [book for book in self.books if value.lower() in str(book[key]).lower()]
        else:
            print("Некорректное поле для поиска. Доступны: 'title', 'author', 'year'.")

    def display_books(self) -> None:
        """Отображение всех книг в библиотеке."""
        if not self.books:
            print("Библиотека пуста.")
            return
        for book in self.books:
            print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                  f"Год: {book['year']}, Статус: {book['status']}")

    def update_status(self, book_id: int, status: str) -> None:
        """
        Изменение статуса книги.
        :param book_id: ID книги.
        :param status: Новый статус ('в наличии', 'выдана').
        """
        book = next((b for b in self.books if b["id"] == book_id), None)
        if book:
            if status in ["в наличии", "выдана"]:
                book["status"] = status
                self.save_books()
                print(f"Статус книги с ID {book_id} изменен на '{status}'.")
            else:
                print("Некорректный статус. Доступны: 'в наличии', 'выдана'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")


def main():
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книг")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            library.add_book(title, author, year)

        elif choice == "2":
            try:
                book_id = int(input("Введите ID книги для удаления: "))
                library.remove_book(book_id)
            except ValueError:
                print("Некорректный ID.")

        elif choice == "3":
            key = input("Введите поле для поиска (title, author, year): ")
            if key in ["title", "author", "year"]:
                value = input("Введите значение для поиска: ")
                results = library.search_books(key, value)
                if results:
                    for book in results:
                        print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                              f"Год: {book['year']}, Статус: {book['status']}")
                else:
                    print("Книги не найдены.")
            else:
                print("Некорректное поле для поиска. Доступны: 'title', 'author', 'year'.")

        elif choice == "4":
            library.display_books()

        elif choice == "5":
            try:
                book_id = int(input("Введите ID книги: "))
                status = input("Введите новый статус ('в наличии' или 'выдана'): ")
                library.update_status(book_id, status)
            except ValueError:
                print("Некорректный ID.")

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
