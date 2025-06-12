import pytest
import requests
from utils.api_client import APIClient


class TestCommentsAPI:
    """Comments API temel testleri"""
    
    def setup_method(self):
        self.api_client = APIClient()
    
    def test_get_all_comments_success(self):
        """Tüm yorumları başarıyla getir"""
        response = self.api_client.get_comments()
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 500
        
    def test_get_comments_by_post_id(self):
        """Post ID'ye göre yorumları getir"""
        response = self.api_client.get_comments(1)
        
        assert response.status_code == 200
        comments = response.json()
        assert len(comments) > 0
        
        # Tüm yorumlar aynı post'a ait olmalı
        for comment in comments:
            assert comment['postId'] == 1
            
    def test_comment_email_validation(self):
        """Yorum email formatını doğrula"""
        response = self.api_client.get_comments()
        comments = response.json()
        
        first_comment = comments[0]
        assert '@' in first_comment['email']
        assert '.' in first_comment['email']
        
    def test_comment_content_not_empty(self):
        """Yorum içeriğinin boş olmadığını doğrula"""
        response = self.api_client.get_comments()
        comments = response.json()
        
        first_comment = comments[0]
        assert first_comment['name'].strip() != ""
        assert first_comment['body'].strip() != ""
        
    # NEGATIF TEST SENARYOLARI
    def test_get_comments_for_nonexistent_post_failure(self):
        """Olmayan post için yorum getirme - Negatif senaryo"""
        response = self.api_client.get_comments(99999)
        
        assert response.status_code == 200
        comments = response.json()
        # Olmayan post için boş array dönmeli
        assert len(comments) == 0
        
    def test_get_comments_with_invalid_post_id_failure(self):
        """Geçersiz post ID formatı ile yorum getirme - Negatif senaryo"""
        response = self.api_client.session.get(f"{self.api_client.base_url}/comments?postId=abc")
        
        assert response.status_code == 200
        comments = response.json()
        # Geçersiz format için boş array dönmeli
        assert len(comments) == 0
        
    def test_get_comments_with_negative_post_id_failure(self):
        """Negatif post ID ile yorum getirme - Negatif senaryo"""
        response = self.api_client.get_comments(-1)
        
        assert response.status_code == 200
        comments = response.json()
        # Negatif ID için boş array dönmeli
        assert len(comments) == 0 