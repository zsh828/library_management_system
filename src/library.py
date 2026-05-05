"""
Library Management System Core Logic
Supports adding, querying, deleting, and listing books.
"""

from typing import List, Dict, Optional


class Book:
    """Represents a single book in the library."""
    
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def to_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn
        }

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return self.isbn == other.isbn

    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"


class Library:
    """Manages a collection of books."""
    
    def __init__(self):
        # Using ISBN as the unique key for efficient lookup
        self._books: Dict[str, Book] = {}

    def add_book(self, title: str, author: str, isbn: str) -> bool:
        """
        Add a book to the library.
        
        Args:
            title: The title of the book.
            author: The author of the book.
            isbn: The ISBN of the book (must be unique).
            
        Returns:
            True if the book was added successfully, False if it already exists.
        """
        if isbn in self._books:
            return False
        
        new_book = Book(title=title, author=author, isbn=isbn)
        self._books[isbn] = new_book
        return True

    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """Retrieve a book by its ISBN."""
        return self._books.get(isbn)

    def get_book_by_title(self, title: str) -> List[Book]:
        """Retrieve all books matching the given title (case-insensitive partial match)."""
        matches = []
        for book in self._books.values():
            if title.lower() in book.title.lower():
                matches.append(book)
        return matches

    def search_books(self, query: str) -> List[Book]:
        """
        Search books by title or ISBN.
        
        Args:
            query: The search term.
            
        Returns:
            A list of matching books.
        """
        # First try exact ISBN match
        if query in self._books:
            return [self._books[query]]
        
        # Then try title search
        title_matches = self.get_book_by_title(query)
        
        # Combine results (avoid duplicates if ISBN happened to match title logic, though unlikely)
        seen_isbns = set()
        result = []
        
        for book in title_matches:
            if book.isbn not in seen_isbns:
                result.append(book)
                seen_isbns.add(book.isbn)
                
        return result

    def delete_book(self, isbn: str) -> bool:
        """
        Delete a book by its ISBN.
        
        Args:
            isbn: The ISBN of the book to delete.
            
        Returns:
            True if the book was deleted, False if it didn't exist.
        """
        if isbn in self._books:
            del self._books[isbn]
            return True
        return False

    def list_all_books(self) -> List[Book]:
        """Return a list of all books in the library."""
        return list(self._books.values())