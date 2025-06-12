from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from selenium.webdriver.support.select import Select


class TodoPageHelper:
    """Helper class for TodoMVC page interactions"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Locators
        self.TODO_INPUT = (By.CLASS_NAME, "new-todo")
        self.TODO_LIST = (By.CLASS_NAME, "todo-list")
        self.TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
        self.TOGGLE_ALL = (By.CLASS_NAME, "toggle-all")
        self.CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")
        self.FILTER_ALL = (By.CSS_SELECTOR, "a[href='#/']")
        self.FILTER_ACTIVE = (By.CSS_SELECTOR, "a[href='#/active']")
        self.FILTER_COMPLETED = (By.CSS_SELECTOR, "a[href='#/completed']")
        self.TODO_COUNT = (By.CLASS_NAME, "todo-count")
        
    def load_page(self, url=None):
        """Load the TodoMVC page"""
        if url is None:
            # Use local HTML file
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            local_file = os.path.join(current_dir, "local_todo.html")
            url = f"file://{local_file}"
            
        print(f"Loading page: {url}")
        self.driver.get(url)
        
        # Wait for the page to load and find the input element
        try:
            self.wait.until(EC.presence_of_element_located(self.TODO_INPUT))
            print("✅ TodoMVC page loaded successfully")
        except TimeoutException:
            # Try alternative selectors
            alternative_selectors = [
                (By.CSS_SELECTOR, "input[placeholder*='todo']"),
                (By.CSS_SELECTOR, "input[type='text']"),
                (By.TAG_NAME, "input")
            ]
            
            for selector in alternative_selectors:
                try:
                    self.wait_for_element(selector, timeout=3)
                    self.TODO_INPUT = selector
                    print(f"✅ Found input with alternative selector: {selector}")
                    break
                except:
                    continue
            else:
                raise TimeoutException("Could not find todo input element")
    
    def add_todo(self, text):
        """Add a new todo item"""
        if not text.strip():
            return  # Don't add empty todos
            
        input_element = self.driver.find_element(*self.TODO_INPUT)
        input_element.clear()
        input_element.send_keys(text)
        input_element.send_keys(Keys.RETURN)
        time.sleep(0.5)  # Wait for animation
    
    def get_todo_items(self):
        """Get all todo items"""
        try:
            return self.driver.find_elements(*self.TODO_ITEMS)
        except NoSuchElementException:
            return []
    
    def get_todo_count(self):
        """Get the number of remaining todos"""
        try:
            count_element = self.driver.find_element(*self.TODO_COUNT)
            text = count_element.text
            # Extract number from text like "1 item left" or "2 items left"
            if "item" in text:
                return int(text.split()[0]) if text.split()[0].isdigit() else 0
            return 0
        except (NoSuchElementException, ValueError, IndexError):
            return 0
    
    def toggle_todo(self, index):
        """Toggle todo item at given index"""
        todos = self.get_todo_items()
        if index < len(todos):
            toggle = todos[index].find_element(By.CLASS_NAME, "toggle")
            toggle.click()
            time.sleep(0.3)
    
    def delete_todo(self, index):
        """Delete todo item at given index"""
        todos = self.get_todo_items()
        if index < len(todos):
            # Hover over the item to show delete button
            self.driver.execute_script("arguments[0].scrollIntoView();", todos[index])
            
            # Try to find and click destroy button
            try:
                destroy_btn = todos[index].find_element(By.CLASS_NAME, "destroy")
                self.driver.execute_script("arguments[0].style.display = 'block';", destroy_btn)
                destroy_btn.click()
                time.sleep(0.3)
            except NoSuchElementException:
                print(f"Warning: Could not find destroy button for todo {index}")
    
    def edit_todo(self, index, new_text):
        """Edit todo item at given index"""
        todos = self.get_todo_items()
        if index < len(todos):
            # Double click to edit
            label = todos[index].find_element(By.TAG_NAME, "label")
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('dblclick', {bubbles: true}));", label)
            time.sleep(0.5)
            
            # Find edit input and change text
            try:
                edit_input = todos[index].find_element(By.CLASS_NAME, "edit")
                edit_input.clear()
                edit_input.send_keys(new_text)
                edit_input.send_keys(Keys.RETURN)
                time.sleep(0.5)
            except NoSuchElementException:
                print(f"Warning: Could not find edit input for todo {index}")
    
    def filter_todos(self, filter_type):
        """Filter todos by type: 'all', 'active', or 'completed'"""
        try:
            if filter_type == 'all':
                self.driver.find_element(*self.FILTER_ALL).click()
            elif filter_type == 'active':
                self.driver.find_element(*self.FILTER_ACTIVE).click()
            elif filter_type == 'completed':
                self.driver.find_element(*self.FILTER_COMPLETED).click()
            time.sleep(0.5)
        except NoSuchElementException:
            print(f"Warning: Could not find filter button for {filter_type}")
    
    def toggle_all_todos(self):
        """Toggle all todos at once"""
        try:
            toggle_all = self.driver.find_element(*self.TOGGLE_ALL)
            toggle_all.click()
            time.sleep(0.5)
        except NoSuchElementException:
            print("Warning: Toggle all button not found")
    
    def clear_completed(self):
        """Clear all completed todos"""
        try:
            clear_btn = self.driver.find_element(*self.CLEAR_COMPLETED)
            if clear_btn.is_displayed():
                clear_btn.click()
                time.sleep(0.5)
        except NoSuchElementException:
            print("Warning: Clear completed button not found or not visible")
    
    def is_todo_completed(self, index):
        """Check if todo at index is completed"""
        todos = self.get_todo_items()
        if index < len(todos):
            classes = todos[index].get_attribute("class")
            return "completed" in classes
        return False
    
    def get_todo_text(self, index):
        """Get text of todo at index"""
        todos = self.get_todo_items()
        if index < len(todos):
            try:
                label = todos[index].find_element(By.TAG_NAME, "label")
                return label.text
            except NoSuchElementException:
                return ""
        return ""
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be present"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            return None
    
    def wait_for_elements(self, locator, timeout=10):
        """Wait for elements to be present"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            return [] 

