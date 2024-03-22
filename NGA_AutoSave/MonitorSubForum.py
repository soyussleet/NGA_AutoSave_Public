import requests  
import json  
import CookieFormat  
import Paths
import re

# 公开变量  
monitoringSubForumUrls = []  
cookies = ''  
  
def GetMonitoringSubForumUrls():  
    """  
    获取当前监控中的版面URL列表。  
    """  
    global monitoringSubForumUrls  
    if not monitoringSubForumUrls:  
        with open(Paths.settingJsonPath, 'r') as f:  
            settings = json.load(f)  
        monitoringSubForumUrls = settings.get('monitoringSubForumUrls', [])  
    return monitoringSubForumUrls  
   
def AddMonitoringSubForumUrls(targetUrl):  
    """  
    将指定的URL添加到监控中的版面列表中。  
    """  
    global monitoringSubForumUrls  
    urls = GetMonitoringSubForumUrls()  
    if targetUrl not in urls:  
        urls.append(targetUrl)  
        with open(Paths.settingJsonPath, 'w') as f:  
            json.dump({'monitoringSubForumUrls': urls}, f, ensure_ascii=False)  
        print(f"已将{targetUrl}添加到监控中的版面")  
        monitoringSubForumUrls = urls  # 同步更新公开变量  
    else:  
        print(f"{targetUrl}已存在于监控中的版面")  
  
def DeleteMonitoringSubForumUrls(targetUrl):  
    """  
    从监控中的版面列表中移除指定的URL。  
    """  
    global monitoringSubForumUrls  
    urls = GetMonitoringSubForumUrls()  
    if targetUrl in urls:  
        urls.remove(targetUrl)  
        with open(Paths.settingJsonPath, 'w') as f:  
            json.dump({'monitoringSubForumUrls': urls}, f, ensure_ascii=False)  
        print(f"已从监控中的版面移除{targetUrl}")  
        monitoringSubForumUrls = urls  # 同步更新公开变量  
    else:  
        print(f"{targetUrl}不在监控中的版面")  
  
def GetHotPost():  
    urls = GetMonitoringSubForumUrls()  
    postsArray = []  
    for url in urls:  
        # 检查cookies是否为空，如果为空则调用CookieFormat.GetCookies()获取cookies  
        if not cookies:  
            cookies = CookieFormat.GetCookies()  
        # 对每个URL发送请求并获取响应作为页面内容  
        response = requests.get(url, cookies=cookies)  
        html = response.text  
        postUrlRegex = r'<a id=.*? title="打开新窗口" href=".*?" target=".*?" class=".*?" style=".*?">(\d+)</a>'  
        postUrlRegexObj = re.compile(postUrlRegex)  
        matches = postUrlRegexObj.findall(html)  
        for match in matches:  
            postUrl = match[0]  
            postReplyCnt = int(match[1])  
            postsArray.append({"postUrl": postUrl, "postReplyCnt": postReplyCnt})  
    return postsArray