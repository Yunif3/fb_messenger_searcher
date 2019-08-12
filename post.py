from selenium import webdriver
import sys, time


chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://www.facebook.com/?sk=nf')

email = driver.find_element_by_id('email')
password = driver.find_element_by_id('pass')

email.send_keys(sys.argv[1])
password.send_keys(sys.argv[2])
password.submit()

textarea = driver.find_element_by_xpath("//div[@class='_4bl9 _42n-']/textarea")
textarea.send_keys(sys.argv[3])
textarea.submit()

driver.quit()