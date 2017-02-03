#!/usr/bin/env python
# -*- coding: utf-8 -*-

import html2text
import urllib.request
import logging
import re


def web_handler(bot, update, args):
    url = "".join(args)
    logging.info("Parsing %s" % url)
    request = urllib.request.Request(url)
    request.add_header('User-Agent', 'Opera/10.00 (X11; Linux x86_64 ; U; ru) Presto/2.2.0')
    request.add_header('Accept-Charset', 'utf-8')
    opener = urllib.request.build_opener()
    data = opener.open(request).read()
    text = html2text.html2text(data.decode("utf-8"), baseurl=url)
    text = re.sub(
        "^\\s+\\*",
        "",
        text,
        flags=re.MULTILINE
    )
    logging.info(text[:2048])
    bot.sendMessage(
        chat_id=update.message.chat_id,
        disable_web_page_preview=True,
        text=text[:2048]
    )


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    web_handler(1, 2, [
        'http://mgorod.kz/nitem/v-dvd-zko-soobshhili-familii-pisayushhego-policejskogo-i-ego-nakazannyx-nachalnikov/'])
