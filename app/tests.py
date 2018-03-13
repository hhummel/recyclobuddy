from django.test import TestCase

# Create your tests here.

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://localhost:8800')

assert 'Django' in browser.title
