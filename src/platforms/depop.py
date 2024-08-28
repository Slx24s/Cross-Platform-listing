import requests
from bs4 import BeautifulSoup
import logging
import time
import random
import os

def login(username, password):
    logging.info(f"Attempting to log in to Depop as {username}")
    login_url = "https://www.depop.com/login/"
    
    session = requests.Session()
    
    # Get the login page to retrieve any necessary cookies or tokens
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the CSRF token (this is an example, actual implementation may vary)
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    # Prepare login data
    login_data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    
    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': login_url
    }
    
    # Attempt to log in
    response = session.post(login_url, data=login_data, headers=headers, allow_redirects=False)
    
    if response.status_code == 302:  # Successful login usually redirects
        logging.info("Successfully logged in to Depop")
        return session
    else:
        logging.error("Failed to log in to Depop")
        return None

def create_listing(config, listing):
    logging.info("Attempting to create Depop listing")
    
    session = login(config['username'], config['password'])
    if not session:
        return "Failed to log in"
    
    create_listing_url = "https://www.depop.com/products/create/"
    
    # Get the create listing page
    response = session.get(create_listing_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the form and extract any necessary tokens
    form = soup.find('form', {'id': 'create-listing-form'})
    if not form:
        logging.error("Could not find the create listing form")
        return "Failed to create listing: form not found"
    
    # Extract form data
    form_data = {
        'title': listing['title'],
        'description': listing['description'],
        'price': str(listing['price']),
        'category': listing['category'],
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
    
    # Upload images
    image_urls = []
    for image_path in listing['images']:
        image_url = upload_image(session, image_path)
        if image_url:
            image_urls.append(image_url)
    
    # Add image URLs to form data
    for i, url in enumerate(image_urls):
        form_data[f'image_{i+1}'] = url
    
    # Add a small delay to mimic human behavior
    time.sleep(random.uniform(1, 3))
    
    # Attempt to create the listing
    response = session.post(create_listing_url, data=form_data, headers=headers)
    
    if "Your item is now live" in response.text:  # This is a placeholder condition
        logging.info("Successfully created Depop listing")
        return "Listing created successfully"
    else:
        logging.error("Failed to create Depop listing")
        return "Failed to create listing"
    
def upload_image(session, image_path):
    logging.info(f"Uploading image: {image_path}")
    
    upload_url = "https://www.depop.com/api/v1/uploads/"  # This URL may need to be adjusted
    
    try:
        with open(image_path, 'rb') as image_file:
            files = {'file': (os.path.basename(image_path), image_file, 'image/jpeg')}
            response = session.post(upload_url, files=files)
            
            if response.status_code == 200:
                image_url = response.json()['url']
                logging.info(f"Successfully uploaded image: {image_url}")
                return image_url
            else:
                logging.error(f"Failed to upload image. Status code: {response.status_code}")
                return None
    except Exception as e:
        logging.error(f"Error uploading image: {str(e)}")
        return None
    


def search_listings(query):
    logging.info(f"Searching Depop for '{query}'")
    
    search_url = f"https://www.depop.com/search/?q={query}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all product cards (this selector may need to be updated)
    listings = soup.find_all('article', class_='styles__ProductCard')
    
    results = []
    for listing in listings:
        title = listing.find('p', class_='styles__ProductCard__Title').text.strip()
        price = listing.find('p', class_='styles__ProductCard__Price').text.strip()
        results.append({'title': title, 'price': price})
    
    return results