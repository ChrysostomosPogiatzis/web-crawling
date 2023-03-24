from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
from bs4 import BeautifulSoup
import time
# Here Chrome  will be used
driver = webdriver.Chrome(options=chrome_options)

q='Kuwait BarberShops'
base_url='https://www.google.com'
# URL of website
url = "https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&sxsrf=AJOqlzUqONezq_TJsPH_0zT0I1C0zmut6Q:1679647149052&q="+q

# Getting current URL source code
get_title = driver.title


def maps(url):
    # Opening the website
    driver.get(url)
    delay = 6 # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'appbar')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")


    l =driver.find_element(By.XPATH, '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe"]')
#perform click
    l.click()

    wallet_providers = driver.find_elements(By.XPATH, '//div[@id="search"]//a[@class="vwVdIc wzN8Ac rllt__link a-no-hover-decoration"]')

    print("Businesses in page ",len(wallet_providers))

    for i in range(len(wallet_providers)):




        wallet_providers[i].click()

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        get_title = soup.find_all('div', class_='SPZz6b')


        for title in get_title:
            print("Name: ",title.get_text())

        if len(soup.find_all('a', class_='Od1FEc dHS6jb')) >0:
        	get_telephone= soup.find_all('a', class_='Od1FEc dHS6jb')[0]['data-phone-number']
        	print("Telephone: ",get_telephone)
        if len(soup.find_all('a', class_='dHS6jb')) >0:
        	get_website = soup.find_all('a', class_='dHS6jb')[0]['href']
        	print("Website: ",get_website)
        if len(soup.find_all('span', class_='LrzXr')) >0:
        	get_address = soup.find_all('span', class_='LrzXr')[0].get_text()
        	print("Address: ",get_address)

        if len(soup.find_all('g-link', class_='fl w23JUc ap3N9d')) >0:
        	get_socials = soup.find_all('g-link', class_='fl w23JUc ap3N9d')
        	for i in get_socials:

        	       links = i.find('a')['href']
        	       print("Socials: ",links)
        time.sleep(4)

        print('---------'+str(i)+'---------')

    maps(base_url+soup.find_all('a', id='pnnext')[0]['href'])
maps(url)
