# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests, re

class Itemdata:
    title = "NA"
    imagelink = "NA" 
    rating = "NA"
    price1 = "NA"
    price2 = "NA"
    reviewcount = "NA"    
    def __init__(self, word):
       self.word = word 
    
    def set_title(self, inp):
        if inp: self.title = inp
    def set_img(self, inp):
        if inp: self.imagelink = inp
    def set_price1(self, inp):
        if inp: self.price1 = inp    
    def set_price2(self, inp):
        if inp: self.price2 = inp    
    def set_rating(self, inp):
        if inp: self.rating = inp
    def set_reviewcnt(self, inp):
        if inp: self.reviewcount = inp    


def get_url(word, page=1):
    ### to do  https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=football
    #https://www.amazon.in/s/ref=sr_pg_2?fst=as%3Aon&rh=k%3Atable%2Cn%3A976442031&page=2&keywords=table&ie=UTF8&qid=1521654137
    #https://www.amazon.in/gp/search/ref=sr_pg_1?fst=as%3Aon&rh=k%3Atable%2Cn%3A976442031&keywords=table&ie=UTF8&qid=1521654149
    link = "https://www.amazon.in/s/ref=sr_pg_" + str(page) + "?fst=as%3Aon&rh=n%3A976442031%2Ck%3A"
    return link + word + "&page=" + str(page) + "&keywords=" + word 
 
 
    
def main_scraping(word):
 
    response = requests.get(get_url(word,1))
    content = response.content.decode(encoding='UTF-8')
    soup = BeautifulSoup(content, "html.parser")
    containers = soup.find_all("div", {"class": "s-item-container"})
    Itemset = []

    for container in containers[1:]:
        Item = Itemdata(word)
        image_src, price1 = container.find_all("a",{"class":"a-link-normal a-text-normal"})
        Item.set_title(container.h2["data-attribute"])
        Item.set_img(image_src.img["src"])
        Item.set_price1(price1.text)
##aria-label='Suggested Retail Price:
    #price_cont = container.find_all("div",{"class":"a-column a-span7"})

        price2 = container.select("span[class*=a-text-strike]")
        if len(price2)!=0:  Item.set_price2(price2[0].text)    



#<a class="a-popover-trigger a-declarative" 
#span class="a-declarative"
        rating_cont = container.find_all("span",{"class":"a-icon-alt"})
        rating = ' '.join(map(str,rating_cont))
        Item.set_rating(rating)
        review_no_cont = container.select("a[href*=customerReviews]")
    
        if len(review_no_cont)!=0:  Item.set_reviewcnt(review_no_cont[0].text)
        Itemset.append(Item)    
    
    return Itemset    