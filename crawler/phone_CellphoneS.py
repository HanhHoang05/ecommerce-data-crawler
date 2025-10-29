import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import random
import logging
from webdriver_manager.chrome import ChromeDriverManager


driver = None

try: 
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


    driver.get('https://cellphones.com.vn/mobile.html')
    sleep(100)


    #-----------------Trang chủ tất cả sản phẩm------------
    items = driver.find_elements(By.CSS_SELECTOR, '.product-info')
    data = []
    links = []

    for item in items:
        try:
            link_div = item.find_element(By.TAG_NAME, 'a')
            link = link_div.get_attribute('href')
            links.append(link)
            name = item.find_element(By.CLASS_NAME, 'product__name').text
            price = item.find_element(By.CLASS_NAME, 'product__price--show').text
                
            # discount_percent
            try:
                discount_percent = item.find_element(By.CLASS_NAME, 'product__price--percent').text
            except NoSuchElementException:
                discount_percent = 'NaN'

            data.append([link, name, price, discount_percent])

        except Exception as e:
            print(f'Error processing item: {e}')
            continue

    df_products = pd.DataFrame(data, columns=['Link', 'Name', 'Discounted_Price', 'Discount_Percent'])

    print(f'Total {len(links)} items')
    print("Bắt đầu chuyển sang từng trang sản phẩm chi tiết...")


    #----------------------Chi tiet tung san pham -----------------
    all_details = []

    for i, link in enumerate(links):
        try:
            driver.get(link)
            sleep(random.randint(2, 4))

            product_details = {
                'Link': link, 
                'Brand': 'NaN', 
                'Rating': 'NaN',
                'SoldQuantity': 'NaN',
                'RAM': 'NaN',
                'ROM': 'NaN',
                'Battery': 'NaN',
                'BackCamera': 'NaN',
                'FrontCamera': 'NaN',
                'GPU': 'NaN',
                'ChargingPort': 'NaN',
                'Resolution': 'NaN',
                'ScreenSize': 'NaN',
                'WarrantyDuration': 'NaN',
                'NumberOfReview': 'NaN',
                'Description': 'NaN'
            }
        
            # Rating / Number of reviews
            try:
                rating = driver.find_element(By.CSS_SELECTOR, 'div.boxReview-score p.title').text.strip()
                product_details['Rating'] = rating

                number_of_review = driver.find_element(By.CSS_SELECTOR, 'p.boxReview-score__count').text.strip()
                product_details['NumberOfReview'] = number_of_review
            except NoSuchElementException:
                product_details['Rating'] = 'NaN'
                product_details['NumberOfReview'] = 'NaN'

            # Brand 
            try: 
                breadcrumb_items = driver.find_elements(By.CSS_SELECTOR, 'a.button__breadcrumb-item')
                if len(breadcrumb_items) > 1:  
                    brand = breadcrumb_items[1].text.strip() 
                    product_details['Brand'] = brand
            except (NoSuchElementException, IndexError):
                product_details['Brand'] = 'NaN'

            # Description
            try:
                description_div = driver.find_element(By.CLASS_NAME, 'ksp-content')
                descriptions = description_div.find_elements(By.TAG_NAME, 'li')
                description = '\n'.join(sentence.text for sentence in descriptions)
                    
                product_details['Description'] = description
            except NoSuchElementException:
                pass

            #Warranty
            try:
                warranty_div = driver.find_element(By.CLASS_NAME, 'item-warranty-info')
                warranty = warranty_div.find_element(By.CLASS_NAME, 'description').text
                    
                product_details['WarrantyDuration'] = warranty
            except NoSuchElementException:
                pass


            # Technical Specifications
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.technical-content'))
                )
                spec_items = driver.find_elements(By.CSS_SELECTOR, 'ul.technical-content > li')
                
                if spec_items:
                    for item in spec_items:
                        try:
                            label = item.find_element(By.TAG_NAME, 'p').text
                            value = item.find_element(By.TAG_NAME, 'div').text

                            print(f'{label} : {value}')  #  In ra check cho dễ nhìn

                            if 'Dung lượng RAM' in label:
                                    product_details['RAM'] = value
                            elif 'Bộ nhớ trong' in label: #
                                product_details['ROM'] = value
                            elif 'Camera sau' in label:
                                product_details['BackCamera'] = value
                            elif 'Camera trước' in label:
                                product_details['FrontCamera'] = value
                            elif 'Loại CPU' in label:
                                product_details['GPU'] = value
                            elif 'Pin' in label:
                                product_details['Battery'] = value
                            elif 'Kích thước màn hình' in label:
                                product_details['ScreenSize'] = value
                            elif 'Cổng sạc' in label:
                                product_details['ChargingPort'] = value
                            elif 'Độ phân giải màn hình' in label:
                                product_details['Resolution'] = value
                        except:
                            continue
                else:
                    logger.warning("No technical specifications found")
                    
            except Exception as e:
                logger.error(f"Couldn't find specification items: {e}")

            all_details.append(product_details)

        except Exception as e:
            logger.error(f'Error processing product page: {e}')
            continue

    df_specs = pd.DataFrame(all_details)
    df_final = pd.merge(df_products, df_specs, on='Link', how='inner')
        
    df_final.to_csv('data/raw/phone_cellphones.csv', index=False, encoding='utf-8-sig')

    print(f"Data saved! Total products: {len(df_final)}")

except Exception as e:
    print(f"✗ Error: {e}")
    
finally:
    if driver is not None:
        driver.quit()