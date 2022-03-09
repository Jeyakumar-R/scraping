# from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
# from selenium import webdriver
# input for the search name
print("*******************************SCRAPING*********************************")
search_name =input('What You Want To Scrap? Enter A Title Here : ')
# page input
headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36','DNT':'1',
       'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ta;q=0.6'}
url = "https://www.amazon.in/s?k=" + str(search_name)
request = requests.get(url,headers=headers)
status=True
while True:
    if request.status_code==200:
        
            # get the request response output
        print(request)
        soup = BeautifulSoup(request.content, 'lxml')
        find_page_no=soup.find_all("div",attrs={"class":"a-section a-text-center s-pagination-container","role":"navigation"})
        for find_page in find_page_no:
            find_page_no=find_page.findAll('span',attrs={'aria-disabled':"true"})
        #print("There Are "+find_page_no+ " Pages")
        print(find_page_no[1].get_text())
        page_nos = int(input("How Many Pages Wanted: "))
        # save outputs
        output_data = []
        title = []
        mrp=[]
        price = []
        rating = []
        availability = []
        review = []
        #common url string
        if int(find_page_no[1].get_text())>=page_nos:
            for i in range(1, page_nos + 1):
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36','DNT':'1',
                    'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ta;q=0.6'}
                url = "https://www.amazon.in/s?k=" + str(search_name) + "&page=" + str(
                    i) + "&qid=1632499249&ref=sr_pg_" + str(i) 
                request = requests.get(url,headers=headers)
                # get the request response output
                soup = BeautifulSoup(request.content, 'lxml')
                # all the division outer
               
                for outer_div_tag in soup:
                   
                    outer_div_tag = soup.find_all(class_="sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 s-list-col-right")
                    print(outer_div_tag)
                for pprice in outer_div_tag:
                    pp=pprice.find('span',class_='a-price-whole')
                    try:
                        price.append(pp.text)
                        print(price)
                    except AttributeError:
                        price.append("NA")
                for single_a_tag in outer_div_tag:
                   
                    whole_href = single_a_tag.find(class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal", href=True)
                    separate_href=whole_href['href']
                    #print(whole_href)
                    # extract all href from the a tag
                    # for separate_href in whole_href:
                    #     temp_separate_href = separate_href['href']
                        #print(temp_separate_href)
                        # split all the href links and convert into list
                    for single_href in  separate_href.split():
                            final_href = "https://www.amazon.in" + single_href
                            final_separate_href = list(final_href.split(" "))
                            #print(final_separate_href)
                            # open all the separated list
                            for separate_url in final_separate_href:
                                request2 = requests.get(separate_url,headers=headers)
                                soup2 = BeautifulSoup(request2.content, 'lxml')
                                product_title = soup2.select_one(selector='#productTitle')
                                product_mrp=soup2.find("span",class_="priceBlockStrikePriceString a-text-strike")
                                product_price = soup2.find("span",id=['priceblock_ourprice','priceblock_dealprice'],class_='a-size-medium a-color-price offer-price a-text-normal')
                                product_rating = soup2.find("span", attrs={'data-hook': 'rating-out-of-text'})
                                product_stock = soup2.find("div",attrs={"id":"availability"})
                                product_review = soup2.find('a',attrs={'data-hook':'see-all-reviews-link-foot'},href=True)
                                product_author = soup2.select('#bylineInfo')
                                try:
                                    pt = product_title.get_text().strip()
                                    title.append(pt)
                                    print(title)              
                                except AttributeError:
                                    title.append("unknown product")
                                try:
                                    mrp.append(product_mrp.text)
                                except AttributeError:
                                    mrp.append("NA")
                                try:
                                    rating.append(product_rating.text)
                                    print(rating)
                                except AttributeError:
                                    rating.append("NA")
                                try:
                                    product_stock=product_stock.find("span")
                                    availability.append(product_stock.text.strip())
                                    print(availability)
                                except AttributeError:
                                    availability.append("Out Of Stock")
                                try:
                                    review_href="https://www.amazon.in"+product_review['href']
                                    request3=requests.get(review_href,headers=headers)
                                    soup3=BeautifulSoup(request3.content,'lxml')
                                    review_find=soup3.find("div",attrs={'data-hook':'cr-filter-info-review-rating-count'})
                                    review_find=review_find.find("span").get_text().strip()
                                    global_rating,separator,global_review=review_find.partition(" | ")
                                    review.append(global_review)
                                    print(review)
                                except (TypeError,AttributeError):
                                    review.append("NA")
                                    
        else:
            print('please enter  valid page no')
        
        # ##print("titles",title)
        # ##print(review)
        # ###print(len(title))
        # ####file_name=input("enter file name")
        # #####print(title)
        # ##print(mrp)
        # ##print(price)
        # ##print(review)
        # ##print(availability)
        # ##print(rating)
        data = pd.DataFrame.from_dict({'TITLE': title, "MRP":mrp,"DEAL OF THE DAY":price,"RATING":rating,"AVAILABILY":availability,"GOBAL_REVIEW_COUNT":review})
        data.to_csv("C:\mini project\dataas.csv", encoding="utf-8")
        break
    else:
        print("false")
        status=False
        time.sleep(4)
