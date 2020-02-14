# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
import re


class SteamscrapeSpider(scrapy.Spider):
    name = "steamscrape"
    start_urls = [
        "https://store.steampowered.com/search/?sort_by=Reviews_DESC&os=linux%2Cwin&filter=globaltopsellers"
    ]

    def parse(self, response):
        for result in response.css("a.search_result_row"):
            #price = result.css("div.search_price::text").get().strip()
            link = result.css("*::attr(href)").get().strip()
            # if not price:
            #    try:
            #        price = result.css(
            #            "div.discounted::text").extract()[-1].strip()
            #    except IndexError:
            #        price = "unknown"
            # cbargs = {"title": result.css("span.title::text").get(), "price": price}
            try:
                price = result.css(
                    "div.discounted::text").extract()[-1].strip()
                oldprice = result.css("div.discounted strike::text").get().strip()
            except:
                continue
            cbargs = {
                "title": result.css("span.title::text").get(),
                "oldprice": oldprice,
                "discountprice": price,
            }
            yield scrapy.Request(link, cookies = {'birthtime': '568022401'}, callback=self.parsegame, cb_kwargs=cbargs)
        nextlink = response.css("a.pagebtn::attr(href)").extract()[-1]
        if nextlink is not None:
            yield scrapy.Request(nextlink, callback=self.parse)

    def parsegame(self, response, title, oldprice, discountprice):
        try:
            totalreviews = response.css(
                "span.user_reviews_count::text").get()[1:-1]
        except TypeError:
            totalreviews = "unknown"
        try:
            good = response.css(
                'label[for="review_type_positive"] span.user_reviews_count::text'
            ).get()[1:-1]
        except TypeError:
            good = "unknown"
        yield {
            "title": title,
            "discountprice": discountprice,
            "oldprice": oldprice,
            "totalreviews": totalreviews,
            "posreviews": good,
        }
