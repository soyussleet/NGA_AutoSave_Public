import json
import time  
from Utils import Paths  
  
monitoringUrls = []  
  
def InitUrls():  
    """  
    初始化URLs，从文件中读取数据到内存中，并删除可能存在的空字典。  
    """  
    global monitoringUrls  
    with open(Paths.settingJsonPath, 'r', encoding='utf-8') as f:  
        settings = json.load(f)  
        monitoringUrls = settings.get('monitoringUrls', [])  
    # 删除可能存在的空字典  
    monitoringUrls = [url for url in monitoringUrls if url]  
  
def AddUrl(targetUrl,isAutoAddHotPost=False):  
    """  
    向数组中增加一条记录，确保不重复添加相同的targetUrl。  
    参数：  
        targetUrl (str): 要添加的URL字符串。  
    """  
    global monitoringUrls  
    if len(targetUrl)<10 or ( "http" not in targetUrl):
        print(f"{targetUrl}不合规范")
        return
    if '&page=' in targetUrl:#以免复制url时带上了第几页
        targetUrl = targetUrl.split('&page=')[0]
    if any(url['savedUrl'] == targetUrl for url in monitoringUrls):  
        print(f"URL {targetUrl} 已存在，不再添加。")  
        return  
    currentTimestamp = int(time.time())  # 当前时间戳  
    new_url_dict = {  
        "savedUrl": targetUrl,   
        "valid": True,  
        "lastNewTime": currentTimestamp,  
        "finalPage": 1,  
        "isAutoAddHotPost":isAutoAddHotPost
    }  
    monitoringUrls.append(new_url_dict)  
    # 更新到文件中  
    UpdateToJson()  
  
def GetUrls():  
    """  
    返回 monitoringUrls 数组。  
    """  
    return monitoringUrls  
  
def SetUrlArg(targetUrl, argName, newValue):  
    """  
    修改指定URL的参数。如果targetUrl不存在，则给出提示。  
    参数：  
        targetUrl (str): 要修改的URL字符串。  
        argName (str): 要修改的参数名。可选值为'valid', 'lastNewTime', 'finalPage'。  
        newValue: 新的参数值。类型根据参数名而定。  
    """   
    global monitoringUrls  
    for urlDict in monitoringUrls:  
        if urlDict['savedUrl'] == targetUrl:  
            if argName == 'valid':  
                urlDict['valid'] = newValue  
            elif argName == 'lastNewTime':  
                urlDict['lastNewTime'] = newValue  
            elif argName == 'finalPage':  
                urlDict['finalPage'] = newValue  
            # 更新到文件中  
            UpdateToJson()  
            return  
    print(f"URL： {targetUrl} 不存在，无法修改。")  
  
def GetUrlArg(targetUrl, argName):  
    """  
    输出指定url的指定argName的值。如果targetUrl不存在，则给出提示。 
    参数：  
    targetUrl (str): 要修改的URL字符串。  
    argName (str): 要修改的参数名。可选值为'valid', 'lastNewTime', 'finalPage'。
    """  
    global monitoringUrls  
    for urlDict in monitoringUrls:  
        if urlDict['savedUrl'] == targetUrl:  
            if argName == 'valid':  
                return (urlDict['valid'])  
            elif argName == 'lastNewTime':  
                return(urlDict['lastNewTime'])  
            elif argName == 'finalPage':  
                return(urlDict['finalPage'])
            else:
                print(f"找不到参数：{argName}")
    print(f"URL： {targetUrl} 不存在")

    
def UpdateToJson():  
    """  
    将 monitoringUrls 的更改更新到 Paths.settingJsonPath 文件中，而不影响文件的其他部分。  
    """  
    with open(Paths.settingJsonPath, 'r', encoding='utf-8') as f:  
        settings = json.load(f)  
      
    # 仅更新 monitoringUrls 部分  
    settings['monitoringUrls'] = monitoringUrls  
      
    # 写回文件  
    with open(Paths.settingJsonPath, 'w', encoding='utf-8') as f:  
        json.dump(settings, f, ensure_ascii=False, indent=4)


def DeleteUrl(targetUrl):  
    """  
    删除 monitoringUrls 中与 targetUrl 匹配的记录。  
    """  
    global monitoringUrls  
    monitoringUrls = [url for url in monitoringUrls if url['savedUrl'] != targetUrl]  
    print(f"已删除{targetUrl}（或本就没有这个URL）")
    UpdateToJson()  
  
def DeleteInvalidUrls():  
    """  
    删除 monitoringUrls 中所有 valid=False 的记录。  
    """  
    global monitoringUrls  
    monitoringUrls = [url for url in monitoringUrls if url.get('valid', True)]  
    print(f"已删除不可用URL")
    UpdateToJson()

InitUrls()