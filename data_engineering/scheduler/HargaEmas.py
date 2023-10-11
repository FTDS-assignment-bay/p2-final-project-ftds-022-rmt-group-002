import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from datetime import datetime
import os

def webscrap_hargaemas():
    #Setup untuk menjalankan Chrome Driver
    driver = webdriver.Chrome()
    driver.maximize_window()

    datetimes = []
    hargas = []


    # Masuk ke Link dengan selenium (Extract URL)
    url = "https://www.logammulia.com/id/harga-emas-hari-ini"
    driver.get(url)

    # Membuat fungsi scroll down agar bisa scroll page kebawah 
    def scroll_down():
        # Scroll down dengan fungsi yang sama dengan tombol keyboard PAGE DOWN
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)  # Menambah Delay 1s agar halaman bisa ke load

    # Jumlah berapa kali fungsi scroll dilakukan
    scrolls = 7  # angka untuk menentukan jumlah fungsi scroll
    for _ in range(scrolls):
        scroll_down()

    # Mengambil konten dari HTML dengan driver
    html_content = driver.page_source

    # Menggunakan parsing HTML dengan beautifulsoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Mencari element tag dan class yang relevan untuk di extract
    product_containers = soup.find_all('div', class_='right')
    for product in product_containers:
        datetime = product.find('span', class_='value update') #Mencari product pada tag div dan class prd_link-product-name dan menyimpan pada variable title
        harga = product.find('span', class_='value') #Mencari price pada tag div dan class prd_link-product-price dan menyimpan pada variable price

        #Memanggil fungsi mengambil Text (get_text()) dan menambahkan serta menyimpan pada variable list
        if datetime and harga:
            datetimes.append(datetime.get_text())
            hargas.append(harga.get_text())
        else:
            continue


    # Menutup browser setelah web scraping
    driver.quit()

    # Membuat dataframe dari data yang sudah dikumpulkan
    data = pd.DataFrame({
        'datetime': datetimes,
        'price': hargas,
    })
    data.to_csv('HargaEmas_raw.csv',index=False)

def clean_hargaemas():
    data = pd.read_csv('HargaEmas_raw.csv')
    listhilang = ['Rp','.',',00','\n']
    for substring in listhilang:
        data = data.applymap(lambda x: x.replace(substring, ''))

    date_format = "%d %b %Y %H:%M:%S"
    # Convert the string to a datetime object
    data['datetime'] = pd.to_datetime(data['datetime'], format=date_format)
    data['year'] = data['datetime'].dt.year
    data['month'] = data['datetime'].dt.month
    data['day'] = data['datetime'].dt.day

    # Nama file CSV yang akan diperiksa
    early_file_name = 'HargaEmas_clean_early.csv'
    latest_file_name = 'HargaEmas_clean_latest.csv'

    # Mengecek apakah file CSV sudah ada
    
    if os.path.exists(latest_file_name):
        old_data = pd.read_csv(latest_file_name)
        old_data.to_csv(early_file_name, index=False)
        new_data = pd.read_csv(early_file_name)
        new_data = pd.concat([old_data, data])
        new_data = data.drop_duplicates()
        new_data.to_csv(latest_file_name, index=False)
    else:
        data.to_csv(latest_file_name, index=False)

if __name__ == '__main__':
    webscrap_hargaemas()
    clean_hargaemas()