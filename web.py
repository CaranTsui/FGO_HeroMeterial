#coding=utf-8

from selenium import webdriver
import time
import io 
import os
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
        try:
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
        except:
            self.levelInfoDict = levelInfoDict
        finally:
            self.levelInfoDict = levelInfoDict
        
    def getHeroSkillUp(self, )    :
        skillupInfoDict = {}
        try:
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
        except:
            self.skillInfoDict = skillupInfoDict
        finally:    
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
        filename = 'FGO_' + str(serialNum) + '.csv'
        b = io.open(filename, 'a', encoding = 'utf-8')
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
#        print self.name, ' finish.'
        print str(serialNum), ' finish.'
        
    def quitDriver(self,):
        self.driver.close()
        self.driver.quit()

#=====================
import Queue    

clawClassQueue = Queue.Queue(maxsize=10)
classNum=2
driverType='chrome'

def beforeBegin():
    global clawClassQueue
    for i in range(1, classNum + 1):
        newClawClass = GetAnFGOHero(driverType)    
        clawClassQueue.put(newClawClass)
    
def getHero(index)        :
    global clawClassQueue
    if clawClassQueue.empty() is True:  
        print 'Zzz...'          
        time.sleep(5000)
        
    newClassTest = clawClassQueue.get()
    newClassTest.getAnHeroInfo(index)
    clawClassQueue.put(newClassTest)
    
def quitAllClass():
    global clawClassQueue
    while clawClassQueue.empty() is not True:
        newClassTest = clawClassQueue.get()
        newClassTest.quitDriver()          

        
if __name__ == '__main__':
    from contextlib import closing
    from multiprocessing import Pool
     
#    newClaw.tryGet()
#    newClaw.getHero(3)
    beforeBegin()
    for i in range(1,8):
        getHero(i)
    quitAllClass()
#    while clawClassQueue.empty() is not True:
#        print 'Zzz...'
#        clawClassQueue.get()
#    with closing(Pool(processes=4)) as pool:
#        pool.map(getHero, range(1,3))
#    
#    quitAllClass()
