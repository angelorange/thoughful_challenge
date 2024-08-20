# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import requests
# import os
# import re
# import pandas as pd

# class NewsSearch:
#     def __init__(self, base_url, excel_filename):
#         self.base_url = base_url
#         self.excel_filename = excel_filename
#         self.driver = webdriver.Firefox()
#         self.wait = WebDriverWait(self.driver, 20)
#         self.image_folder = 'images'
#         if not os.path.exists(self.image_folder):
#             os.makedirs(self.image_folder)

#     def search_news(self, search_phrase, months):
#         self.search_phrase = search_phrase
#         self.driver.get(self.base_url)

#         print("Waiting for the search button...")
#         search_button = self.wait.until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, '.SearchOverlay-search-button'))
#         )
#         search_button.click()

#         print("Waiting for the search input field...")
#         search_input = self.wait.until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, '.SearchOverlay-search-input'))
#         )
#         search_input.send_keys(search_phrase)

#         print("Waiting for the send button...")
#         search_submit_button = self.wait.until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, '.SearchOverlay-search-submit'))
#         )
#         search_submit_button.click()

#         print("Waiting for the category button...")
#         category_button_xpath = '/html/body/div[3]/bsp-search-results-module/form/div[2]/div/bsp-search-filters/div/aside/div/div[3]/div/bsp-toggler/div'
#         category_button = self.wait.until(
#             EC.element_to_be_clickable((By.XPATH, category_button_xpath))
#         )
#         category_button.click()

#         print("Waiting for the Stories checkbox...")
#         filter_stories_checkbox = self.wait.until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="00000188-f942-d221-a78c-f9570e360000"]'))
#         )
#         if not filter_stories_checkbox.is_selected():
#             filter_stories_checkbox.click()

#         print("Waiting for the search results...")
#         self.wait.until(
#             EC.visibility_of_element_located((By.CLASS_NAME, 'PageList-items'))
#         )
#         time.sleep(5)

#         news_data_list = []
#         article_links = self.get_article_links()

#         for i in range(min(10, len(article_links))):
#             link = article_links[i]
#             print(f"Processing news {i + 1}...")
#             self.driver.get(link)
#             time.sleep(5)
#             news_data = self.extract_article_data()
#             if news_data:
#                 print(f"News {i + 1} successfully extracted:")
#                 print(news_data)
#                 news_data_list.append(news_data)
#             else:
#                 print(f"Error when extracting data from the news {i + 1}")

#             self.driver.back()
#             time.sleep(5)

#             print("Reloading news links...")
#             self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'PageList-items')))
#             article_links = self.get_article_links()

#         if news_data_list:
#             self.save_to_excel(news_data_list)
#         self.driver.quit()

#     def get_article_links(self):
#         links_xpath = '//div[@data-list-loadmore-items]//div[contains(@class, "PageList-items")]//div//a'
#         link_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, links_xpath)))
#         article_links = list(set(element.get_attribute('href') for element in link_elements))
#         print(f"Links found (no duplicates): {article_links}")
#         return article_links

#     def extract_article_data(self):
#         try:
#             title_xpath = '//div[contains(@class, "Page-headline")]//h1 | //h1'
#             title = self.get_element_text(title_xpath)

#             if not title:
#                 title_xpath = '//h1[contains(@class, "Page-headline")]'
#                 title = self.get_element_text(title_xpath)

#             date_xpath = '//span[@data-date]'
#             date = self.get_element_text(date_xpath)

#             description_xpath = '//div[contains(@class, "Page-storyBody") or contains(@class, "RichTextStoryBody") or contains(@class, "RichTextBody")]'
#             description = self.get_element_text(description_xpath)

#             image_xpath = '//img[contains(@class, "Image")]'
#             image_url = self.get_element_attribute(image_xpath, 'src')
#             image_filename = self.download_image(image_url, f"{title[:30].replace(' ', '_')}.jpg")

#             count_search_phrase = (title + description).lower().count(self.search_phrase.lower())
#             contains_money = bool(re.search(r'\$\d+(\.\d+)?|\d+ (dollars|USD)', title + description, re.IGNORECASE))

#             return {
#                 'title': title,
#                 'date': date,
#                 'description': description,
#                 'image_filename': image_filename,
#                 'search_phrase_count': count_search_phrase,
#                 'contains_money': contains_money
#             }
#         except Exception as e:
#             print(f"Error when extracting data from the news: {e}")
#             return None

#     def get_element_text(self, xpath=None):
#         try:
#             if xpath:
#                 element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
#                 return element.text
#             return ''
#         except Exception as e:
#             print(f"Error when extracting text from element: {e}")
#             return ''

#     def get_element_attribute(self, xpath=None, attribute='src'):
#         try:
#             if xpath:
#                 element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
#                 return element.get_attribute(attribute)
#             return ''
#         except Exception as e:
#             print(f"Error extracting attribute from element: {e}")
#             return ''

#     def download_image(self, img_url, filename):
#         if not img_url or not img_url.startswith('http'):
#             print(f"Invalid image URL: {img_url}")
#             return ''
#         try:
#             response = requests.get(img_url, timeout=10)
#             response.raise_for_status()  # Levanta um erro para códigos de status não-200
#             img_path = os.path.join(self.image_folder, filename)
#             with open(img_path, 'wb') as file:
#                 file.write(response.content)
#             return filename
#         except Exception as e:
#             print(f"Error downloading image: {e}")
#             return ''

