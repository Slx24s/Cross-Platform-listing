import requests
from bs4 import BeautifulSoup
import logging
import time
import random

def login(username, password):
    logging.info(f"Attempting to log in to Vinted as {username}")
    login_url = "https://www.vinted.co.uk/auth/login"
    
    session = requests.Session()
    
    # Get the login page to retrieve any necessary cookies or tokens
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the CSRF token (this is an example, actual implementation may vary)
    csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']
    
    # Prepare login data
    login_data = {
        'user[login]': username,
        'user[password]': password,
        'authenticity_token': csrf_token
    }
    
    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': login_url
    }
    
    # Attempt to log in
    response = session.post(login_url, data=login_data, headers=headers, allow_redirects=False)
    
    if response.status_code == 302:  # Successful login usually redirects
        logging.info("Successfully logged in to Vinted")
        return session
    else:
        logging.error("Failed to log in to Vinted")
        return None

def create_listing(config, listing):
    logging.info("Attempting to create Vinted listing")
    
    session = login(config['username'], config['password'])
    if not session:
        return "Failed to log in"
    
    create_listing_url = "https://www.vinted.co.uk/items/new"
    
    # Get the create listing page
    response = session.get(create_listing_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the form and extract any necessary tokens
    form = soup.find('form', {'id': 'new_item'})
    if not form:
        logging.error("Could not find the create listing form")
        return "Failed to create listing: form not found"
    
    # Extract form data (this is an example, actual implementation may vary)
    form_data = {
        'item[title]': listing['title'],
        'item[description]': listing['description'],
        'item[price]': str(listing['price']),
        'item[category_id]': listing['category'],
        # Add any other necessary fields here
    }
    
    # Find and add any hidden inputs
    for hidden_input in form.find_all('input', type='hidden'):
        form_data[hidden_input['name']] = hidden_input['value']
    
    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': create_listing_url
    }
    
    # Add a small delay to mimic human behavior
    time.sleep(random.uniform(1, 3))
    
    # Attempt to create the listing
    response = session.post(create_listing_url, data=form_data, headers=headers)
    
    if "Your item has been listed" in response.text:  # This is a placeholder condition
        logging.info("Successfully created Vinted listing")
        return "Listing created successfully"
    else:
        logging.error("Failed to create Vinted listing")
        return "Failed to create listing"

def search_listings(query):
    logging.info(f"Searching Vinted for '{query}'")
    
    search_url = f"https://www.vinted.co.uk/catalog?search_text={query}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all product cards (this selector may need to be updated)
    listings = soup.find_all('div', class_='feed-grid__item')
    
    results = []
    for listing in listings:
        title = listing.find('h3', class_='Text_text__QBn4- Text_subtitle__Z1OVT').text.strip()
        price = listing.find('span', class_='Text_text__QBn4- Text_subtitle__Z1OVT').text.strip()
        results.append({'title': title, 'price': price})
    
    return results