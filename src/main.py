import json
import logging
import re
import os
from platforms import depop, vinted, ebay

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Validate config structure
        required_keys = ['depop', 'vinted', 'ebay']
        for key in required_keys:
            if key not in config:
                logging.error(f"Missing '{key}' in config file.")
                return None
        
        return config
    except FileNotFoundError:
        logging.error("Config file not found. Please create a config.json file.")
        return None
    except json.JSONDecodeError:
        logging.error("Invalid JSON in config file. Please check the format.")
        return None

def validate_input(prompt, validator, error_message):
    while True:
        user_input = input(prompt)
        if validator(user_input):
            return user_input
        print(error_message)

def get_listing_details():
    logging.info("Getting listing details from user.")
    
    title = validate_input("Title: ", 
                           lambda x: len(x.strip()) > 0, 
                           "Title cannot be empty.")
    
    description = validate_input("Description: ", 
                                 lambda x: len(x.strip()) > 0, 
                                 "Description cannot be empty.")
    
    price = validate_input("Price: ", 
                           lambda x: re.match(r'^\d+(\.\d{1,2})?$', x) and float(x) > 0, 
                           "Please enter a valid positive number for the price.")
    
    category = validate_input("Category: ", 
                              lambda x: len(x.strip()) > 0, 
                              "Category cannot be empty.")
    

    images = []
    while True:
        image_path = input("Enter image path (or press enter to finish): ")
        if not image_path:
            break
        if os.path.exists(image_path):
            images.append(image_path)
        else:
            print("Image file not found. Please enter a valid path.")

    return {
        'title': title,
        'description': description,
        'price': float(price),
        'category': category,
        'images': images
    }


def create_listing(platform, config, listing):
    try:
        if platform == 'depop':
            return depop.create_listing(config['depop'], listing)
        elif platform == 'vinted':
            return vinted.create_listing(config['vinted'], listing)
        elif platform == 'ebay':
            return ebay.create_listing(config['ebay'], listing)
        else:
            raise ValueError(f"Unknown platform: {platform}")
    except Exception as e:
        logging.error(f"Error creating listing on {platform}: {str(e)}")
        return f"Failed to create listing on {platform}: {str(e)}"

def main():
    config = load_config()
    if not config:
        return

    while True:
        print("\n1. Create new listing on Depop")
        print("2. Create new listing on Vinted")
        print("3. Create new listing on eBay")
        print("4. Exit")
        
        choice = validate_input("Choose an option: ", 
                                lambda x: x in ['1', '2', '3', '4'], 
                                "Please enter a valid option (1-4).")

        if choice in ['1', '2', '3']:
            listing = get_listing_details()
            platform = {'1': 'depop', '2': 'vinted', '3': 'ebay'}[choice]
            result = create_listing(platform, config, listing)
            print(result)
        elif choice == '4':
            logging.info("Exiting application.")
            break

if __name__ == "__main__":
    main()