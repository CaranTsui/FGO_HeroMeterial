#coding=utf-8

from selenium import webdriver
import time
import io 
import os
import threading

#XPaths

#selenium driver
## use Chrome instead of PhantomJS for a faster speed
 
class GetAnFGOHero():
    levelXPath = "//div[@class='break-databox']"
    skillXPath = "//div[@class='skill-databox']"
    nameXPath = "//div[@class='textsmall NAME']"
    driver = None
    name = ''
    levelInfoDict = {}
    skillupInfoDict = {}
    
    def __init__(self, driverType='default'):
        '''
        Init an engine to get the hero info, giving the driver type
        '''
        if driverType == 'default':
           self.driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
        elif str.lower(driverType) == 'phantomjs':
           self.driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
        elif str.lower(driverType) == 'chrome':
           self.driver = webdriver.Chrome(executable_path='chromedriver.exe')
        else:
           self.driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
     
    def getHeroName(self, ):
        self.name = self.driver.find_element_by_xpath(self.nameXPath).text        
        
    def getHeroLevelUp(self, )    :
        levelInfoDict = {}
        levelElement = self.driver.find_element_by_xpath(self.levelXPath)
        levels = levelElement.find_elements_by_class_name('cf')
        i = 1
        for level in levels:
            nextButton = level.find_element_by_xpath(self.levelXPath + '/div[' + str(i) + ']/div[2]')
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
        
        self.levelInfoDict = levelInfoDict
        
    def getHeroSkillUp(self, )    :
        skillupInfoDict = {}
        skillElement = self.driver.find_element_by_xpath(self.skillXPath)
        skills = skillElement.find_elements_by_class_name('cf')    
        i = 1
        for skill in skills:
            nextButton = skill.find_element_by_xpath(self.skillXPath + '/div[' + str(i) + ']/div[2]')
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
            
        self.skillInfoDict = skillupInfoDict
    

    def getAnHeroInfo(self, serialNum)        :
        if self.driver is None:
            return 
            
        self.driver.get('http://fgowiki.com/guide/petdetail/' + str(serialNum))
        #1. get hero name                
        self.getHeroName()        
        a = io.open('FGOHero.csv', 'a', encoding = 'utf-8')
        nameStr = str(serialNum) + ',' +  self.name + '\n'
        a.write(nameStr)
        a.flush()
        a.close()
        
        #2. get all the info
        self.getHeroLevelUp()
        self.getHeroSkillUp()
        self.driver.close()
        self.driver.quit()
        b = io.open('FGO.csv', 'a', encoding = 'utf-8')
        for key, value in self.skillInfoDict.items():
             for v in value.items():   
                 skillStr = str(serialNum) + ',skill,' + key + ',' + os.path.splitext(os.path.split(v[0])[1])[0] + ',' + v[1] + '\n'
                 b.write(skillStr)
                 b.flush()
        
        for key, value in self.levelInfoDict.items(): 
            for v in value.items():   
                levelStr = str(serialNum) + ',level,' + key + ',' + os.path.splitext(os.path.split(v[0])[1])[0] + ',' + v[1] + '\n'
                b.write(levelStr)
                b.flush()
        
        b.flush()
        b.close()
        print self.name, ' finish.'
        
        
def getHero(index)        :
    newClassTest = GetAnFGOHero('chrome')
    newClassTest.getAnHeroInfo(index)
        
if __name__ == '__main__':
#    threads = []
#    for i in range(5):
#        t = threading.Thread(target=getHero, args=(i,))
#        threads.append(t)
#        
#    for tt in threads:
#        tt.setDaemon(True)        
#        tt.start()
#        tt.join()
        
    getHero(3)
#    #main 
#    #1. init a driver
#    driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
#    driver.get("http://fgowiki.com/guide/petdetail/2")
#    time.sleep(3)
#    
#    a = io.open('FGO.csv', 'w', encoding = 'utf-8')
#    
#    #2. get the hero info
#    #2.1 get hero name
#    name = getHeroName(driver)
#    
#    #2.2 get hero level up
#    levelInfo = getHeroLevelUp(driver)
##    levelInfo = sorted(levelInfo.iteritems(), key=lambda d:d[0]) 
#    
#    #2.3 get hero skill up
#    skillInfo = getHeroSkillUp(driver)
##    skillInfo = sorted(skillInfo.iteritems(), key=lambda d:d[0]) 
#    
#    driver.close()
#    driver.quit()
#            
#    print 'Hero Name is: ', name
#    print 'skill\n'
#    for key, value in skillInfo.items():
#        for v in value.items():      
#            skillStr = name + ',skill,' + key + ',' + v[0] + ',' + v[1] + '\n'
##            print skillStr
#            a.write(skillStr)
##            a.write(unicode(skillStr, "utf-8"))
#            a.flush()
##            print key, ' ', v, '\n'
#    
#    print 'level\n'   
#    for key, value in levelInfo.items(): 
#        for v in value.items():    
#            levelStr = name + ',level,' + key + ',' + v[0] + ',' + v[1] + '\n'
##            print levelStr
#            a.write(levelStr)
##            a.writeline(unicode(levelStr, "utf-8"))
#            a.flush()
##            print key, ' ', v, '\n'
#    a.close()    
#    print 'FGO'


    

 