#     def save_to_excel(self, news_data_list):
#         df = pd.DataFrame(news_data_list)
#         df.to_excel(self.excel_filename, index=False)
#         print(f"Data saved in Excel file: {self.excel_filename}")


import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
import re
import pandas as pd

class NewsSearch:
    def __init__(self, base_url, excel_filename):
        self.base_url = base_url
        self.excel_filename = excel_filename
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 20)
        self.image_folder = 'images'
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

        # Configuração do logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()

    def search_news(self, search_phrase, months):
        self.search_phrase = search_phrase
        self.driver.get(self.base_url)

        self.logger.info("Waiting for the search button...")
        search_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.SearchOverlay-search-button'))
        )
        search_button.click()

        self.logger.info("Waiting for the search input field...")
        search_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.SearchOverlay-search-input'))
        )
        search_input.send_keys(search_phrase)

        self.logger.info("Waiting for the send button...")
        search_submit_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.SearchOverlay-search-submit'))
        )
        search_submit_button.click()

        self.logger.info("Waiting for the category button...")
        category_button_xpath = '/html/body/div[3]/bsp-search-results-module/form/div[2]/div/bsp-search-filters/div/aside/div/div[3]/div/bsp-toggler/div'
        category_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, category_button_xpath))
        )
        category_button.click()

        self.logger.info("Waiting for the Stories checkbox...")
        filter_stories_checkbox = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="00000188-f942-d221-a78c-f9570e360000"]'))
        )
        if not filter_stories_checkbox.is_selected():
            filter_stories_checkbox.click()

        self.logger.info("Waiting for the search results...")
        self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'PageList-items'))
        )
        time.sleep(5)

        news_data_list = []
        article_links = self.get_article_links()

        for i in range(min(10, len(article_links))):
            link = article_links[i]
            self.logger.info(f"Processing news {i + 1}...")
            self.driver.get(link)
            time.sleep(5)
            news_data = self.extract_article_data()
            if news_data:
                self.logger.info(f"News {i + 1} successfully extracted:")
                self.logger.info(news_data)
                news_data_list.append(news_data)
            else:
                self.logger.error(f"Error when extracting data from the news {i + 1}")

            self.driver.back()
            time.sleep(5)

            self.logger.info("Reloading news links...")
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'PageList-items')))
            article_links = self.get_article_links()

        if news_data_list:
            self.save_to_excel(news_data_list)
        self.driver.quit()

    def get_article_links(self):
        links_xpath = '//div[@data-list-loadmore-items]//div[contains(@class, "PageList-items")]//div//a'
        link_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, links_xpath)))
        article_links = list(set(element.get_attribute('href') for element in link_elements))
        self.logger.info(f"Links found (no duplicates): {article_links}")
        return article_links

    def extract_article_data(self):
        try:
            title_xpath = '//div[contains(@class, "Page-headline")]//h1 | //h1'
            title = self.get_element_text(title_xpath)

            if not title:
                title_xpath = '//h1[contains(@class, "Page-headline")]'
                title = self.get_element_text(title_xpath)

            date_xpath = '//span[@data-date]'
            date = self.get_element_text(date_xpath)

            description_xpath = '//div[contains(@class, "Page-storyBody") or contains(@class, "RichTextStoryBody") or contains(@class, "RichTextBody")]'
            description = self.get_element_text(description_xpath)

            image_xpath = '//img[contains(@class, "Image")]'
            image_url = self.get_element_attribute(image_xpath, 'src')
            image_filename = self.download_image(image_url, f"{title[:30].replace(' ', '_')}.jpg")

            count_search_phrase = (title + description).lower().count(self.search_phrase.lower())
            contains_money = bool(re.search(r'\$\d+(\.\d+)?|\d+ (dollars|USD)', title + description, re.IGNORECASE))

            return {
                'title': title,
                'date': date,
                'description': description,
                'image_filename': image_filename,
                'search_phrase_count': count_search_phrase,
                'contains_money': contains_money
            }
        except Exception as e:
            self.logger.error(f"Error when extracting data from the news: {e}")
            return None

    def get_element_text(self, xpath=None):
        try:
            if xpath:
                element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                return element.text
            return ''
        except Exception as e:
            self.logger.error(f"Error when extracting text from element: {e}")
            return ''

    def get_element_attribute(self, xpath=None, attribute='src'):
        try:
            if xpath:
                element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                return element.get_attribute(attribute)
            return ''
        except Exception as e:
            self.logger.error(f"Error extracting attribute from element: {e}")
            return ''

    def download_image(self, img_url, filename):
        if not img_url or not img_url.startswith('http'):
            self.logger.warning(f"Invalid image URL: {img_url}")
            return ''
        try:
            response = requests.get(img_url, timeout=10)
            response.raise_for_status()  # Levanta um erro para códigos de status não-200
            img_path = os.path.join(self.image_folder, filename)
            with open(img_path, 'wb') as file:
                file.write(response.content)
            return filename
        except Exception as e:
            self.logger.error(f"Error downloading image: {e}")
            return ''

    def save_to_excel(self, news_data_list):
        df = pd.DataFrame(news_data_list)
        df.to_excel(self.excel_filename, index=False)
        self.logger.info(f"Data saved in Excel file: {self.excel_filename}")
