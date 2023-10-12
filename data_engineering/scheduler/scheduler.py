import schedule
import time
from selenium import webdriver
from tokopedia import webscrap_tokopedia,clean_tokopedia
from bukalapak import webscrap_bukalapak,clean_bukalapak
from blibli import webscrap_blibli,clean_blibli
from HargaEmas import webscrap_hargaemas,clean_hargaemas

driver = webdriver.Chrome()


def run_web_scraping_tasks():
    webscrap_tokopedia()
    clean_tokopedia()
    webscrap_bukalapak()
    clean_bukalapak()
    webscrap_blibli()
    clean_blibli()
    webscrap_hargaemas()
    clean_hargaemas()

schedule.every().day.at("14:42").do(run_web_scraping_tasks)

while True:
    schedule.run_pending()
    time.sleep(1)