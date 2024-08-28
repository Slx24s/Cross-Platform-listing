import logging
import os
from ebaysdk.finding import Connection as Finding
from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

def login(config):
    # eBay uses API keys instead of username/password for authentication
    logging.info("Setting up eBay API connection")
    try:
        finding_api = Finding(appid=config['app_id'], config_file=None)
        trading_api = Trading(appid=config['app_id'], devid=config['dev_id'], 
                              certid=config['cert_id'], token=config['user_token'], 
                              config_file=None)
        return {'finding': finding_api, 'trading': trading_api}
    except Exception as e:
        logging.error(f"Failed to set up eBay API connection: {str(e)}")
        return None

def upload_image(api, image_path):
    logging.info(f"Uploading image: {image_path}")
    
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        
        request = {
            "PictureData": {"Data": image_data},
            "PictureName": os.path.basename(image_path)
        }
        
        response = api['trading'].execute('UploadSiteHostedPictures', request)
        
        if response.reply.Ack == 'Success':
            image_url = response.reply.SiteHostedPictureDetails.FullURL
            logging.info(f"Successfully uploaded image: {image_url}")
            return image_url
        else:
            logging.error(f"Failed to upload image: {response.reply.Errors.LongMessage}")
            return None
    except Exception as e:
        logging.error(f"Error uploading image: {str(e)}")
        return None

def create_listing(config, listing):
    logging.info("Attempting to create eBay listing")
    
    api = login(config)
    if not api:
        return "Failed to set up API connection"
    
    try:
        # Upload images
        picture_urls = []
        for image_path in listing['images']:
            image_url = upload_image(api, image_path)
            if image_url:
                picture_urls.append(image_url)
        
        # Convert our generic listing format to eBay's format
        ebay_item = {
            "Item": {
                "Title": listing['title'],
                "Description": listing['description'],
                "PrimaryCategory": {"CategoryID": listing['category']},
                "StartPrice": listing['price'],
                "Country": "US",
                "Currency": "USD",
                "ListingDuration": "Days_7",
                "PaymentMethods": ["PayPal"],
                "PayPalEmailAddress": config['paypal_email'],
                "ReturnPolicy": {
                    "ReturnsAcceptedOption": "ReturnsAccepted",
                    "RefundOption": "MoneyBack",
                    "ReturnsWithinOption": "Days_30",
                    "ShippingCostPaidByOption": "Buyer"
                },
                "PictureDetails": {
                    "PictureURL": picture_urls
                }
            }
        }
        
        # Add the item
        response = api['trading'].execute('AddItem', ebay_item)
        
        if response.reply.Ack == 'Success':
            logging.info("Successfully created eBay listing")
            return f"Listing created successfully. Item ID: {response.reply.ItemID}"
        else:
            logging.error("Failed to create eBay listing")
            return f"Failed to create listing: {response.reply.Errors.LongMessage}"
    
    except ConnectionError as e:
        logging.error(f"eBay API connection error: {e}")
        return f"eBay API connection error: {str(e)}"
    except Exception as e:
        logging.error(f"Error creating eBay listing: {str(e)}")
        return f"Error creating listing: {str(e)}"

def search_listings(query, config):
    logging.info(f"Searching eBay for '{query}'")
    
    api = login(config)
    if not api:
        return []
    
    try:
        response = api['finding'].execute('findItemsAdvanced', {'keywords': query})
        
        search_result = response.reply.searchResult
        results = []
        for item in search_result.item:
            results.append({
                'title': item.title,
                'price': item.sellingStatus.currentPrice.value
            })
        
        return results
    
    except ConnectionError as e:
        logging.error(f"eBay API connection error: {e}")
        return []
    except Exception as e:
        logging.error(f"Error searching eBay listings: {str(e)}")
        return []