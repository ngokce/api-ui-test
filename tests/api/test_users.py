import pytest
import requests
from utils.api_client import APIClient


class TestUsersAPI:
    """Users API temel testleri"""
    
    def setup_method(self):
        self.api_client = APIClient()
    
    def test_get_all_users_success(self):
        """Tüm kullanıcıları başarıyla getir"""
        response = self.api_client.get_users()
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 10
        
    def test_get_single_user_success(self):
        """Tek kullanıcı başarıyla getir"""
        response = self.api_client.get_users(1)
        
        assert response.status_code == 200
        user = response.json()
        assert user['id'] == 1
        assert 'name' in user
        assert 'email' in user
        assert 'address' in user
        
    def test_get_nonexistent_user_failure(self):
        """Olmayan kullanıcı için 404 hatası"""
        response = self.api_client.get_users(999)
        assert response.status_code == 404
        
    def test_user_email_format_validation(self):
        """Kullanıcı email formatını doğrula"""
        response = self.api_client.get_users(1)
        user = response.json()
        
        assert '@' in user['email']
        assert '.' in user['email']
        
    def test_user_address_structure(self):
        """Kullanıcı adres yapısını doğrula"""
        response = self.api_client.get_users(1)
        user = response.json()
        
        address = user['address']
        assert 'street' in address
        assert 'city' in address
        assert 'zipcode' in address
        
    # NEGATIF TEST SENARYOLARI
    def test_get_user_with_invalid_id_format_failure(self):
        """Geçersiz ID formatı ile kullanıcı getirme - Negatif senaryo"""
        # String ID yerine sayı beklenir
        response = self.api_client.session.get(f"{self.api_client.base_url}/users/abc")
        
        # Geçersiz format için 404 beklenir
        assert response.status_code == 404
        
    def test_get_user_with_negative_id_failure(self):
        """Negatif ID ile kullanıcı getirme - Negatif senaryo"""
        response = self.api_client.get_users(-1)
        
        # Negatif ID için 404 beklenir
        assert response.status_code == 404
        
    def test_get_user_with_zero_id_failure(self):
        """Sıfır ID ile kullanıcı getirme - Negatif senaryo"""
        response = self.api_client.get_users(0)
        
        # JSONPlaceholder sıfır ID için tüm kullanıcıları döner (beklenmeyen davranış)
        assert response.status_code == 200
        users = response.json()
        # Bu negatif senaryoda beklenmeyen davranış gözlemleniyor
        assert isinstance(users, list), "Sıfır ID için beklenmeyen response formatı"