# JSONPlaceholder API ile entegre Full Stack Test URL'si 
FULLSTACK_APP_URL = f"file://{os.path.abspath('full_stack_app.html')}"

def navigate_to_fullstack_app(driver):
    """JSONPlaceholder Full Stack uygulamasına git"""
    try:
        driver.get(FULLSTACK_APP_URL)
        # Sayfa yüklenene kadar bekle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "header"))
        )
        return True
    except Exception as e:
        print(f"Full Stack uygulaması yüklenemedi: {e}")
        return False

def wait_for_api_data(driver, timeout=10):
    """API verilerinin yüklenmesini bekle"""
    try:
        # Posts verilerinin yüklenmesini bekle
        WebDriverWait(driver, timeout).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "#posts-list .item")) > 0
        )
        return True
    except:
        return False

def switch_tab(driver, tab_name):
    """Tab değiştir (posts, users, create)"""
    try:
        tab_button = driver.find_element(By.CSS_SELECTOR, f'[data-tab="{tab_name}"]')
        tab_button.click()
        
        # Tab içeriğinin görünür olmasını bekle
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, f"{tab_name}-tab"))
        )
        return True
    except:
        return False

def create_new_post(driver, title, content, user_id=1):
    """Yeni post oluştur"""
    try:
        # Create tab'ına geç
        if not switch_tab(driver, "create"):
            return False
        
        # Form alanlarını doldur
        title_input = driver.find_element(By.ID, "postTitle")
        body_input = driver.find_element(By.ID, "postBody")
        user_select = driver.find_element(By.ID, "postUserId")
        
        title_input.clear()
        title_input.send_keys(title)
        
        body_input.clear()
        body_input.send_keys(content)
        
        # User seç
        Select(user_select).select_by_value(str(user_id))
        
        # Formu gönder
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        # Success mesajını bekle
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success"))
        )
        
        return True
    except Exception as e:
        print(f"Post oluşturma hatası: {e}")
        return False

def filter_posts_by_user(driver, user_name=None):
    """Postları kullanıcıya göre filtrele"""
    try:
        # Posts tab'ına geç
        if not switch_tab(driver, "posts"):
            return False
        
        user_filter = driver.find_element(By.ID, "userFilter")
        
        if user_name:
            Select(user_filter).select_by_visible_text(user_name)
        else:
            Select(user_filter).select_by_value("")  # Tümü
            
        # Filtreleme sonuçlarının yüklenmesini bekle
        time.sleep(1)
        return True
    except:
        return False

