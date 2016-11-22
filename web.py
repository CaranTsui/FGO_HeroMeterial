#coding=utf-8

from selenium import webdriver
import time

#XPaths
levelXPath = "//*[@id='row-move']/div[2]/div/div[4]/div[3]/div[4]/div/div/div"
skillXPath = "//*[@id='row-move']/div[2]/div/div[4]/div[3]/div[5]/div/div"
nameXPath = "//*[@id='row-move']/div[2]/div/div[2]/div/div/table[1]/tbody/tr[1]/th/div"
#selenium driver
## use Chrome instead of PhantomJS for a faster speed


#def readHtml():
#    #todo: driver return a session. up to now don't know how to
#    #      parse them. Another method is find all div but seems 
#    #      stupid. Work on it later
#    level = driver.find_element_by_xpath(levelXPath)    
#    for img in soup.find_all("img"):
#        print (img.get("src"))
#
#def getHtml():
#    for i in range(1,2):
#        driver.get("http://fgowiki.com/guide/petdetail/" + str(i))    
#        time.sleep(3)
#        readHtml()
#        
    #find element by class name   
    #   breakdata = driver.find_element_by_class_name("break-databox")
    #save the html stand alone. DONE.
    #   a = open(str(i) + ".html", "wb")
    #   a.write(driver.page_source.encode('gbk', 'ignore'))
    #   a.flush()
    #   a.close()
    #   driver.get_screenshot_as_file(str(i) + ".jpg")
    
#    driver.close()   
    
def getHeroName(driver):
    name = driver.find_element_by_xpath(nameXPath).text
    return name
    
def getHeroLevelUp(driver)    :
    levelInfoDict = {}
    levelElement = driver.find_element_by_xpath(levelXPath)
    levels = levelElement.find_elements_by_class_name('cf')
    i = 1
    for level in levels:
        nextButton = level.find_element_by_xpath(levelXPath + '/div[' + str(i) + ']/div[2]')
        lv = level.find_element_by_class_name('lv').text        
        items = level.find_elements_by_tag_name('li')
        itemsDict = {}
        for item in items:
            itemCount = item.find_element_by_class_name('ItemGroupNum').text
            itemName = item.find_element_by_tag_name('img').get_attribute('src')
            itemsDict[itemName] = itemCount            
        levelInfoDict[lv] = itemsDict     
        i = i + 1  
        nextButton.click() 
    
    return levelInfoDict
    
def getHeroSkillUp(driver)    :
    skillupInfoDict = {}
    skillElement = driver.find_element_by_xpath(skillXPath)
    skills = skillElement.find_elements_by_class_name('cf')    
    i = 1
    for skill in skills:
        nextButton = skill.find_element_by_xpath(skillXPath + '/div[' + str(i) + ']/div[2]')
        lv = skill.find_element_by_class_name('lv').text     
        items = skill.find_elements_by_tag_name('li')
        itemsDict = {}
        for item in items:
            itemCount = item.find_element_by_class_name('ItemGroupNum').text
            itemName = item.find_element_by_tag_name('img').get_attribute('src')
            itemsDict[itemName] = itemCount            
        skillupInfoDict[lv] = itemsDict   
        i = i + 1       
        nextButton.click()   
        
    return skillupInfoDict
    
    
if __name__ == '__main__':
    #main 
    #1. init a driver
    driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
    driver.get("http://fgowiki.com/guide/petdetail/2")
    time.sleep(3)
    
    #2. get the hero info
    #2.1 get hero name
    name = getHeroName(driver)
    
    #2.2 get hero level up
    levelInfo = getHeroLevelUp(driver)
#    levelInfo = sorted(levelInfo.iteritems(), key=lambda d:d[0]) 
    
    #2.3 get hero skill up
    skillInfo = getHeroSkillUp(driver)
#    skillInfo = sorted(skillInfo.iteritems(), key=lambda d:d[0]) 
    
    driver.close()
    driver.quit()
    
    print 'Hero Name is: ', name
    print 'skill\n'
    for key, value in skillInfo.items():
        for v in value.items():            
            print key, ' ', v, '\n'
    
    print 'level\n'   
    for key, value in levelInfo.items(): 
        for v in value.items():            
            print key, ' ', v, '\n'
        
    print 'FGO'


    

 