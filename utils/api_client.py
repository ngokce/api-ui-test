import requests
import json
from typing import Dict, Any, Optional
import time


class APIClient:
    """JSONPlaceholder API client for testing"""
    
    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def get_posts(self, post_id: Optional[int] = None) -> requests.Response:
        """Get posts from API"""
        url = f"{self.base_url}/posts"
        if post_id:
            url = f"{url}/{post_id}"
        return self.session.get(url)
    
    def create_post(self, post_data: Dict[str, Any]) -> requests.Response:
        """Create a new post"""
        url = f"{self.base_url}/posts"
        return self.session.post(url, json=post_data)
    
    def update_post(self, post_id: int, post_data: Dict[str, Any]) -> requests.Response:
        """Update an existing post"""
        url = f"{self.base_url}/posts/{post_id}"
        return self.session.put(url, json=post_data)
    
    def patch_post(self, post_id: int, post_data: Dict[str, Any]) -> requests.Response:
        """Partially update an existing post"""
        url = f"{self.base_url}/posts/{post_id}"
        return self.session.patch(url, json=post_data)
    
    def delete_post(self, post_id: int) -> requests.Response:
        """Delete a post"""
        url = f"{self.base_url}/posts/{post_id}"
        return self.session.delete(url)
    
    def get_users(self, user_id: Optional[int] = None) -> requests.Response:
        """Get users from API"""
        url = f"{self.base_url}/users"
        if user_id:
            url = f"{url}/{user_id}"
        return self.session.get(url)
    
    def get_comments(self, post_id: Optional[int] = None) -> requests.Response:
        """Get comments from API"""
        url = f"{self.base_url}/comments"
        if post_id:
            url = f"{url}?postId={post_id}"
        return self.session.get(url)
    
    def get_albums(self, user_id: Optional[int] = None) -> requests.Response:
        """Get albums from API"""
        url = f"{self.base_url}/albums"
        if user_id:
            url = f"{url}?userId={user_id}"
        return self.session.get(url)
    
    def measure_response_time(self, endpoint: str, method: str = "GET") -> float:
        """Measure API response time"""
        start_time = time.time()
        
        if method.upper() == "GET":
            response = self.session.get(f"{self.base_url}{endpoint}")
        elif method.upper() == "POST":
            response = self.session.post(f"{self.base_url}{endpoint}")
        
        end_time = time.time()
        return end_time - start_time
    
    def validate_json_schema(self, response: requests.Response, expected_fields: list) -> bool:
        """Validate JSON response has expected fields"""
        try:
            json_data = response.json()
            if isinstance(json_data, list):
                # List response - check first item
                if json_data and isinstance(json_data[0], dict):
                    return all(field in json_data[0] for field in expected_fields)
            elif isinstance(json_data, dict):
                # Single object response
                return all(field in json_data for field in expected_fields)
            return False
        except (json.JSONDecodeError, KeyError, IndexError):
            return False 