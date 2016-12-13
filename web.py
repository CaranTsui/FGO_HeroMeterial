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
        print str(serialNum), ' finish.'
        
    def quitDriver(self,):
        self.driver.close()
        self.driver.quit()
        
    def getAMaterialInfo(self, serialNum):
        if self.driver is None:
            return 
            
        self.driver.get('http://fgowiki.com/guide/materialdetail/' + str(serialNum))
        fullmaterialName = self.driver.find_element_by_xpath("//div[@class='leftico']").find_element_by_tag_name('img').get_attribute('src')
        materialName = os.path.splitext(os.path.split(fullmaterialName)[1])[0]
        materialChName = self.driver.find_element_by_xpath("//div[@class='textsmall itemname']").text
        materialStr = str(serialNum) + ',' +  materialName + ',' + materialChName + '\n'
        a = io.open('FGOMaterial.csv', 'a', encoding = 'utf-8')
        a.write(materialStr)
        a.flush()
        a.close()
        
        
#=====================
import Queue    
import threading  
clawClassQueue = Queue.Queue(maxsize=10)
driverType='chrome'
lock = threading.Lock()
count = 0

def beforeBegin(classNum = 4):
    global clawClassQueue
    for i in range(1, classNum + 1):
        newClawClass = GetAnFGOHero(driverType)    
        clawClassQueue.put(newClawClass)
    
def getHero(index)        :
    global clawClassQueue    
    global count
    global lock
    while clawClassQueue.empty() is True:  
        print 'Zzz...'          
        time.sleep(30)
    t1 = time.time()
    newClassTest = clawClassQueue.get()
    newClassTest.getAnHeroInfo(index)    
    clawClassQueue.put(newClassTest)
    t2 = time.time()
    print str(index), ' ', str(t2-t1)
    count = count + 1
    if count == 149:
        lock.release()
        
def getMaterial(index):
    global clawClassQueue 
#    global count
    while clawClassQueue.empty() is True:  
        print 'Zzz...'          
        time.sleep(30)
        
    t1 = time.time()
    newClassTest = clawClassQueue.get()
    newClassTest.getAMaterialInfo(index)    
    clawClassQueue.put(newClassTest)
    t2 = time.time()
    print 'Material ', str(index), ' ', str(t2-t1)
#    count = count + 1
#    if count == 74:
#        lock.release()
    
def quitAllClass():
    global clawClassQueue  
    global lock
    lock.acquire()
    while clawClassQueue.empty() is not True:
        newClassTest = clawClassQueue.get()
        newClassTest.quitDriver()    
    lock.release()

        
if __name__ == '__main__':
    try:
        beforeBegin(classNum=4)
        lock.acquire()
        for i in range(1,75):
            t = threading.Thread(target=getMaterial, args=(i,))
            t.start()
            
        for i in range(1,150):
            t = threading.Thread(target=getHero, args=(i,))
            t.start()
    finally:
        quitAllClass()
