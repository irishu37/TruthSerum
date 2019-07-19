import selenium
import webbrowser

from selenium import webdriver
from selenium.webdriver.common.by import By


def find_first_tweet(URL):

        driver = webdriver.Chrome()
        driver.get(URL)
        driver.execute_script("window.stop()")
        elem = driver.find_element_by_css_selector("div[data-permalink-path]")
        path = elem.get_attribute("data-permalink-path")

        full_path = "https://www.twitter.com" + path
        webbrowser.open(full_path)

        return full_path


