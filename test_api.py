#!/usr/bin/env python
"""
Simple script to test the DVD Rental API endpoints
Run this after the API is up and running
"""

import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:8000/api"
headers = {"Content-Type": "application/json"}


def print_response(response, title="Response"):
    """Helper function to print API responses"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        pprint(response.json())
    except:
        print(response.text)


def test_registration():
    """Test user registration"""
    print("\n🔹 Testing User Registration...")
    url = f"{BASE_URL}/auth/register/"
    data = {
        "username": "testcustomer",
        "email": "customer@example.com",
        "password": "testpass123",
        "password2": "testpass123",
        "first_name": "Test",
        "last_name": "Customer",
        "role": "customer"
    }
    response = requests.post(url, json=data, headers=headers)
    print_response(response, "User Registration")
    return response.status_code == 201


def test_login():
    """Test user login and get token"""
    print("\n🔹 Testing User Login...")
    url = f"{BASE_URL}/auth/login/"
    data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(url, json=data, headers=headers)
    print_response(response, "User Login")
    
    if response.status_code == 200:
        return response.json().get('access')
    return None


def test_films(token):
    """Test films endpoint"""
    print("\n🔹 Testing Films Endpoint...")
    url = f"{BASE_URL}/films/"
    auth_headers = {
        **headers,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=auth_headers)
    print_response(response, "Films List (First Page)")
    return response.status_code == 200


def test_film_search(token):
    """Test film search"""
    print("\n🔹 Testing Film Search...")
    url = f"{BASE_URL}/films/search/?q=love"
    auth_headers = {
        **headers,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=auth_headers)
    print_response(response, "Film Search Results")
    return response.status_code == 200


def test_actors(token):
    """Test actors endpoint"""
    print("\n🔹 Testing Actors Endpoint...")
    url = f"{BASE_URL}/actors/"
    auth_headers = {
        **headers,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=auth_headers)
    print_response(response, "Actors List (First Page)")
    return response.status_code == 200


def test_categories(token):
    """Test categories endpoint"""
    print("\n🔹 Testing Categories Endpoint...")
    url = f"{BASE_URL}/categories/"
    auth_headers = {
        **headers,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=auth_headers)
    print_response(response, "Categories List")
    return response.status_code == 200


def test_current_user(token):
    """Test current user endpoint"""
    print("\n🔹 Testing Current User Endpoint...")
    url = f"{BASE_URL}/users/me/"
    auth_headers = {
        **headers,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=auth_headers)
    print_response(response, "Current User Info")
    return response.status_code == 200


def test_swagger():
    """Test if Swagger UI is accessible"""
    print("\n🔹 Testing Swagger UI...")
    url = "http://localhost:8000/swagger/"
    try:
        response = requests.get(url)
        print(f"Swagger UI Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Swagger UI is accessible at http://localhost:8000/swagger/")
            return True
        return False
    except Exception as e:
        print(f"❌ Error accessing Swagger UI: {e}")
        return False


def main():
    """Main test function"""
    print("="*60)
    print("DVD RENTAL API TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test Swagger
    results.append(("Swagger UI", test_swagger()))
    
    # Test registration (might fail if user already exists)
    test_registration()
    
    # Test login and get token
    token = test_login()
    if not token:
        print("\n❌ Failed to get authentication token. Cannot proceed with authenticated tests.")
        return
    
    print(f"\n✅ Successfully obtained authentication token")
    
    # Run authenticated tests
    results.append(("Films List", test_films(token)))
    results.append(("Film Search", test_film_search(token)))
    results.append(("Actors List", test_actors(token)))
    results.append(("Categories List", test_categories(token)))
    results.append(("Current User", test_current_user(token)))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    print("\n" + "="*60)
    print("For full API documentation, visit:")
    print("  - Swagger UI: http://localhost:8000/swagger/")
    print("  - ReDoc: http://localhost:8000/redoc/")
    print("  - Django Admin: http://localhost:8000/admin/")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to the API server.")
        print("Make sure the Docker containers are running:")
        print("  docker-compose up")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

