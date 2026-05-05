class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"


class LibraryManager:
    def __init__(self):
        self.books = {}  # Key: ISBN, Value: Book object

    def add_book(self, title: str, author: str, isbn: str) -> bool:
        """添加图书。如果ISBN已存在，返回False；否则添加并返回True。"""
        if not title or not author or not isbn:
            raise ValueError("Title, author, and ISBN cannot be empty.")
        
        if isbn in self.books:
            return False
        
        self.books[isbn] = Book(title, author, isbn)
        return True

    def search_books(self, keyword: str) -> list:
        """查询图书。按书名或ISBN模糊匹配（不区分大小写）。"""
        if not keyword:
            return []
        
        keyword_lower = keyword.lower()
        results = []
        for book in self.books.values():
            if keyword_lower in book.title.lower() or keyword_lower in book.isbn:
                results.append(book)
        return results

    def delete_book(self, isbn: str) -> bool:
        """删除图书。如果ISBN存在则删除并返回True，否则返回False。"""
        if not isbn:
            raise ValueError("ISBN cannot be empty.")
        
        if isbn in self.books:
            del self.books[isbn]
            return True
        return False

    def list_all_books(self) -> list:
        """列出所有图书。"""
        return list(self.books.values())