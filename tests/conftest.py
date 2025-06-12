import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from utils.api_client import APIClient
import os


@pytest.fixture(scope="session")
def api_client():
    """API test client fixture"""
    return APIClient()


@pytest.fixture(scope="function")
def browser():
    """Chrome browser fixture for UI tests"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-extensions")
    # Headless mode için gerektiğinde uncomment edin:
    # chrome_options.add_argument("--headless")
    
    try:
        # ChromeDriverManager ile driver yolunu al
        driver_dir = ChromeDriverManager().install()
        # Gerçek chromedriver executable'ını bul
        driver_dir = os.path.dirname(driver_dir)
        
        # Mac ARM64 için chromedriver'ı bul
        chromedriver_path = None
        for root, dirs, files in os.walk(driver_dir):
            for file in files:
                if file == 'chromedriver' and os.access(os.path.join(root, file), os.X_OK):
                    chromedriver_path = os.path.join(root, file)
                    break
            if chromedriver_path:
                break
        
        if not chromedriver_path:
            # Fallback: sistem PATH'indeki chromedriver'ı kullan
            chromedriver_path = 'chromedriver'
        
        print(f"Using ChromeDriver: {chromedriver_path}")
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        
        yield driver
        
    except Exception as e:
        print(f"❌ ChromeDriver setup failed: {e}")
        print("🔧 Trying alternative setup...")
        
        # Alternative setup - system chromedriver veya manual path
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.implicitly_wait(10)
            yield driver
        except Exception as e2:
            print(f"❌ Alternative setup also failed: {e2}")
            print("💡 UI tests will be skipped. Please check Chrome installation.")
            pytest.skip("ChromeDriver setup failed")
    
    finally:
        try:
            driver.quit()
        except:
            pass


@pytest.fixture(scope="session")
def test_data():
    """Test data fixture"""
    return {
        "valid_post": {
            "title": "Test Post Title",
            "body": "Test post body content",
            "userId": 1
        },
        "invalid_post": {
            "title": "",
            "body": "",
            "userId": "invalid"
        },
        "valid_user": {
            "name": "Test User",
            "username": "testuser",
            "email": "test@example.com"
        },
        "todo_items": [
            "Learn Python testing",
            "Write API tests",
            "Create UI tests",
            "Complete project report"
        ]
    }


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test"""
    # Test başlamadan önce yapılacak hazırlıklar
    yield
    # Test bittikten sonra temizlik işlemleri 


@pytest.fixture
def driver(browser):
    """WebDriver fixture - browser fixture'ını kullanır"""
    return browser 