"""
Full Stack JSONPlaceholder Uygulaması UI Testleri
API ve UI entegrasyonu testleri
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.ui_helpers import (
    navigate_to_jsonplaceholder_site,
    verify_page_title
)

class TestJSONPlaceholderUI:
    """JSONPlaceholder web sitesi UI testleri - Pozitif ve Negatif senaryolar"""
    
    # POZİTİF TEST SENARYOLARI
    def test_site_loads_successfully(self, driver):
        """JSONPlaceholder sitesinin başarıyla yüklendiğini test et"""
        assert navigate_to_jsonplaceholder_site(driver), "JSONPlaceholder sitesi yüklenemedi"
        
    def test_page_title(self, driver):
        """Sayfa başlığını test et"""
        navigate_to_jsonplaceholder_site(driver)
        assert verify_page_title(driver, "JSONPlaceholder"), "Sayfa başlığı doğru değil"
        
    def test_posts_endpoint_access(self, driver):
        """Posts endpoint'ine erişimi test et"""
        driver.get("https://jsonplaceholder.typicode.com/posts")
        time.sleep(2)
        
        # JSON formatında veri olduğunu doğrula
        page_source = driver.page_source
        assert '"userId"' in page_source or '"id"' in page_source, "Posts JSON response görüntülenmiyor"
        
    def test_users_endpoint_access(self, driver):
        """Users endpoint'ine erişimi test et"""
        driver.get("https://jsonplaceholder.typicode.com/users")
        time.sleep(2)
        
        # User verilerinin olduğunu doğrula
        page_source = driver.page_source
        assert '"name"' in page_source or '"email"' in page_source, "Users JSON response görüntülenmiyor"
        
    def test_comments_endpoint_access(self, driver):
        """Comments endpoint'ine erişimi test et"""
        driver.get("https://jsonplaceholder.typicode.com/comments")
        time.sleep(2)
        
        # Comments verilerinin olduğunu doğrula
        page_source = driver.page_source
        assert '"postId"' in page_source or '"email"' in page_source, "Comments JSON response görüntülenmiyor"
        
    def test_single_post_display(self, driver):
        """Tek bir post'un görüntülendiğini test et"""
        driver.get("https://jsonplaceholder.typicode.com/posts/1")
        time.sleep(2)
        
        # Post verilerinin olduğunu doğrula
        page_source = driver.page_source
        assert '"userId": 1' in page_source or '"id": 1' in page_source, "Tek post görüntülenmiyor"
        
    def test_json_format_validation(self, driver):
        """JSON formatının geçerli olduğunu test et"""
        driver.get("https://jsonplaceholder.typicode.com/posts/1")
        time.sleep(2)
        
        page_source = driver.page_source
        
        # JSON formatı kontrolü
        assert page_source.count('{') > 0, "JSON açılış parantezi bulunamadı"
        assert page_source.count('}') > 0, "JSON kapanış parantezi bulunamadı"
        assert '"' in page_source, "JSON string formatı bulunamadı"
        
    def test_endpoint_accessibility(self, driver):
        """API endpoint'lerinin erişilebilir olduğunu test et"""
        endpoints = [
            "https://jsonplaceholder.typicode.com/posts",
            "https://jsonplaceholder.typicode.com/users", 
            "https://jsonplaceholder.typicode.com/comments"
        ]
        
        for endpoint in endpoints:
            driver.get(endpoint)
            time.sleep(1)
            
            # JSON formatında veri olduğunu doğrula (başarılı response)
            page_source = driver.page_source
            assert '"id"' in page_source, f"JSON response bulunamadı: {endpoint}"
            assert '[' in page_source and ']' in page_source, f"JSON array formatı bulunamadı: {endpoint}"
            
    # NEGATİF TEST SENARYOLARI
    def test_nonexistent_post_access_failure(self, driver):
        """Olmayan post erişimi - Negatif senaryo"""
        driver.get("https://jsonplaceholder.typicode.com/posts/99999")
        time.sleep(2)
        
        page_source = driver.page_source
        # Olmayan post için boş obje {} dönmeli
        assert '{}' in page_source, "Olmayan post için boş response bekleniyor"
        
    def test_nonexistent_user_access_failure(self, driver):
        """Olmayan kullanıcı erişimi - Negatif senaryo"""
        driver.get("https://jsonplaceholder.typicode.com/users/99999")
        time.sleep(2)
        
        page_source = driver.page_source
        # Olmayan user için boş obje {} dönmeli
        assert '{}' in page_source, "Olmayan kullanıcı için boş response bekleniyor"
        
    def test_invalid_endpoint_access_failure(self, driver):
        """Geçersiz endpoint erişimi - Negatif senaryo"""
        driver.get("https://jsonplaceholder.typicode.com/invalidendpoint")
        time.sleep(2)
        
        page_source = driver.page_source.lower()
        # 404 hatası veya boş response beklenir
        assert '{}' in page_source or 'not found' in page_source, "Geçersiz endpoint için hata bekleniyor"
        
    def test_malformed_url_access_failure(self, driver):
        """Hatalı URL formatı erişimi - Negatif senaryo"""
        driver.get("https://jsonplaceholder.typicode.com/posts/abc")
        time.sleep(2)
        
        page_source = driver.page_source
        # Geçersiz ID formatı için boş response beklenir
        assert '{}' in page_source, "Hatalı URL formatı için boş response bekleniyor"
        
    def test_empty_response_handling(self, driver):
        """Boş response handling - Negatif senaryo"""
        # Olmayan post ID'ye göre comments
        driver.get("https://jsonplaceholder.typicode.com/comments?postId=99999")
        time.sleep(2)
        
        page_source = driver.page_source
        # Boş array [] dönmeli
        assert '[]' in page_source, "Olmayan post için boş comments array'i bekleniyor" 