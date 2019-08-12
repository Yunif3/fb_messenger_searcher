from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
import sys, time

def send(facebook, output):
    messenger = facebook.find_element_by_xpath("//div[@aria-label='Type a message...']")
    messenger.send_keys(output)
    messenger.send_keys(Keys.ENTER)

def wiki():
    query = last_message[last_message.find(' '):].strip()
    wiki = webdriver.Chrome()
    wiki.get('https://www.wikipedia.com')
    searchbar = wiki.find_element_by_id('searchInput')
    searchbar.send_keys(query)
    searchbar.submit()

    if 'Search' in wiki.title:
        first = wiki.find_element_by_xpath("//div[@class='mw-search-result-heading']/a")
        output = first.get_attribute('href')
    else:
        output = wiki.current_url
    wiki.quit()
    return output

def define():
    query = last_message[last_message.find(' '):].strip()
    webster = webdriver.Chrome()
    webster.get('https://www.dictionary.com/browse/' + query)
    print(query)
    try:
        output = query + ' definition) \n' 
        output = output + webster.find_element_by_xpath("//span[@class='luna-pos']").text + '\n'
        output = output + webster.find_element_by_xpath("//div[@class='css-kg6o37 e1q3nk1v3']").get_attribute("innerText")
    except:
        output = "incorrect word"
    return output

def slang():
    query = last_message[last_message.find(' '):].strip()
    urban_dictionary = webdriver.Chrome()
    urban_dictionary.get('https://www.urbandictionary.com/define.php?term=' + query)
    print(query)
    try:
        output = query + ' definition) \n' 
        output = output + urban_dictionary.find_element_by_xpath("//div[@class='meaning']").get_attribute("innerText")
    except:
        output = "incorrect word"
    return output

display = Display(visible=0, size=(800, 800))
display.start()

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://www.facebook.com/messages')

email = driver.find_element_by_id('email')
password = driver.find_element_by_id('pass')

email.send_keys(sys.argv[1])
password.send_keys(sys.argv[2])
password.submit()

driver.implicitly_wait(1)
while(True):
    user = driver.find_element_by_xpath("//ul[@aria-label='Conversation List']")
    user = user.find_element_by_xpath(".//li/div/a")
    user.click()

    time.sleep(3)
    user_check = driver.find_element_by_xpath("(//div[@class='_41ud'])[last()]/div/div")
    print(user_check.get_attribute('data-tooltip-position') == 'left')
    if user_check.get_attribute('data-tooltip-position') == 'left':
        last_message = driver.find_element_by_xpath("(//div[@class='_41ud'])[last()]/div/div/div/span").text
        print(last_message)
        if 'Wiki' in last_message:
            output = wiki()
            send(driver, output)
        
        elif 'Define' in last_message or 'Def' in last_message:
            output = define()
            send(driver, output)
        
        elif 'Slang' in last_message:
            output = slang()
            send(driver, output)

        elif 'Quit' in last_message:
            output = "quitting the program"
            send(driver, output)
            
            driver.quit()
            display.stop()
            break



