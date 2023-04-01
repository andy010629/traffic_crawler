import requests 
from bs4 import BeautifulSoup
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

base_url = 'https://trafficsafety.web.nycu.edu.tw'

def get_all_page_url():
    page_url_list = [base_url]
    r = requests.get(base_url,headers=headers,verify=False)
    soup = BeautifulSoup(r.text, 'lxml')
    page_soup = soup.select_one('div.nav-previous')
    while page_soup:
        page_url = page_soup.select_one('a').get('href')
        r = requests.get(page_url,headers=headers,verify=False)
        soup = BeautifulSoup(r.text, 'lxml')
        page_soup = soup.select_one('div.nav-previous')
        page_url_list.append(page_url)
    return page_url_list

def get_all_article_title_url(page_url_list):
    title_url_data = []
    for url in page_url_list:
        r = requests.get(url,headers=headers,verify=False)
        soup = BeautifulSoup(r.text, 'lxml')
        artical_soup = soup.select('article')
        for artical in artical_soup:
            title = artical.select('h2')[0].text
            link = artical.select('a')[0].get('href')
            title_url_data.append({'title':title,'link':link})
    return title_url_data

def get_artical_innerHtml(url):
    r = requests.get(url,headers=headers,verify=False)
    soup = BeautifulSoup(r.text, 'lxml')
    artical_soup = soup.select_one('article')
    artical_innerHtml = artical_soup.select_one('div.entry-content').prettify()
    return artical_innerHtml


if __name__ == '__main__':

    if not os.path.exists('article_data'):
        os.mkdir('article_data')

    page_url_list = get_all_page_url()
    title_url_data = get_all_article_title_url(page_url_list)
    
    for data in title_url_data:
        artical_innerHtml = get_artical_innerHtml(data['link'])
        title = data['title'].replace(" ","_")
        if not os.path.exists(f'article_data/{title}'):
            os.mkdir(f'article_data/{title}')

        with open(f'article_data/{title}/article.html','w') as f:
            f.write(artical_innerHtml)

    