import requests, random, logging, urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
from config import CFG


def get_links(url = CFG.url):
    master_links = []

    page = urllib.request.urlopen(url).read().decode('utf8','ignore') 
    soup = BeautifulSoup(page,"lxml")

    for link in soup.find_all('a',{'class': 'terms-bar__link mntl-text-link'},  href = True):

        master_links.append(link.get('href'))

    print(f"Num URLs:{len(master_links)}")
    return master_links[:CFG.num_links]

if __name__ == "__main__":

    os.makedirs("data", exist_ok = True)

    logging.basicConfig(filename='scraping.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    master_links = get_links(CFG.url)

    with open('URL_INDEX_BY_ALPHA.txt', 'w') as f:
        for item in master_links:
            f.write("%s\n" % item)

    list_alpha = []
    for articleIdx in master_links:
        page = urllib.request.urlopen(articleIdx).read().decode('utf8','ignore') 
        soup = BeautifulSoup(page,"lxml")
        for link in soup.find_all('a',{'class': 'dictionary-top300-list__list mntl-text-link'},  href = True):
                list_alpha.append(link.get('href'))

    with open('FULL_URL_INDEX.txt', 'w') as f:
        for item in list_alpha:
            f.write("%s\n" % item)

    logf = open("scraping_error.log", "w")
    for article in tqdm(list_alpha):
    
        try:
            page = urllib.request.urlopen(article, timeout = 3).read().decode('utf8','ignore')
            soup = BeautifulSoup(page,"lxml")
            myTags = soup.find_all('p', {'class': 'comp mntl-sc-block finance-sc-block-html mntl-sc-block-html'})
            title = soup.find('title').get_text(strip=True).replace(" ", "_") + '.txt'
            post = ''
            for tag in myTags:
                post += str(tag.get_text(strip=True).encode('ascii', errors='replace')).lower() + '\n' 
            f = 'data/' + title.split("/")[-1]    
            w = open(f, 'w')
            w.write(post)
            w.close()
            
        except:
            logf.write("Failed to extract: {0}\n".format(str(article)))
            logging.error("Exception occurred", exc_info=True)
            
        finally:
            pass