def get_posts_count(driver):
    """Görünen post sayısını al"""
    try:
        posts = driver.find_elements(By.CSS_SELECTOR, "#posts-list .item")
        return len(posts)
    except:
        return 0

def get_users_count(driver):
    """Görünen kullanıcı sayısını al"""
    try:
        if not switch_tab(driver, "users"):
            return 0
        users = driver.find_elements(By.CSS_SELECTOR, "#users-list .item")
        return len(users)
    except:
        return 0

def delete_first_post(driver):
    """İlk postu sil"""
    try:
        if not switch_tab(driver, "posts"):
            return False
        
        # İlk delete butonunu bul ve tıkla
        delete_button = driver.find_element(By.CSS_SELECTOR, "#posts-list .item:first-child .btn.danger")
        delete_button.click()
        
        # Confirmation dialog'u kabul et
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert.accept()
        
        # Success mesajını bekle
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success"))
        )
        
        return True
    except:
        return False

def verify_post_exists(driver, title):
    """Belirli başlıklı postun var olduğunu kontrol et"""
    try:
        if not switch_tab(driver, "posts"):
            return False
        posts = driver.find_elements(By.CSS_SELECTOR, "#posts-list .item h3")
        for post in posts:
            if title.lower() in post.text.lower():
                return True
        return False
    except:
        return False

def verify_user_data(driver, user_name):
    """Kullanıcı verisinin doğru yüklendiğini kontrol et"""
    try:
        if not switch_tab(driver, "users"):
            return False
        users = driver.find_elements(By.CSS_SELECTOR, "#users-list .item h3")
        for user in users:
            if user_name.lower() in user.text.lower():
                return True
        return False
    except:
        return False

# JSONPlaceholder'ın kendi web sitesi
JSONPLACEHOLDER_WEBSITE = "https://jsonplaceholder.typicode.com/"

def navigate_to_jsonplaceholder_site(driver):
    """JSONPlaceholder web sitesine git"""
    try:
        driver.get(JSONPLACEHOLDER_WEBSITE)
        # Sayfa yüklenene kadar bekle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        return True
    except Exception as e:
        print(f"JSONPlaceholder sitesi yüklenemedi: {e}")
        return False

def test_api_documentation_links(driver):
    """API dokümantasyon linklerini test et"""
    try:
        # API endpoint linklerini bul
        api_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/posts'], a[href*='/users'], a[href*='/comments']")
        return len(api_links) > 0
    except:
        return False

def test_interactive_examples(driver):
    """Interaktif örnekleri test et"""
    try:
        # Code örneklerini bul
        code_blocks = driver.find_elements(By.TAG_NAME, "code")
        return len(code_blocks) > 0
    except:
        return False

def test_navigation_menu(driver):
    """Site navigasyonunu test et"""
    try:
        # Navigation elementlerini bul
        nav_elements = driver.find_elements(By.CSS_SELECTOR, "nav, .nav, .menu")
        return len(nav_elements) > 0
    except:
        return False

def test_api_response_display(driver):
    """API response görüntülenmesini test et"""
    try:
        # JSON response alanlarını bul
        json_elements = driver.find_elements(By.CSS_SELECTOR, "pre, .json, .response")
        return len(json_elements) > 0
    except:
        return False

def click_api_endpoint_link(driver, endpoint):
    """API endpoint linkine tıkla"""
    try:
        link = driver.find_element(By.CSS_SELECTOR, f"a[href*='/{endpoint}']")
        link.click()
        time.sleep(2)
        return True
    except:
        return False

def verify_page_title(driver, expected_title_part):
    """Sayfa başlığını doğrula"""
    try:
        title = driver.title
        return expected_title_part.lower() in title.lower()
    except:
        return False

def verify_api_url_in_browser(driver, endpoint):
    """Browser'da API URL'inin görüntülendiğini doğrula"""
    try:
        current_url = driver.current_url
        return endpoint in current_url
    except:
        return False 