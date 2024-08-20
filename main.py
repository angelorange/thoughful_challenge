import yaml
from new_search import NewsSearch
import pandas as pd

def load_parameters():
    with open('parameters.yaml', 'r') as file:
        return yaml.safe_load(file)

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Dados salvos no arquivo Excel: {filename}")

def main():
    params = load_parameters()
    search_phrase = params.get('search_phrase')
    months = params.get('months', 0)
    excel_filename = params.get('excel_filename', 'news_data.xlsx')

    scraper = NewsSearch("https://apnews.com", excel_filename)
    scraper.search_news(search_phrase, months)

if __name__ == "__main__":
    main()
