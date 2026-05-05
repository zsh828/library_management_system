import pytest
from src.library import Library, Book


class TestBook:
    """Tests for the Book class."""

    def test_book_creation(self):
        book = Book("Python Crash Course", "Eric Matthes", "978-1593279288")
        assert book.title == "Python Crash Course"
        assert book.author == "Eric Matthes"
        assert book.isbn == "978-1593279288"

    def test_book_repr(self):
        book = Book("Test Book", "Test Author", "1234567890")
        expected_repr = "Book(title='Test Book', author='Test Author', isbn='1234567890')"
        assert repr(book) == expected_repr


class TestLibraryAddBook:
    """Tests for adding books."""

    def setup_method(self):
        self.library = Library()

    def test_add_new_book_success(self):
        result = self.library.add_book("Clean Code", "Robert C. Martin", "978-0132350884")
        assert result is True
        assert len(self.library.list_all_books()) == 1

    def test_add_duplicate_isbn_fails(self):
        self.library.add_book("Book A", "Author A", "ISBN1")
        result = self.library.add_book("Book B", "Author B", "ISBN1")
        assert result is False
        # Should still only have one book
        assert len(self.library.list_all_books()) == 1

    def test_add_empty_title_raises_error(self):
        with pytest.raises(ValueError):
            self.library.add_book("", "Author", "ISBN1")

    def test_add_empty_author_raises_error(self):
        with pytest.raises(ValueError):
            self.library.add_book("Title", "", "ISBN1")

    def test_add_empty_isbn_raises_error(self):
        with pytest.raises(ValueError):
            self.library.add_book("Title", "Author", "")


class TestLibrarySearchAndQuery:
    """Tests for searching and retrieving books."""

    def setup_method(self):
        self.library = Library()
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565")
        self.library.add_book("To Kill a Mockingbird", "Harper Lee", "978-0061120084")
        self.library.add_book("1984", "George Orwell", "978-0451524935")

    def test_get_book_by_isbn_found(self):
        book = self.library.get_book_by_isbn("978-0743273565")
        assert book is not None
        assert book.title == "The Great Gatsby"

    def test_get_book_by_isbn_not_found(self):
        book = self.library.get_book_by_isbn("000-0000000000")
        assert book is None

    def test_search_by_title_partial_match(self):
        results = self.library.search_books("Great")
        assert len(results) == 1
        assert results[0].title == "The Great Gatsby"

    def test_search_by_title_case_insensitive(self):
        results = self.library.search_books("gatsby")
        assert len(results) == 1
        assert results[0].title == "The Great Gatsby"

    def test_search_by_isbn(self):
        results = self.library.search_books("978-0061120084")
        assert len(results) == 1
        assert results[0].title == "To Kill a Mockingbird"

    def test_search_no_results(self):
        results = self.library.search_books("NonExistentBook")
        assert len(results) == 0

    def test_search_empty_query(self):
        results = self.library.search_books("")
        assert len(results) == 0


class TestLibraryRemoveBook:
    """Tests for removing books."""

    def setup_method(self):
        self.library = Library()
        self.library.add_book("Book A", "Author A", "ISBN_A")
        self.library.add_book("Book B", "Author B", "ISBN_B")

    def test_remove_existing_book(self):
        result = self.library.remove_book("ISBN_A")
        assert result is True
        assert len(self.library.list_all_books()) == 1

    def test_remove_non_existing_book(self):
        result = self.library.remove_book("ISBN_Z")
        assert result is False
        assert len(self.library.list_all_books()) == 2

    def test_remove_last_book(self):
        self.library.remove_book("ISBN_A")
        self.library.remove_book("ISBN_B")
        assert len(self.library.list_all_books()) == 0


class TestLibraryListAllBooks:
    """Tests for listing all books."""

    def setup_method(self):
        self.library = Library()

    def test_list_empty_library(self):
        books = self.library.list_all_books()
        assert books == []

    def test_list_multiple_books(self):
        self.library.add_book("Book 1", "Author 1", "111")
        self.library.add_book("Book 2", "Author 2", "222")
        
        books = self.library.list_all_books()
        assert len(books) == 2
        
        # Check content integrity
        titles = [b.title for b in books]
        assert "Book 1" in titles
        assert "Book 2" in titles