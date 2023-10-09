from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
import pandas as pd

MAIN_LINK  = "https://enzyme.expasy.org/EC/"


def get_all_human(table):
    h_list = []
    td = table.find_all("td")
    for d in td:
        if "HUMAN" in d.text:
            h_list.append(d.text)
    
    h_list = [i.replace("\xa0",'') for i in h_list]
    
    return h_list



def get_entry(x):
    html_link = MAIN_LINK+x
    print(html_link)
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(html_link)
    time.sleep(10)
    html = driver.page_source
    soup = bs(html, "lxml")
    time.sleep(10)

    table = soup.find("table",{"class":"type-1"})
    if table:
        tr = table.find_all("tr")
        for r in tr:
            s_table = r.find("table")
            if s_table:
                all_h = get_all_human(s_table)
                return all_h
    else:
        print("no data found")
        return None


names = {1:"Oxidoreductases",2:"Transferases",3:"Hydrolases",4:"Lyases",5:"Isomerases",6:"Ligases",7:"Translocases"}

for i in range(1,8):

    html_link = f'''https://enzyme.expasy.org/EC/{i}.-.-.-'''

    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(html_link)
    time.sleep(10)

    html = driver.page_source
    soup = bs(html, "lxml")
    time.sleep(10)

    table = soup.find("table",{"class":"type-1"})

    df = pd.read_html(str(table))[0]
    
    df.rename(columns={0:"id",1:"sub-class"}, inplace=True)
    print(df)

    df["uniprot_entry"] = df["id"].apply(get_entry) 
    
    df = df.explode('uniprot_entry')
    df.to_excel(f"output_{names[i]}.xlsx")
    time.sleep(15)