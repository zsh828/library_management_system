class Book:
    def __init__(self, isbn: str, title: str, author: str, price: float, stock: int = 1):
        if not isbn or not title or not author:
            raise ValueError("ISBN, title, and author cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if stock < 0:
            raise ValueError("Stock cannot be negative")
        
        self.isbn = isbn
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return self.isbn == other.isbn

    def __repr__(self):
        return f"Book(isbn='{self.isbn}', title='{self.title}', author='{self.author}', price={self.price}, stock={self.stock})"


class BorrowRecord:
    def __init__(self, user_id: str, book_isbn: str, borrow_date: str):
        if not user_id or not book_isbn:
            raise ValueError("User ID and Book ISBN cannot be empty")
        
        self.user_id = user_id
        self.book_isbn = book_isbn
        self.borrow_date = borrow_date
        self.return_date = None

    def return_book(self, return_date: str):
        if self.return_date is not None:
            raise ValueError("Book already returned")
        self.return_date = return_date

    def __repr__(self):
        status = "Returned" if self.return_date else "Borrowed"
        return f"BorrowRecord(user='{self.user_id}', isbn='{self.book_isbn}', status={status})"