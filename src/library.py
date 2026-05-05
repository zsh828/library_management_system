"""
Library Management System Core Logic.
Supports adding, querying, deleting, and listing books.
"""


class Book:
    """Represents a single book."""
    
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"


class Library:
    """Manages a collection of books."""

    def __init__(self):
        # Using a dictionary for O(1) lookup by ISBN, which is unique
        self._books = {} 

    def add_book(self, title: str, author: str, isbn: str) -> bool:
        """
        Add a book to the library.
        
        Args:
            title: The title of the book.
            author: The author of the book.
            isbn: The ISBN of the book (must be unique).
            
        Returns:
            True if added successfully, False if ISBN already exists.
        """
        if not title or not author or not isbn:
            raise ValueError("Title, Author, and ISBN cannot be empty.")
            
        if isbn in self._books:
            return False
        
        self._books[isbn] = Book(title, author, isbn)
        return True

    def get_book_by_isbn(self, isbn: str) -> Book | None:
        """Retrieve a book by its ISBN."""
        return self._books.get(isbn)

    def search_books(self, query: str) -> list:
        """
        Search books by title or ISBN.
        
        Args:
            query: The search string.
            
        Returns:
            A list of matching Book objects.
        """
        if not query:
            return []
        
        results = []
        query_lower = query.lower()
        
        for book in self._books.values():
            if query_lower in book.title.lower() or query_lower in book.isbn:
                results.append(book)
                
        return results

    def remove_book(self, isbn: str) -> bool:
        """
        Remove a book by ISBN.
        
        Args:
            isbn: The ISBN of the book to remove.
            
        Returns:
            True if removed successfully, False if not found.
        """
        if isbn in self._books:
            del self._books[isbn]
            return True
        return False

    def list_all_books(self) -> list:
        """Return a list of all books in the library."""
        return list(self._books.values())