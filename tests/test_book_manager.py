import pytest
from src.book_manager import LibraryManager, Book


class TestLibraryManager:
    @pytest.fixture
    def manager(self):
        return LibraryManager()

    def test_add_book_success(self, manager):
        """测试成功添加一本新图书"""
        result = manager.add_book("Python编程", "Guido", "1234567890")
        assert result is True
        assert len(manager.list_all_books()) == 1
        assert manager.books["1234567890"].title == "Python编程"

    def test_add_book_duplicate_isbn(self, manager):
        """测试添加重复ISBN的图书"""
        manager.add_book("Python编程", "Guido", "1234567890")
        result = manager.add_book("Java编程", "James", "1234567890")
        assert result is False
        assert len(manager.list_all_books()) == 1

    def test_add_book_empty_fields(self, manager):
        """测试添加字段为空的图书应抛出异常"""
        with pytest.raises(ValueError):
            manager.add_book("", "Author", "123")
        with pytest.raises(ValueError):
            manager.add_book("Title", "", "123")
        with pytest.raises(ValueError):
            manager.add_book("Title", "Author", "")

    def test_search_by_title(self, manager):
        """测试按书名搜索"""
        manager.add_book("Python编程", "Guido", "123")
        manager.add_book("Java编程", "James", "456")
        
        results = manager.search_books("Python")
        assert len(results) == 1
        assert results[0].title == "Python编程"

    def test_search_by_isbn(self, manager):
        """测试按ISBN搜索"""
        manager.add_book("Python编程", "Guido", "123456")
        manager.add_book("Java编程", "James", "789012")
        
        results = manager.search_books("123456")
        assert len(results) == 1
        assert results[0].isbn == "123456"

    def test_search_case_insensitive(self, manager):
        """测试搜索不区分大小写"""
        manager.add_book("PYTHON Programming", "Guido", "123")
        
        results = manager.search_books("python")
        assert len(results) == 1

    def test_search_no_match(self, manager):
        """测试搜索无结果"""
        manager.add_book("Python编程", "Guido", "123")
        results = manager.search_books("NonExistent")
        assert len(results) == 0

    def test_search_empty_keyword(self, manager):
        """测试空关键字搜索"""
        manager.add_book("Python编程", "Guido", "123")
        results = manager.search_books("")
        assert len(results) == 0

    def test_delete_book_success(self, manager):
        """测试成功删除图书"""
        manager.add_book("Python编程", "Guido", "123")
        result = manager.delete_book("123")
        assert result is True
        assert len(manager.list_all_books()) == 0

    def test_delete_book_not_found(self, manager):
        """测试删除不存在的图书"""
        result = manager.delete_book("999")
        assert result is False

    def test_delete_book_empty_isbn(self, manager):
        """测试删除时ISBN为空应抛出异常"""
        with pytest.raises(ValueError):
            manager.delete_book("")

    def test_list_all_books(self, manager):
        """测试列出所有图书"""
        manager.add_book("Book A", "Author A", "111")
        manager.add_book("Book B", "Author B", "222")
        
        books = manager.list_all_books()
        assert len(books) == 2
        titles = [b.title for b in books]
        assert "Book A" in titles
        assert "Book B" in titles

    def test_list_all_books_empty(self, manager):
        """测试空图书馆列出所有图书"""
        books = manager.list_all_books()
        assert len(books) == 0