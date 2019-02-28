# coding: utf-8
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys
import requests
import re
import math
import os
import csv
import pandas as pd
from codecs import encode

url = 'https://bihua.51240.com/e9a39e__bihuachaxun/'

s1 = "的"
print(type(s1.encode('utf-8')), s1.encode('utf-8'))
print(len(s1.encode('utf-8')))


s = str(encode(s1.encode('utf-8'), "hex"), "utf-8")
print(s)



class StrokeOrderScrapy(object):
    pass



def craw():
    pass


if __name__ == '__main__':
    craw()