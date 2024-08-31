

from googleform import GoogleForm
from selenium import webdriver
from selenium.webdriver.common.by import By


class WebScraper:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument("--disable-popup-blocking")
        self.chrome_options.add_argument("--no-first-run")
        self.chrome_options.add_argument("--no-default-browser-check")
        self.driver = webdriver.Chrome(options=self.chrome_options)


        self.url="https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/malopolskie/krakow/krakow/krakow?ownerTypeSingleSelect=ALL&priceMax=3000&areaMin=30&viewType=listing&limit=72"
        self.data={}

        self.index=0

        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36'
        }

        self.ul_ids=['#__next > div.css-1bx5ylf.e50rtj23 > main > div > div.css-1d0gimt.e50rtj21 > div.css-feokcq.e50rtj24 > div.ef1jqb0.css-1cvir3j > div.css-1i43dhb.ef1jqb1 > div:nth-child(2) > ul',
                     '#__next > div.css-1bx5ylf.e50rtj23 > main > div > div.css-1d0gimt.e50rtj21 > div.css-feokcq.e50rtj24 > div.ef1jqb0.css-1cvir3j > div.css-1i43dhb.ef1jqb1 > div:nth-child(3) > ul:nth-child(2)',
                     '#__next > div.css-1bx5ylf.e50rtj23 > main > div > div.css-1d0gimt.e50rtj21 > div.css-feokcq.e50rtj24 > div.ef1jqb0.css-1cvir3j > div.css-1i43dhb.ef1jqb1 > div:nth-child(3) > ul:nth-child(2)']

        self.next_page_url='https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/malopolskie/krakow/krakow/krakow?ownerTypeSingleSelect=ALL&priceMax=3000&areaMin=30&viewType=listing&limit=72&page=2'

        self.iteration=0

    def create_objects(self,price,address,link):

        self.data[self.index]={"price":price,"address":address,"link":link}

        self.index+=1
        print("SCRAPING...")



    def start_scraping(self):

        self.driver.get(self.url)

        #accept cookies
        cookies=self.driver.find_element(By.XPATH,value='//*[@id="onetrust-accept-btn-handler"]')
        cookies.click()


        for id in self.ul_ids:

            if self.iteration == 2:

                self.driver.get(self.next_page_url)

            self.iteration += 1

            ul_element=self.driver.find_element(By.CSS_SELECTOR,value=id)
            all_li_elements=ul_element.find_elements(By.TAG_NAME,value="li")



            nbr_of_all_li_elements=len(all_li_elements)



            for li_el in range (0,nbr_of_all_li_elements):

                #spans=all_li_elements[li_el].find_elements(By.TAG_NAME,value="span")
                spans = all_li_elements[li_el].find_elements(By.XPATH, value=".//span[normalize-space(text()) != '']")
                print("\n\nNEXT PROPERTY ")

                nbr_spans=len(spans)
                real_price=None

                for n in range(0,nbr_spans):
                    #algorithm finding price through number of spans
                    if spans[n].text!="":

                        real_price=spans[n].text
                        break

                if real_price!=None:


                    paragraphs=all_li_elements[li_el].find_elements(By.TAG_NAME,value="p")


                    nbr_p = len(paragraphs)
                    real_address = []

                    for n in range(0,nbr_p):
                        #algorithm finding price through number of spans
                        if paragraphs[n].text!="":

                            real_address.append(paragraphs[n].text)



                    link=all_li_elements[li_el].find_element(By.TAG_NAME,value="a")

                    link=link.get_attribute("href")



                    #if there is no complications then save all the data

                    address=real_address[-1]

                    self.create_objects(real_price, address, link)
                    print("OMNOMNOM")


                else:
                    print("EMPTY")


    def all_data_ready_to_send(self):
        self.driver.quit()
        nbr_properties=len(self.data)
        print(f"\n\nNUMBER OF PROPERTIES: {nbr_properties}")

        googleform=GoogleForm()
        googleform.send_values(self.data)
        print("\nALL DATA HAS BEEN SENT\n THAT WAS EASY! !")
