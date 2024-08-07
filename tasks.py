import yaml
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import requests
from io import BytesIO
from PIL import Image

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewsScraper:
    def __init__(self, search_phrase, news_category, months):
        self.search_phrase = search_phrase
        self.news_category = news_category
        self.months = months
        self.driver = None
    
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    def load_parameters_from_file(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_file = os.path.join(script_dir, 'parameters.yaml')
        
        if not os.path.isfile(yaml_file):
            raise FileNotFoundError(f"Arquivo {yaml_file} não encontrado.")
        
        with open(yaml_file, 'r') as file:
            return yaml.safe_load(file)

    def scrape_news(self):
        try:
            self.setup_driver()
            url = "https://news.yahoo.com/"
            self.driver.get(url)
            
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'p'))
            )
            search_box.send_keys(self.search_phrase)
            search_box.submit()

            if self.news_category:
                category_filter = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//a[text()='{self.news_category}']"))
                )
                category_filter.click()
            
            articles = self.driver.find_elements(By.CSS_SELECTOR, 'article')
            news_data = []
            
            for article in articles:
                try:
                    title = article.find_element(By.CSS_SELECTOR, 'h3').text
                    date = article.find_element(By.CSS_SELECTOR, 'time').get_attribute('datetime')
                    description = article.find_element(By.CSS_SELECTOR, 'p').text

                    money_pattern = re.compile(r'\$\d+(?:\.\d+)?|\d+ dollars|\d+ USD', re.IGNORECASE)
                    contains_money = bool(money_pattern.search(title)) or bool(money_pattern.search(description))
                    
                    search_phrase_count = title.lower().count(self.search_phrase.lower()) + description.lower().count(self.search_phrase.lower())
                    
                    img_elem = article.find_element(By.CSS_SELECTOR, 'img')
                    img_url = img_elem.get_attribute('src')
                    img_filename = os.path.basename(img_url)
                    img_data = requests.get(img_url).content
                    img = Image.open(BytesIO(img_data))
                    img.save(f'output/{img_filename}')

                    news_data.append({
                        'title': title,
                        'date': date,
                        'description': description,
                        'picture_filename': img_filename,
                        'search_phrase_count': search_phrase_count,
                        'contains_money': contains_money
                    })
                except Exception as e:
                    logging.error(f"Erro ao processar o artigo: {e}")

            df = pd.DataFrame(news_data)
            output_file = 'output/news_data.xlsx'
            df.to_excel(output_file, index=False)
            logging.info(f"Dados salvos em {output_file}")

        except Exception as e:
            logging.error(f"Erro durante a coleta de notícias: {e}")
        finally:
            if self.driver:
                self.driver.quit()

def main():
    try:
        scraper = NewsScraper(search_phrase='', news_category='', months=1)
        params = scraper.load_parameters_from_file()
        scraper.search_phrase = params.get('search_phrase', '')
        scraper.news_category = params.get('news_category', '')
        scraper.months = int(params.get('months', 1))
        
        logging.info(f"Search Phrase: {scraper.search_phrase}")
        logging.info(f"News Category: {scraper.news_category}")
        logging.info(f"Months: {scraper.months}")
        
        scraper.scrape_news()
        
    except Exception as e:
        logging.error(f"Erro: {e}")

if __name__ == "__main__":
    main()
