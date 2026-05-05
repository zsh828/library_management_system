from src.library import Library, Book
import pytest


class TestLibraryAddBook:
    """Tests for adding books to the library."""

    def test_add_new_book_success(self):
        """Test adding a new book with unique ISBN."""
        lib = Library()
        result = lib.add_book("The Great Gatsby", "F. Scott Fitzgerald", "1234567890")
        assert result is True
        assert len(lib.list_all_books()) == 1

    def test_add_duplicate_book_fails(self):
        """Test that adding a book with an existing ISBN fails."""
        lib = Library()
        lib.add_book("The Great Gatsby", "F. Scott Fitzgerald", "1234567890")
        result = lib.add_book("Another Book", "Some Author", "1234567890")
        assert result is False
        assert len(lib.list_all_books()) == 1

    def test_add_multiple_unique_books(self):
        """Test adding multiple books with different ISBNs."""
        lib = Library()
        lib.add_book("Book A", "Author A", "ISBN_A")
        lib.add_book("Book B", "Author B", "ISBN_B")
        assert len(lib.list_all_books()) == 2

    def test_add_book_with_empty_fields(self):
        """Test adding a book with empty strings (allowed by current spec, but verify behavior)."""
        lib = Library()
        # Empty strings are valid inputs unless specified otherwise
        result = lib.add_book("", "", "")
        assert result is True
        assert len(lib.list_all_books()) == 1


class TestLibraryQueryBooks:
    """Tests for querying/searching books."""

    def setup_method(self):
        """Set up a library with some initial data for each test."""
        self.lib = Library()
        self.lib.add_book("Python Programming", "John Doe", "111")
        self.lib.add_book("Java Basics", "Jane Smith", "222")
        self.lib.add_book("Python Advanced", "John Doe", "333")

    def test_search_by_exact_isbn(self):
        """Test searching for a book by exact ISBN."""
        results = self.lib.search_books("111")
        assert len(results) == 1
        assert results[0].isbn == "111"
        assert results[0].title == "Python Programming"

    def test_search_by_partial_title(self):
        """Test searching for books by partial title match."""
        results = self.lib.search_books("Python")
        assert len(results) == 2
        titles = [book.title for book in results]
        assert "Python Programming" in titles
        assert "Python Advanced" in titles

    def test_search_by_non_existent_query(self):
        """Test searching for a book that doesn't exist."""
        results = self.lib.search_books("NonExistentTitle")
        assert len(results) == 0

    def test_search_by_non_existent_isbn(self):
        """Test searching for an ISBN that doesn't exist."""
        results = self.lib.search_books("999")
        assert len(results) == 0

    def test_get_book_by_isbn_found(self):
        """Test retrieving a specific book by ISBN."""
        book = self.lib.get_book_by_isbn("222")
        assert book is not None
        assert book.title == "Java Basics"

    def test_get_book_by_isbn_not_found(self):
        """Test retrieving a non-existent book by ISBN."""
        book = self.lib.get_book_by_isbn("999")
        assert book is None

    def test_case_insensitive_title_search(self):
        """Test that title search is case-insensitive."""
        results_upper = self.lib.search_books("PYTHON")
        results_lower = self.lib.search_books("python")
        assert len(results_upper) == len(results_lower) == 2


class TestLibraryDeleteBook:
    """Tests for deleting books."""

    def setup_method(self):
        """Set up a library with some initial data."""
        self.lib = Library()
        self.lib.add_book("Book One", "Author One", "100")
        self.lib.add_book("Book Two", "Author Two", "200")

    def test_delete_existing_book(self):
        """Test deleting a book that exists."""
        result = self.lib.delete_book("100")
        assert result is True
        assert len(self.lib.list_all_books()) == 1
        assert self.lib.get_book_by_isbn("100") is None

    def test_delete_non_existent_book(self):
        """Test deleting a book that does not exist."""
        result = self.lib.delete_book("999")
        assert result is False
        assert len(self.lib.list_all_books()) == 2

    def test_delete_removes_correct_book(self):
        """Test that the correct book is removed and others remain."""
        self.lib.delete_book("100")
        remaining = self.lib.list_all_books()
        assert len(remaining) == 1
        assert remaining[0].isbn == "200"


class TestLibraryListAllBooks:
    """Tests for listing all books."""

    def test_list_empty_library(self):
        """Test listing books when the library is empty."""
        lib = Library()
        books = lib.list_all_books()
        assert books == []

    def test_list_all_books(self):
        """Test listing all books in the library."""
        lib = Library()
        lib.add_book("A", "Auth A", "1")
        lib.add_book("B", "Auth B", "2")
        lib.add_book("C", "Auth C", "3")
        
        books = lib.list_all_books()
        assert len(books) == 3
        
        # Verify content integrity
        isbns = [book.isbn for book in books]
        assert "1" in isbns
        assert "2" in isbns
        assert "3" in isbns

    def test_list_returns_copy_or_independent_list(self):
        """Ensure that modifying the returned list doesn't affect internal state (optional check based on implementation)."""
        lib = Library()
        lib.add_book("A", "Auth A", "1")
        
        books = lib.list_all_books()
        # Clear the returned list
        books.clear()
        
        # Internal library should still have the book
        assert len(lib.list_all_books()) == 1