# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

from core.crawler.baiduzhidao import baidu_count
from main import pre_process_question


class OcrTestCase(TestCase):
    """unittest"""

    def test_baidu_ocr(self):
        """
        test baidu ocr

        :return:
        """
        from core.ocr.baiduocr import get_text_from_image

        print("test baidu ocr")
        app_id = "10712738"
        app_key = "98QhwoCzoZxKoZbX5XWNPld4"
        app_secret = "MGYLv1BeHjWOGFc9IjZPfzuhlPlaBEWA"

        with open("screenshots/text_area.png", "rb") as fp:
            message = get_text_from_image(fp.read(), app_id, app_key, app_secret, 0, 10)
            print(message)

    def test_detect_direction(self):
        """
        Test baidu api direction

        :return:
        """
        from core.ocr.baiduocr import get_text_from_image

        print("test baidu ocr direction")
        app_id = "10712738"
        app_key = "98QhwoCzoZxKoZbX5XWNPld4"
        app_secret = "MGYLv1BeHjWOGFc9IjZPfzuhlPlaBEWA "

        with open("screenshots/screenshot.png", "rb") as fp:
            import time
            start = int(time.time())
            message = get_text_from_image(fp.read(), app_id, app_key, app_secret, 10)
            print("time spend: ", int(time.time()) - start)
            print(message)

    def test_image_count(self):
        """

        :return:
        """
        from PIL import Image
        count_white = 0
        with Image.open("screenshots/screenshot.png") as img:
            w, h = img.size
            for pix in img.getdata():
                if all([i >= 240 for i in pix[:3]]):
                    count_white += 1

            print(count_white / (w * h))

    def test_crawler(self):
        """
        Test baidu crawler

        :return:
        """
        from core.crawler.crawl import kwquery
        from core.crawler.crawl import jieba_initialize
        jieba_initialize()
        query = "回锅肉属于什么菜系"
        query = "北京奥运会是什么时候"
        ans = kwquery(query)
        print("~~~~~~~")
        for a in ans:
            print(a)
        print("~~~~~~~")

    def test_preparse_question(self):
        """
        Test pre parse question

        :return:
        """
        question = "我国什么时候开始改革开放"
        print(pre_process_question(question))

        question = "今天是什么日子"
        print(pre_process_question(question))

        question = "这个月有多少天"
        print(pre_process_question(question))

    def test_baidu_word_count(self):
        a = baidu_count("全世界第一部公映的有声动画片是？", ["威利号汽船", "小熊维尼", "猫和老鼠"])
        print(a)

    def test_sougou_bs4(self):
        """
        测试搜狗接口
        1. vrwrap, str-text-info / str-green-skin
        2. vrwrap, vr-box-border  keep span
        :return: 
        """
        import requests
        from bs4 import BeautifulSoup
        resp = requests.get("https://www.sogou.com/web?query=全世界第一部公映的有声动画片是")
        soup = BeautifulSoup(resp.content, "lxml")
        answer_elements = soup.find_all("div", class_="vrwrap")
        for element in answer_elements:
            for best in element.find_all("div", class_="str-text-info"):
                if best.find("i", "str-green-skin"):
                    print(best.span.get_text())

    def test_pseg(self):
        """
        test pseg for some words
        
        :return: 
        """
        from core.crawler.text_process import postag
        for i in postag("8点钟"):
            print(i)


if __name__ == "__main__":
    unittest.main()
