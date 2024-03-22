import json  
import os  
from Utils import Paths  
 

settingJsonPath=Paths.settingJsonPath
cookieTxtPath=Paths.cookieTxtPath
savedCookies={}

def SplitCookieAndSave(cookieStr):  
    global savedCookies
    cookieDict = {}  
    for line in cookieStr.splitlines():  
        if line.strip():  # 检查这一行是否为空
            lineSplit=line.split('\t')
            key, value = lineSplit[0].strip(), lineSplit[1].strip()  # 使用制表符（tab）作为分隔符，并取出第一、二个元素作为key和value，同时去除空格  
            if('nga' in lineSplit[2] or '178' in lineSplit[2]):
                cookieDict[key] = value  
      
    settings = {}  
    savedCookies=cookieDict

    with open(settingJsonPath, 'r', encoding='utf-8') as f: 
        settings = json.load(f)  
        settings['cookies'] = cookieDict  
    with open(settingJsonPath, 'w', encoding='utf-8') as f:  
        json.dump(settings, f)  
        print(f'Cookie已成功保存！\n{cookieDict}') 
        return cookieDict  # 成功保存后返回cookie_dict  
  
def UserInputCookie():  

    with open(cookieTxtPath, 'r', encoding='utf-8') as f:  
        f.seek(0)
        cookieStr = f.read()  
        #print(f"cookieStr\n{cookieStr}")
    
    if len(cookieStr) > 100: 
        cookieDict= SplitCookieAndSave(cookieStr)  # 如果cookieStr长度大于10，则调用SplitCookieAndSave方法并返回其结果  
        #print(f'cookie_dict\n{cookie_dict}')
        return cookieDict
    else:  
        print("Cookie字符串太短，请重新输入！")  # 如果cookieStr长度小于等于10，则输出提示信息并返回None表示调用失败  
        return None  # 返回None表示调用失败
  

def GetCookies():
    
    #如果存在savedCookies，则直接返回
    global savedCookies
    if len(savedCookies)>100:
        return savedCookies

    #否则， 读取文件

    needReInput=False
    # 检查文件是否存在  
    if os.path.exists(settingJsonPath) and os.path.getsize(settingJsonPath) > 0:  
        with open(settingJsonPath, 'r', encoding='utf-8') as f: 
            settings = json.load(f)  
            if len(settings['cookies'])<3:
                needReInput=True
            else:
                savedCookies=settings['cookies']
                print(f"GetCookies Success")

            #f.seek(0)
            #print(f'f.read()\n{f.read()}')
    else:  
        needReInput=True

    if needReInput:
        print(f"File {settingJsonPath} does not exist or is empty.")  
        savedCookies = UserInputCookie()

    return savedCookies
 


# 在开始运行时自动调用GetCookie方法，这里使用的是懒加载的方式，也可以在程序初始化时调用GetCookie方法。  
#GetCookie()

#UserInputCookie()