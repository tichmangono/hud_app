# =====================================
# SCRAPE HUD DATA BY CITY, STATE
# =====================================

# Import Libraries
import pandas as pd # library that manipulates data and tables
import numpy as np # allows you to work with numbers in systematic way
from selenium import webdriver # headless web driver mimicking what you do with browser
from selenium.webdriver.common.keys import Keys
from time import sleep # to do time things e.g. wait, sleep
import time
from bs4 import BeautifulSoup as bs
import json
import traceback
import datetime
# AUTO CHROME BINARY
#pip install chromedriver-binary
#import chromedriver_binary  # Adds chromedriver binary to path

# Set up Tkinter and main window
from datetime import timedelta
from tkinter import Tk, messagebox, Entry, Button, Label

def main():
    ############################# FUNCS START #########################################
    def make_url_city_state(city, state):
        city = city.strip().upper().replace(" ", "%20")
        state = state.strip().upper().replace(" ", "%20")
        city_state = city+"%2C%20"+state
        url_a = "https://www.hudhomesusa.org/Membersite/member/property/srp.html?propertySearchParameter=%7B%22brandId%22%3A29%2C%22productIDs%22%3A%5B1%5D%2C%22propertySaleTypes%22%3A%5B%22PreForeclosureNOD%22%2C%22PreForeclosureLisPendens%22%2C%22TaxDeed%22%2C%22TaxLien%22%2C%22RedeemableDeed%22%2C%22TaxTaking%22%5D%2C%22propertyRecordTypes%22%3A%5B%22SingleFamilyHome%22%2C%22TownhouseOrCondo%22%2C%22MultifamilyTwoToFourUnits%22%2C%22MultifamilyFivePlusUnits%22%2C%22Commercial%22%2C%22VacantLand%22%2C%22MobileOrManufacturedHome%22%2C%22Unknown%22%5D%2C%22availPropsOnly%22%3Afalse%2C%22sortBy%22%3A%22quality_score_member%22%2C%22userStatus%22%3A%22member%22%2C%22sortByDesc%22%3Atrue%2C%22recordsCount%22%3A15%2C%22includeSaleTypeCount%22%3Atrue%2C%22propsWithPicturesOnly%22%3Afalse%2C%22validated%22%3Afalse%2C%22qualityScoreColumn%22%3A%22quality_score_9%22%2C%22exclusive%22%3Afalse%2C%22specialFinancing%22%3Afalse%2C%22bargainPrice%22%3Afalse%2C%22fixerUpper%22%3Afalse%2C%22rtoPotential%22%3Afalse%2C%22rtoFinancing%22%3Afalse%2C%22allHotHomes%22%3Afalse%2C%22"
        url_b = f"state%22%3A%22{state}%22%2C%22city%22%3A%22{city}%22%7D&queryText={city_state}#property-value"
        url_c = url_a+ url_b
        print(url_c)
        return url_c

    def do_the_scroll():
        sleep(1)
        print("Try scroll >>",)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-document.body.scrollHeight/98)")
        sleep(3)

    def get_links():
        links = []
        try:
            atags = driver.find_elements_by_class_name("prevent-a-text")
            for a in atags:
                try:
                    links.append(a.get_attribute('href'))
                except:
                    print("no link")
        except Exception as e:
            print("no atags, links con", e, "\n?????\n", traceback.format_exc(), "\n?????\n")

        num_links = len(links)
        print("Links found >> ", num_links)
        return links, num_links

    def get_itm():
        itm = {}

        try:
            addr = driver.find_element_by_class_name("address-heading").text
            address = addr.strip().replace("\n", ", ")
            itm["address"] = address
            print("address >>", address)
        except Exception as e:
            print("no add ", e, "\n?????\n", traceback.format_exc(), "\n?????\n")
        try:
            street = address.split(",")[0].strip()
            itm["street"] = street
        except Exception as e:
            print("no add ", e, "\n?????\n", traceback.format_exc(), "\n?????\n")
        try:
            city = address.split(",")[1].strip()
            itm["city"] = city
        except Exception as e:
            print("no add ", e, "\n?????\n", traceback.format_exc(), "\n?????\n")
        try:
            state = address.split(",")[-1].split()[0].strip()
            itm["state"] = state
        except Exception as e:
            print("no add ", e, "\n?????\n", traceback.format_exc(), "\n?????\n")
        try:
            zipcode = address.split(",")[-1].split()[-1].strip()
            itm["zipcode"] = zipcode
        except Exception as e:
            print("no add ", e, "\n?????\n",traceback.format_exc(), "\n?????\n")
        try:
            meta_detail = driver.find_element_by_class_name("pdp-meta").text
            itm["meta_detail"] = meta_detail
        except Exception as e:
            print("no meta ", e, "\n?????\n",traceback.format_exc(), "\n?????\n")

        try:
            div_det = driver.find_element_by_id("property-details-content")
            details = div_det.text
        except Exception as e:
            print("no div det", e, "\n?????\n", traceback.format_exc(), "\n?????\n")
        try:
            desc = details.split("\n")[-1]
            itm["description"] = desc
        except Exception as e:
            print("no desc det", e, "\n?????\n", traceback.format_exc(), "\n?????\n")

        lis = []
        try:
            lis = div_det.find_elements_by_tag_name("li")
        except Exception as e:
            print("no lis ", e, "\n?????\n", traceback.format_exc(), "\n?????\n")

        li_text_list = []
        for li in lis:
            if li.text != "":
                li_text_list.append(li.text)

        for s in li_text_list:
            try:
                s0 = s.split(":")[0].strip().lower().replace(" ", "_").replace("-", "_")
                s1 = s.split(":")[1].strip()
                itm[s0] = s1
            except Exception as e:
                print("no s ", e, "\n?????\n", traceback.format_exc(), "\n?????\n")

        try:
            div_contact= driver.find_element_by_id("contact-info")
            contact = " - ".join(div_contact.text.split("\n")[1:-1])
            itm["contact"] = contact
        except Exception as e:
            print("no div con", e, "\n?????\n", traceback.format_exc(), "\n?????\n")
        try:
            div_price_info= driver.find_element_by_id("price-info")
            price_info = div_price_info.text
        except Exception as e:
            print("no div pric ", e, "\n?????\n", traceback.format_exc(), "\n?????\n")

        lis_price = []
        try:
            lis_price = div_price_info.find_elements_by_tag_name("li")
        except Exception as e:
            print("no lis_price ", e, "\n?????\n", traceback.format_exc(), "\n?????\n")

        li_text_list_price = []
        for li_price in lis_price:
            if li_price.text != "":
                li_text_list_price.append(li_price.text)

        for s_price in li_text_list_price:
            try:
                s0_price = s_price.split(":")[0].strip().lower().replace(" ", "_").replace("-", "_")
                s1_price = s_price.split(":")[1].strip()
                itm[s0_price] = s1_price
            except Exception as e:
                print("no s_price ", e, "\n?????\n", traceback.format_exc(), "\n?????\n")
        return itm

    ############################# FUNCS END #########################################

    try:
        #chrome_path = "C:\\Program Files\chromedriver"  # PUT YOUR OWN PATH HERE
        chrome_path = "chromedriver"
        #driver = webdriver.Chrome(chrome_path)
        options = webdriver.ChromeOptions()
        #options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        #options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path=chrome_path , options=options)
        url_base = "https://www.hudhomesusa.org/"
        url_x = "https://www.hudhomesusa.org/Membersite/?from=banner"

        usr = "cleo@yowzazz.com"
        pwd = "2023302466"

        url_login = f"{url_base}/Membersite/login.html?username={usr}&password={pwd}"
        # Get the home page
        driver.get(url_login)
        sleep(1)

        #city = input("ENTER CITY e.g. New York (with spaces): =>")#"new york"
        #state = input("ENTER STATE: e.g. NY =>") # "ny"

        city = str(entry1.get())
        state = str(entry2.get())

        url_city_state = make_url_city_state(city, state)
        print("\n$$$$$$$\nSEARCH FOR >> ", city, state, "\n$$$$$$$\n")

        print("search ...")
        sleep(1)
        driver.get(url_city_state)
        sleep(3)


        num_links = 0
        links = []

        links, num_links_new = get_links()

        while num_links_new - num_links != 0:
            print("num_links_new,  num_links >>", num_links_new,  num_links )
            num_links = num_links_new
            do_the_scroll()
            links, num_links_new = get_links()

        if num_links > 0:
            items = []
            for link in links:
                print("\n############\n Processing page =>",  link, "\n############\n")
                try:
                    driver.get(link)
                    sleep(3)

                    item = get_itm()
                    print("len(item) >>", len(item))
                    print(item)
                    items.append(item)
                except Exception as e:
                    print("no link ", e, "\n?????\n", traceback.format_exc(), "\n?????\n")
            df_items = pd.DataFrame(items)
            tag = datetime.datetime.now().strftime("%Y%m%d")
            df_items.to_csv(f"search_results_{city}_{state}_{tag}.csv")

            print(df_items.head(1))

            try:
                driver.close()
                print("Browser closed.")
            except:
                print("No browser")
            report = "SUCCESS!"
            print(report)
        else:
            try:
                driver.close()
                print("Browser closed.")
            except:
                print("No browser")
            report = "NO RESULTS FOUND."
            print("NO RESULTS FOUND.")

    except Exception as e:
        report = "ERROR! " + str(e)

    print(report)
    messagebox.showinfo(report)
    time.sleep(3)

    return report
# -----------------
# TKINTer WIDGETS
# ------------------
window = Tk()
window.geometry('500x300')
window.title("HUD Properties Scraper")
window.configure(background='light gray')

label = Label(window, width=40, text="Enter CITY and STATE then CLICK TO RUN:", bg="yellow")
label.pack(pady=10)

label_r1 = Label(window, width=20, text="CITY e.g. New York:", bg="light blue")
label_r1.pack(pady=2)
entry1 = Entry(window, width=30)
entry1.pack(pady=10, ipady=2)

label_r2 = Label(window, width=20, text="STATE e.g. NY:", bg="light blue")
label_r2.pack(pady=2)
entry2 = Entry(window, width=8)
entry2.pack(pady=10, ipady=2)

button = Button(window, text="Run Scraper", width=15,
                height=2, bg="light blue", command=main)
button.pack(pady=10)

window.mainloop()

# ====================
# END
# ====================
