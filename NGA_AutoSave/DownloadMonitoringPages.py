'''
TODO
response.text可以读到
<a href='/read.php?tid=38670883&page=1' title='上一页'class='pager_spacer'>上一页(1)</a>
<a href='/read.php?tid=38670883&page=3' title='下一页'class='pager_spacer'>下一页(3)</a>
这在直接打开网页时是没有的，注意。
通过存在“page=3' title='下一页'class='pager_spacer'>下一页”来判断是否有下一页，如果有，则继续访问下一页
需要给定一个起始页，会从起始页开始保存
'''

import os
import time  
import string 
#import requests  
import CookieFormat  
from Utils import Paths  
#import MonitorUrls  
import MonitorUrlsV2 
import re  
from Utils import M_requests
import monitor_fid_urls_manager
  
# 将 cookies 定义为全局变量  
cookies = None  
nextPage=1
  
def sanitize_filename(filename):  
    """标准化路径"""
    # 创建一个转换表，将非法字符映射为空格  
    trans_table = str.maketrans({k: ' ' for k in '&#<>:"|?*'})  
    # 使用转换表清理文件名  
    filename_sanitized=filename.translate(trans_table)
    return filename_sanitized

def GetPageTitle(savedUrl):
    """
    先进行一次访问，获得网页标题
    """
    global cookies  # 声明使用全局变量 cookies  
    if not cookies:  # 如果 cookies 为空，则调用 CookieFormat.GetCookies() 获取 cookies  
        cookies = CookieFormat.GetCookies()  
    response = M_requests.get(savedUrl, cookies=cookies) 
    pageTitle=""
    if response.status_code == 200:  
        match = re.search(r"<meta name='keywords' content=''><title>.*?</title>", response.text)
        if(match):
            pageTitle=match.group()[40:-8]
    return pageTitle

def GetFolderName(folderName):
    """
    当不存在文件夹路径时，创建文件夹
    """
    if not os.path.exists(folderName):  
        try:  
            os.makedirs(folderName)  
        except OSError as e:  
            print(f"创建文件夹时出错：{e}")  

def CalcUrlExpire(urlBase,finalPage,expireTime=86400):
    """
    储存此次记录的时间和末页计算帖子是否进坟，计算距离上一页新帖子过去的时间，过期则进坟。
    参数：
        expireTime：过期时间，默认为1天=86400s
    """

    lastNewTime = MonitorUrlsV2.GetUrlArg(urlBase,"lastNewTime")
    lastFinalPage = MonitorUrlsV2.GetUrlArg(urlBase,"finalPage")
    currTime=int(time.time())

    if lastFinalPage==finalPage and currTime-lastNewTime>expireTime :
        #如果上次的末页等于这次的末页，并且超时了，那么进坟
        MonitorUrlsV2.SetUrlArg(urlBase,"valid",False)
        print(f"{urlBase}已经超时，进坟")
    elif not lastFinalPage==finalPage:
        # 如果有新页，才更新新页时间和末页页码
        print(f"已经达到最后一页: {finalPage}，存在新页，更新末页时间:{currTime}、页码:{finalPage}")
        MonitorUrlsV2.SetUrlArg(urlBase,"lastNewTime",currTime)
        MonitorUrlsV2.SetUrlArg(urlBase,"finalPage",finalPage)
    else:
        print(f"已经达到最后一页: {finalPage}，无新页，距离上次末页时间:{currTime-lastNewTime}")


