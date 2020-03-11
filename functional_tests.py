from selenium import webdriver

browser = webdriver.Firefox(executable_path="geckodriver-v0.26.0-linux64/geckodriver")
browser.get('http://localhost:8000')

assert 'Django' in browser.title