#coding=utf-8

from selenium import webdriver
import time
import io 
#XPaths
levelXPath = "//*[@id='row-move']/div[2]/div/div[4]/div[3]/div[4]/div/div/div"
skillXPath = "//*[@id='row-move']/div[2]/div/div[4]/div[3]/div[5]/div/div"
nameXPath = "//*[@id='row-move']/div[2]/div/div[2]/div/div/table[1]/tbody/tr[1]/th/div"
#selenium driver
## use Chrome instead of PhantomJS for a faster speed
 
    
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
    
    a = io.open('FGO.csv', 'w', encoding = 'utf-8')
    
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
            skillStr = name + ',skill,' + key + ',' + v[0] + ',' + v[1] + '\n'
#            print skillStr
            a.write(skillStr)
#            a.write(unicode(skillStr, "utf-8"))
            a.flush()
#            print key, ' ', v, '\n'
    
    print 'level\n'   
    for key, value in levelInfo.items(): 
        for v in value.items():    
            levelStr = name + ',level,' + key + ',' + v[0] + ',' + v[1] + '\n'
#            print levelStr
            a.write(levelStr)
#            a.writeline(unicode(levelStr, "utf-8"))
            a.flush()
#            print key, ' ', v, '\n'
    a.close()    
    print 'FGO'


    

 