def DownloadWebpage(url, filename, urlBase):  
    """
    下载单个网页
    """
    global cookies  # 声明使用全局变量 cookies  
    if not cookies:  # 如果 cookies 为空，则调用 CookieFormat.GetCookies() 获取 cookies  
        cookies = CookieFormat.GetCookies()  
    response = M_requests.get(url, cookies=cookies)  
    if response.status_code == 200:  
        match = re.search(r"\(ERROR:<!--msgcodestart-->\d+<!--msgcodeend-->\)", response.text)
        if(match):
            print(f"帖子{url}访问失败: {match.group()}")
            #MonitorUrls.InvalidMonitoringUrls(urlBase)
            MonitorUrlsV2.SetUrlArg(urlBase,"valid",False)
            return response
        else:


            #尝试进行gbk和utf-8编码保存
            try:  
                sanitized_fileName=sanitize_filename(filename)
                with open(sanitized_fileName, 'w', encoding='gbk') as file:  
                    file.write(response.text)  
                    print(f"网页已成功保存为 {sanitized_fileName}")  
                    return response  
            except UnicodeEncodeError:  
                print(f"GBK编码保存失败，正在尝试UTF-8编码保存为 {filename}")  
                with open(sanitized_fileName, 'w', encoding='utf-8') as file:  
                    file.write(response.text)  
                    print(f"网页已成功保存为 {sanitized_fileName}")  
                return response
            except OSError as e:
                print(f"An error occurred while trying to open the file: {e}")
                
    else:  
        print(f"请求失败，状态码：{response.status_code}")  
        #MonitorUrls.InvalidMonitoringUrls(urlBase)
        MonitorUrlsV2.SetUrlArg(urlBase,"valid",False)
        return None  # 返回请求失败时返回的None  
  

  
def DownloadWebpageSequence(urlBase, fileNameBase, page=1):  
    """
    下载网页序列
    """
    global nextPage
    if(page==1):
        url=urlBase
        fileName=fileNameBase + ".html"
    else:
        url = urlBase + "&page=" + str(page)  
        fileName=fileNameBase + "&page=" + str(page) + ".html"
    print(f"准备下载网页{url}") 
    response = DownloadWebpage(url, fileName, urlBase)  
    if response is not None:  
        # 有返回时，如果有下一页，则递归调用本函数，然后page+1以访问下一页
        match = re.search(r"title='下一页' class='pager_spacer'>下一页\(\d+\)</a>", response.text) 
        if match:  
            nextPage = int(match.group()[37:-5])  
            if nextPage > page:  
                print(f"存在下一页: {nextPage}") 
                return DownloadWebpageSequence(urlBase, fileNameBase, nextPage)
        else:
            #当已经到了最后一页，计算进坟
            CalcUrlExpire(urlBase,page)
            nextPage=1
            return page
            
  
def DownloadMonitoringPages(): 
    """
    下载网页，入口
    """

    #monitoringUrls = MonitorUrls.GetMonitoringUrls()  
    monitoringUrls = MonitorUrlsV2.GetUrls()  
    if monitoringUrls:  
        for urlDict in monitoringUrls:  
            valid = urlDict.get("valid")  
            savedUrl = urlDict.get("savedUrl")
            try:
                autoAddHotPost=urlDict.get("isAutoAddHotPost")
            except:
                autoAddHotPost=None
            #如果这个url是热度自动添加，并且不需要热度自动添加时，则不保存这个帖子
            if autoAddHotPost==True and monitor_fid_urls_manager.get_need_auto_add_hot_post()==False:
                continue
                
            if valid:  
                if savedUrl:  
                    # 分割 savedUrl，获取 "tid=" 后的部分  
                    tidPart = savedUrl.split("tid=")[-1]  

                    # 修改文件夹名
                    folderName = Paths.saveHtmlFolderPath + "tid=" + tidPart + "_" + GetPageTitle(savedUrl)  
                    if(autoAddHotPost):
                        folderName+="_高热度自动保存"
                    # 检查文件夹是否存在，如果不存在则创建文件夹，然后进行网页下载  
                    GetFolderName(folderName)

                    # 文件名
                    fileNameBase = folderName + "/tid_" + tidPart

                    # 获取末页，从末页开始继续访问
                    finalPage=MonitorUrlsV2.GetUrlArg(savedUrl,"finalPage")
                    print(f"准备下载网页序列{savedUrl}，从{finalPage}页开始")  
                    DownloadWebpageSequence(savedUrl, fileNameBase,finalPage)  # 直接调用DownloadWebpageSequence函数，不再检查保存是否成功  
                else:  
                    print(f"获取到的 URL 列表中的{savedUrl}不是有效的 URL。")  
            else:  
                print(f"{savedUrl} 不可用。")  # 当 valid 为 false 时给出提示，内容为某某 URL 不可用  
        print("所有有效的 URL 已处理完毕。")  
    else:  
        print("获取到的 URL 列表为空。")
# 程序开始运行时调用DownloadMonitoringPages 函数，并初始化page变量（这里仅为示例，您需要根据实际情况进行赋值）   
#DownloadMonitoringPages()
