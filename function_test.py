from selenium import webdriver

browser = webdriver.Safari()
browser.get('http://localhost:8090')

assert ' Django' in browser.title
