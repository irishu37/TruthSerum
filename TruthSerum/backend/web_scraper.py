import selenium
import webbrowser

from selenium import webdriver
from selenium.webdriver.common.by import By


def find_first_tweet(URL):
        print(URL)
        # Changing options to run chrome headless and not to load image assets
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        chromeOptions.add_argument('headless');
        driver = webdriver.Chrome(chrome_options=chromeOptions)


        driver.get(URL)
        try:
            elem = driver.find_element_by_css_selector("div[data-permalink-path]")
            print(elem)
            path = elem.get_attribute("data-permalink-path")
            driver.quit()

            full_path = "https://www.twitter.com" + path
        except:
            print("No tweet found")
            return None


        return full_path


