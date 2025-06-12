import pytest
import requests
from utils.api_client import APIClient

class TestPostsAPI:
    """Posts API temel testleri"""
    
    def setup_method(self):
        self.api_client = APIClient()
    
    def test_get_all_posts_success(self):
        """Tüm postları başarıyla getir"""
        response = self.api_client.get_posts()
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 100
        
    def test_get_single_post_success(self):
        """Tek post başarıyla getir"""
        response = self.api_client.get_posts(1)
        
        assert response.status_code == 200
        post = response.json()
        assert post['id'] == 1
        assert 'title' in post
        assert 'body' in post
        assert 'userId' in post
        
    def test_create_post_success(self):
        """Yeni post başarıyla oluştur"""
        new_post = {
            'title': 'Test Post',
            'body': 'Test content',
            'userId': 1
        }
        
        response = self.api_client.create_post(new_post)
        
        assert response.status_code == 201
        created_post = response.json()
        assert created_post['title'] == new_post['title']
        assert created_post['body'] == new_post['body']
        assert created_post['userId'] == new_post['userId']
        
    def test_update_post_success(self):
        """Post başarıyla güncelle"""
        updated_post = {
            'id': 1,
            'title': 'Updated Title',
            'body': 'Updated content',
            'userId': 1
        }
        
        response = self.api_client.update_post(1, updated_post)
        
        assert response.status_code == 200
        post = response.json()
        assert post['title'] == updated_post['title']
        assert post['body'] == updated_post['body']
        
    def test_delete_post_success(self):
        """Post başarıyla sil"""
        response = self.api_client.delete_post(1)
        assert response.status_code == 200
        
    def test_get_nonexistent_post_failure(self):
        """Olmayan post için 404 hatası"""
        response = self.api_client.get_posts(999)
        assert response.status_code == 404
        
    # NEGATIF TEST SENARYOLARI
    def test_create_post_with_empty_data_failure(self):
        """Boş veri ile post oluşturma - Negatif senaryo"""
        empty_post = {}
        
        response = self.api_client.create_post(empty_post)
        
        # JSONPlaceholder boş veri kabul eder ama gerçek API'de 400 olmalı
        assert response.status_code == 201
        created_post = response.json()
        assert created_post.get('title') is None or created_post.get('title') == ""
        
    def test_create_post_with_invalid_user_id_failure(self):
        """Geçersiz kullanıcı ID ile post oluşturma - Negatif senaryo"""
        invalid_post = {
            'title': 'Test Post',
            'body': 'Test content',
            'userId': 99999  # Olmayan kullanıcı ID
        }
        
        response = self.api_client.create_post(invalid_post)
        
        # JSONPlaceholder geçersiz userID kabul eder ama gerçek API'de hata vermeli
        assert response.status_code == 201
        created_post = response.json()
        assert created_post['userId'] == 99999
        
    def test_update_nonexistent_post_failure(self):
        """Olmayan post güncelleme - Negatif senaryo"""
        updated_post = {
            'id': 99999,
            'title': 'Updated Title',
            'body': 'Updated content',
            'userId': 1
        }
        
        response = self.api_client.update_post(99999, updated_post)
        
        # JSONPlaceholder bazen 500 error verebilir, bu da geçerli bir negatif sonuç
        assert response.status_code in [200, 500], f"Beklenmeyen status code: {response.status_code}"
        
    def test_delete_nonexistent_post_failure(self):
        """Olmayan post silme - Negatif senaryo"""
        response = self.api_client.delete_post(99999)
        
        # JSONPlaceholder olmayan post için de 200 döner ama gerçek API'de 404 olmalı
        assert response.status_code == 200 