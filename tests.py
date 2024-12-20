import pytest
from main import BooksCollector


class TestBooksCollector:

    @pytest.fixture
    def books_collector(self):
        return BooksCollector()

    @pytest.fixture
    def setup_books_with_genres(self, books_collector):
        def _add_books(books_and_genres):
            for book_name, book_genre in books_and_genres:
                books_collector.add_new_book(book_name)
                books_collector.set_book_genre(book_name, book_genre)

        return _add_books

    @pytest.fixture
    def add_book_to_favorites(self, books_collector):
        def _add_book(book_name):
            books_collector.add_new_book(book_name)
            books_collector.add_book_in_favorites(book_name)

        return _add_book

    # Добавление одной книги
    @pytest.mark.parametrize('book_name',
                             ['Война и мир',
                              'Гамлет',
                              'Сто лет одиночества',
                              'Преступление и наказание'])
    def test_add_new_book_add_one_book(self, books_collector, book_name):
        books_collector.add_new_book(book_name)
        assert book_name in books_collector.get_books_genre()
        assert len(books_collector.get_books_genre()) == 1

    # Добавление нескольких книг
    @pytest.mark.parametrize('book_names, expected_count', [
        (['Гарри Поттер', 'Дракула'], 2),
        (['Гарри Поттер', 'Властелин колец', 'Шерлок Холмс'], 3)
    ])
    def test_add_new_book_multiple_books(self, books_collector, book_names, expected_count):
        for name in book_names:
            books_collector.add_new_book(name)
        assert len(books_collector.get_books_genre()) == expected_count

    # Добавление книги с неверным именем
    @pytest.mark.parametrize('book_name',
                             ['',
                              'Преступление и наказание - социально-философский роман Фёдора Михайловича Достоевского'])
    def test_add_new_book_add_one_book_with_invalid_name(self, books_collector, book_name):
        books_collector.add_new_book(book_name)
        assert book_name not in books_collector.get_books_genre()

    # Установка жанра книги
    @pytest.mark.parametrize('book_name, book_genre',
                             [['Горе от ума', 'Комедии'],
                              ['Зелёная миля', 'Фантастика'],
                              ['Мизери', 'Ужасы'],
                              ['Малыш и Карлсон', 'Мультфильмы'],
                              ['Шерлок Холмс', 'Детективы']])
    def test_set_book_genre_add_book_and_set_genre(self, books_collector, book_name, book_genre):
        books_collector.add_new_book(book_name)
        books_collector.set_book_genre(book_name, book_genre)
        assert books_collector.get_book_genre(book_name) == book_genre

    # Неверный жанр
    def test_set_book_genre_with_invalid_genre(self, books_collector):
        books_collector.add_new_book('Гарри Поттер')
        books_collector.set_book_genre('Гарри Поттер', 'Научная фантастика')
        assert books_collector.get_book_genre('Гарри Поттер') == ''

    # Получение книг по жанру
    @pytest.mark.parametrize('books_and_genres, genre, expected_books', [
        ([('Гарри Поттер', 'Фантастика')], 'Фантастика', ['Гарри Поттер']),
        ([('Гарри Поттер', 'Фантастика')], 'Ужасы', []),
        ([('Дракула', 'Ужасы'), ('Шерлок Холмс', 'Детективы')], 'Ужасы', ['Дракула']),
        ([('Гарри Поттер', 'Фантастика'), ('Властелин колец', 'Фантастика')], 'Фантастика',
         ['Гарри Поттер', 'Властелин колец'])
    ])
    def test_get_books_with_specific_genre(self, books_collector, setup_books_with_genres, books_and_genres, genre,
                                           expected_books):
        setup_books_with_genres(books_and_genres)
        assert books_collector.get_books_with_specific_genre(genre) == expected_books

    # Получение книг для детей
    @pytest.mark.parametrize('books_and_genres, expected_books', [
        ([('Гарри Поттер', 'Фантастика')], ['Гарри Поттер']),
        ([('Дракула', 'Ужасы')], []),
        ([('Гарри Поттер', 'Фантастика'), ('Малыш и Карлсон', 'Мультфильмы')], ['Гарри Поттер', 'Малыш и Карлсон'])
    ])
    def test_get_books_for_children(self, books_collector, setup_books_with_genres, books_and_genres, expected_books):
        setup_books_with_genres(books_and_genres)
        assert books_collector.get_books_for_children() == expected_books

    # Добавление книги в избранное
    def test_add_book_in_favorites(self, books_collector, add_book_to_favorites):
        add_book_to_favorites('Гарри Поттер')
        assert 'Гарри Поттер' in books_collector.get_list_of_favorites_books()

    # Удаление книги из избранного
    def test_delete_book_from_favorites(self, books_collector, add_book_to_favorites):
        add_book_to_favorites('Гарри Поттер')
        books_collector.delete_book_from_favorites('Гарри Поттер')
        assert 'Гарри Поттер' not in books_collector.get_list_of_favorites_books()

    # Получение списка избранных книг
    def test_get_list_of_favorites_books(self, books_collector, add_book_to_favorites):
        add_book_to_favorites('Гарри Поттер')
        add_book_to_favorites('Властелин колец')
        assert books_collector.get_list_of_favorites_books() == ['Гарри Поттер', 'Властелин колец']

    # Изменение жанра книги
    def test_set_book_genre_correct_name_change_book_genre(self, books_collector):
        books_collector.add_new_book('Гарри Поттер')
        books_collector.set_book_genre('Гарри Поттер', 'Фантастика')
        books_collector.set_book_genre('Гарри Поттер', 'Комедии')
        assert books_collector.get_book_genre('Гарри Поттер') == 'Комедии'
