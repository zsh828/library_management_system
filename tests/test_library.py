import pytest
from src.book_manager import LibraryManager, Book


class TestLibraryOperations:
    """针对图书馆整体操作的测试用例"""

    @pytest.fixture
    def library(self):
        return LibraryManager()

    def test_initial_state_is_empty(self, library):
        """验证初始状态下图书馆为空"""
        assert library.list_all_books() == []
        assert len(library.books) == 0

    def test_multiple_books_can_be_added(self, library):
        """验证可以添加多本不同的书"""
        library.add_book("Book 1", "Author 1", "ISBN1")
        library.add_book("Book 2", "Author 2", "ISBN2")
        library.add_book("Book 3", "Author 3", "ISBN3")
        
        books = library.list_all_books()
        assert len(books) == 3
        titles = {b.title for b in books}
        assert titles == {"Book 1", "Book 2", "Book 3"}

    def test_delete_removes_book_from_collection(self, library):
        """验证删除后书籍不再存在于内部字典中"""
        library.add_book("Test Book", "Test Author", "111")
        library.delete_book("111")
        assert "111" not in library.books

    def test_search_returns_correct_type(self, library):
        """验证搜索结果返回的是列表，且元素类型为 Book"""
        library.add_book("Search Test", "Author", "999")
        results = library.search_books("Search")
        
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], Book)
            assert results[0].title == "Search Test"

    def test_complex_search_scenario(self, library):
        """复杂搜索场景：添加多本书，混合搜索"""
        library.add_book("Introduction to Python", "John Doe", "100")
        library.add_book("Advanced Java", "Jane Smith", "200")
        library.add_book("Python Data Science", "Alice Brown", "300")
        
        # 搜索 "Python" 应该匹配第1和第3本
        python_results = library.search_books("Python")
        assert len(python_results) == 2
        assert all("Python" in b.title for b in python_results)
        
        # 搜索 "Java" 应该只匹配第2本
        java_results = library.search_books("Java")
        assert len(java_results) == 1
        assert java_results[0].title == "Advanced Java"
        
        # 搜索 "Data" 应该只匹配第3本
        data_results = library.search_books("Data")
        assert len(data_results) == 1
        assert data_results[0].title == "Python Data Science"