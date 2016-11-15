from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time

#XPaths
levelXPath = "//*[@id='row-move']/div[2]/div/div[4]/div[3]/div[4]/div/div/div"
skillXPath = "//*[@id='row-move']/div[2]/div/div[4]/div[3]/div[5]/div/div"

#selenium driver
## use Chrome instead of PhantomJS for a faster speed
driver = webdriver.Chrome(executable_path="chromedriver.exe")

def readHtml():
    #todo: driver return a session. up to now don't know how to
    #      parse them. Another method is find all div but seems 
    #      stupid. Work on it later
    level = driver.find_element_by_xpath(levelXPath)
    soup = bs(level)
    for img in soup.find_all("img"):
        print (img.get("src"))

def getHtml()
    for i in range(1,2):
        driver.get("http://fgowiki.com/guide/petdetail/" + str(i))    
        time.sleep(3)
        readHtml()
        
    #find element by class name   
    #   breakdata = driver.find_element_by_class_name("break-databox")
    #save the html stand alone. DONE.
    #   a = open(str(i) + ".html", "wb")
    #   a.write(driver.page_source.encode('gbk', 'ignore'))
    #   a.flush()
    #   a.close()
    #   driver.get_screenshot_as_file(str(i) + ".jpg")
    
    driver.close()       


    

 