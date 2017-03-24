#!/usr/bin/python
# -*- coding: utf8 -*-

from lxml import etree
import urllib.request
import logging
import re


def get():
    request = urllib.request.Request("http://kakoysegodnyaprazdnik.ru/")
    request.add_header('User-Agent', 'Opera/10.00 (X11; Linux x86_64 ; U; ru) Presto/2.2.0')
    request.add_header('Accept-Charset', 'utf-8')
    opener = urllib.request.build_opener()
    data = opener.open(request).read()
    tree = etree.HTML(data.decode("utf-8"))
    r = tree.xpath("//*[@id='main_frame']/div[@class='listing']/div[@class='listing_wr']/*/div[@class='main']")
    for i in r:
        for el in i.iterchildren():
            if el.tag=="a":
                yield el.get("href"), el.getchildren()[0].text
            elif el.get("itemprop")=='text':
                yield None, el.text

#print(r)

def render():
    yield "*Праздники сегодня*"
    yield ""
    for i,j in get():
        if i:
            yield "[%s](http://kakoysegodnyaprazdnik.ru/%s)"%(j,i)
        else:
            yield "%s"%j

def holiday_handler(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text="\n".join(render()), parse_mode="Markdown", disable_web_page_preview=True)

