#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from selenium import webdriver
import time
import regex as re
from tqdm import tqdm
from datetime import date
import lxml
import pickle

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



def scrape():

    brand = []
    item = []
    og_price = []
    final_price = []
    sale = []
    store_id = []
    item_num = []

    # Load the web page
    search_word = input("Type URL") 
    driver = webdriver.Chrome(executable_path=r'C:\Users\h00ns\Web Scraping\chromedriver') #access chromedriver
    driver.get(search_word) #open chrome window with url
    driver.maximize_window()

    # Wait for the page to fully load
    driver.implicitly_wait(5)

    #Move to American Website
    wait = WebDriverWait(driver, 5)

    nation_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/header/div[2]/div/div[1]/div[2]/div/button")))
    nation_button.click()

    US_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/header/div[2]/div/div[1]/div[3]/div/div[3]/ul/li[218]/a")))
    US_button.click()

    driver.maximize_window()

    driver.execute_script("window.scrollTo(0, 15000)") 

    page_number = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/section[1]/div[1]/div[3]/div[2]/div[2]/div/div[2]/div/div[2]")))
    total_pages = int(page_number.text.split(" ")[2].replace(",", ""))

    time.sleep(5)


    for xxxx in tqdm(range(800, total_pages)):

        #print(len(product_count))
        #item_count = 90

        if (xxxx+1)%100 == 0:
            #driver.quit()
            #driver.close()
            #time.sleep(5)
            
            pickle.dump(dic, open( "Farfetch_Mens_clothing_"+str(xxxx+1), "wb" ))
            print(str(xxxx+1),  "pages saved" )
            
            search_word = "https://www.farfetch.com/shopping/men/clothing-2/items.aspx?page="+str(xxxx+1)+"&view=90"
            driver = webdriver.Chrome(executable_path=r'C:\Users\h00ns\Web Scraping\chromedriver') #access chromedriver
            driver.get(search_word) #open chrome window with url

            wait = WebDriverWait(driver, 5)    

            driver.maximize_window()
            
            nation_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/header/div[2]/div/div[1]/div[2]/div/button")))
            nation_button.click()

            US_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/header/div[2]/div/div[1]/div[3]/div/div[3]/ul/li[218]/a")))
            US_button.click()
     

            driver.execute_script("window.scrollTo(0, 15000)")  

            time.sleep(5)

        product_count = driver.find_elements_by_xpath("/html/body/div[2]/main/section[1]/div[1]/div[3]/div[2]/div[2]/div/div[1]/ul/li")

        try:
            for i in (range(len(product_count))):
                product_card = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/section[1]/div[1]/div[3]/div[2]/div[2]/div/div[1]/ul/li["+str(i+1)+"]")))
                text_li = product_card.text.replace(",", "").split("\n")

                if len(product_card.text) > 0 :

                    href_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/section[1]/div[1]/div[3]/div[2]/div[2]/div/div[1]/ul/li["+str(i+1)+"]/a")))
                    href_link = href_element.get_attribute('href')

                    num = re.findall("\d+.aspx", href_link)[0].split(".")[0]

                    if len(re.findall("storeid=\d+", href_link)) == 0:
                        id_ = re.findall("storeid%3d\d+", href_link)[0].split('3d')[-1]

                    else:
                        id_ = re.findall("storeid=\d+", href_link)[0].split("=")[-1]


                    item_num.append(num)
                    store_id.append(id_)

                    if len(text_li) == 4:
                        price_info = text_li[3]
                        find = re.findall("\$\d{2,}", price_info)


                        if len(find) > 1:

                            brand.append(text_li[1])
                            item.append(text_li[2])
                            og_price.append(find[0][:len(find[0])-2])
                            sale.append(find[0][len(find[0])-2:len(find[0])])
                            final_price.append(find[1])
                            #print(find[0][len(find[0])-2:len(find[0])])

                        else:
                            brand.append(text_li[1])
                            item.append(text_li[2])
                            og_price.append(find[0])
                            sale.append(0)
                            final_price.append(find[0])


                    else:
                        price_info = text_li[2]
                        find = re.findall("\$\d{2,}", price_info)

                        if len(find) > 1:

                            brand.append(text_li[0])
                            item.append(text_li[1])
                            og_price.append(find[0][:len(find[0])-2])
                            sale.append(find[0][len(find[0])-2:len(find[0])])
                            final_price.append(find[1])

                        else:
                            brand.append(text_li[0])
                            item.append(text_li[1])
                            og_price.append(find[0])
                            sale.append(0)
                            final_price.append(find[0])

                else:
                    pass

        except:

            for i in (range(len(product_count))):
                product_card = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/section[1]/div[1]/div[3]/div[2]/div[2]/div/div[1]/ul/li["+str(i+1)+"]")))
                text_li = product_card.text.replace(",", "").split("\n")

                if len(product_card.text) > 0 :

                    href_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/section[1]/div[1]/div[3]/div[2]/div[2]/div/div[1]/ul/li["+str(i+1)+"]/a")))
                    href_link = href_element.get_attribute('href')

                    num = re.findall("\d+.aspx", href_link)[0].split(".")[0]
                    id_ = re.findall("storeid=\d+", href_link)[0].split("=")[-1]

                    item_num.append(num)
                    store_id.append(id_)

                    if len(text_li) == 4:
                        price_info = text_li[3]
                        find = re.findall("\$\d{2,}", price_info)


                        if len(find) > 1:

                            brand.append(text_li[1])
                            item.append(text_li[2])
                            og_price.append(find[0][:len(find[0])-2])
                            sale.append(find[0][len(find[0])-2:len(find[0])])
                            final_price.append(find[1])
                            #print(find[0][len(find[0])-2:len(find[0])])

                        else:
                            brand.append(text_li[1])
                            item.append(text_li[2])
                            og_price.append(find[0])
                            sale.append(0)
                            final_price.append(find[0])


                    else:
                        price_info = text_li[2]
                        find = re.findall("\$\d{2,}", price_info)

                        if len(find) > 1:

                            brand.append(text_li[0])
                            item.append(text_li[1])
                            og_price.append(find[0][:len(find[0])-2])
                            sale.append(find[0][len(find[0])-2:len(find[0])])
                            final_price.append(find[1])

                        else:
                            brand.append(text_li[0])
                            item.append(text_li[1])
                            og_price.append(find[0])
                            sale.append(0)
                            final_price.append(find[0])

                else:
                    pass


        next_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='slice-container']/div[3]/div[2]/div[2]/div/div[2]/div/div[3]/a")))
        next_btn.click()

        print(len(brand), len(item_num))
        
        dic = {'brand': brand, 
            'item_name': item, 
            'original_price': og_price, 
            "discounted_price": final_price, 
            "discount":sale, 
            "store_id": store_id, 
            "item_number": item_num}
        
        time.sleep(5)
        

    return dic

