# monitoring_urls.py  
import json
import time  
from Utils import Paths  
  
monitoringUrls = []  # 新建一个数组用于存储监控URL  
  
def AddMonitoringUrl(newUrl):  
    global monitoringUrls  # 声明MonitoringUrl为全局变量，以便在函数内部进行修改  
  
    # 先读取Paths.settingJsonPath中的现有settings  
    with open(Paths.settingJsonPath, 'r') as file:  
        settings = json.load(file)  # 读取JSON文件中的数据为settings字典  
    monitoringUrls = settings['monitoringUrls']  
    if len(monitoringUrls[0])==0:
        monitoringUrls=[]

    # 检查newUrl是否已经存在于MonitoringUrls中  
    if not len(monitoringUrls)<=1:
        for savedUrl in monitoringUrls:  
            if savedUrl['savedUrl'] == newUrl:  
                print("该URL已存在，无需重复添加。")  
                return  # 如果已存在，则直接返回，不进行后续操作  

    # 新建一个字典，包含两个key-value  
    currentTime=time.time()
    newDict = {  
        "savedUrl": newUrl, 
        "valid": True,
        "lastNewTime":currentTime,
        "finalPage":1
        }  
  
    # 将这个字典新增进MonitoringUrls  
    monitoringUrls.append(newDict)  
  
    settings['monitoringUrls'] = monitoringUrls  # 将MonitoringUrl数组作为字典的一个元素，key为'MonitoringUrl'  
  
    with open(Paths.settingJsonPath, 'w') as file:  # 使用settingJsonPath变量的值打开setting.json文件进行写入操作  
        json.dump(settings, file, indent=4)  # 将字典数据保存到setting.json文件中，并使用缩进进行格式化  
        print(f"已经新增新监控中的Url: {newUrl}")  
  
def GetMonitoringUrls():  
    global monitoringUrls  # 声明MonitoringUrls为全局变量  
    if monitoringUrls:  
        return monitoringUrls  
    else:  
        with open(Paths.settingJsonPath, 'r') as file:  
            settings = json.load(file)  # 读取JSON文件中的数据为settings字典  
        monitoringUrls = settings['monitoringUrls']  
        return monitoringUrls  
          
def InvalidMonitoringUrls(TargetUrl):  
    global monitoringUrls  # 声明MonitoringUrl为全局变量，以便在函数内部进行修改  
    with open(Paths.settingJsonPath, 'r') as file:  
        settings = json.load(file)  # 读取JSON文件中的数据为settings字典  
    monitoringUrls = settings['monitoringUrls']  
    found = False  # 添加一个标志变量，用于记录是否找到目标URL  
    for savedUrl in monitoringUrls:  # 将url改名为savedUrl  
        if savedUrl['savedUrl'] == TargetUrl:  # 如果savedUrl的值等于TargetUrl  
            savedUrl['valid'] = False  # 将valid设为False  
            found = True  # 设置找到目标URL的标志为True  
            break  # 找到目标后退出循环  
    if not found:  # 如果没有找到目标URL  
        print("未找到对应的TargetUrl")  # 打印提示信息  
        return None  # 返回空值  
    settings['monitoringUrls'] = monitoringUrls  # 将修改后的MonitoringUrls列表保存回settings字典中  
    with open(Paths.settingJsonPath, 'w') as file:  # 将修改后的settings字典保存回setting.json文件中  
        json.dump(settings, file, indent=4)  # 使用缩进进行格式化保存  
    print("已将{TargetUrl}的valid设为False")

def SetFinalPage(targetUrl, finalPage):  
    print(f"设置{targetUrl}的末页: {finalPage}")
    global monitoringUrls  # 声明MonitoringUrls为全局变量，以便在函数内部进行修改  
    with open(Paths.settingJsonPath, 'r') as file:  
        settings = json.load(file)  # 读取JSON文件中的数据为settings字典  
    monitoringUrls = settings['monitoringUrls']  
    for savedUrl in monitoringUrls:  # 遍历MonitoringUrls列表中的每个元素（字典）  
        if savedUrl['savedUrl'] == targetUrl:  # 如果savedUrl的值等于TargetUrl  
            savedUrl['finalPage'] = finalPage  # 将finalPage设为给定的值  
            break  # 找到目标后退出循环  
    else:  # 如果没有找到目标URL  
        print("未找到{targetUrl}")  # 打印提示信息  
        return None  # 返回空值  
    settings['monitoringUrls'] = monitoringUrls  # 将修改后的MonitoringUrls列表保存回settings字典中  
    with open(Paths.settingJsonPath, 'w') as file:  # 将修改后的settings字典保存回setting.json文件中  
        json.dump(settings, file, indent=4)  # 使用缩进进行格式化保存  
    print(f"已设置{targetUrl}的末页: {finalPage}")  
  
def GetFinalPage(targetUrl): 
    print(f"获取{targetUrl}的末页")
    global monitoringUrls  # 声明MonitoringUrls为全局变量  
    if not monitoringUrls:   
        with open(Paths.settingJsonPath, 'r') as file:  
            settings = json.load(file)  # 读取JSON文件中的数据为settings字典  
        monitoringUrls = settings['monitoringUrls']  
    for savedUrl in monitoringUrls:  # 遍历MonitoringUrls列表中的每个元素（字典）  
        if savedUrl['savedUrl'] == targetUrl:  # 如果savedUrl的值等于TargetUrl 
            finalPage=1
            if savedUrl.get('finalPage'):
                finalPage=savedUrl.get('finalPage')
            print(f"{targetUrl}的末页: {finalPage}")
            return finalPage # 返回finalPage的值（如果存在）

    print("未找到TargetUrl: {targetUrl}或finalPage不存在")  # 如果未找到目标URL或finalPage不存在，则打印提示信息  
    return None  # 返回空值

def DeleteInvalidUrls():  
    print("取消监视不可用的Url")
    global monitoringUrls  # 声明monitoringUrls为全局变量，以便在函数内部进行修改  
    invalidUrls = []  
    
    with open(Paths.settingJsonPath, 'r') as file:  
        settings = json.load(file)  # 读取JSON文件中的数据为settings字典  
        monitoringUrls = settings['monitoringUrls'] 

    # 遍历monitoringUrls列表中的每个元素（字典），找出valid为false的记录并添加到invalid_urls列表中  
    for url in monitoringUrls:  
        if not url['valid']:  
            invalidUrls.append(url)  
              
    # 从monitoringUrls列表中删除无效的URL记录  
    for url in invalidUrls:  
        monitoringUrls.remove(url)  
          
    # 将修改后的monitoringUrls列表保存回settings字典中  
    settings['monitoringUrls'] = monitoringUrls  
      
    # 将修改后的settings字典保存回setting.json文件中  
    with open(Paths.settingJsonPath, 'w') as file:  # 将修改后的settings字典保存回setting.json文件中  
        json.dump(settings, file, indent=4)  # 使用缩进进行格式化保存  
    
    print("已经取消监视不可用的Url: {invalidUrls}")
          
def DeleteMonitoringUrl(targetUrl): 
    global monitoringUrls  # 声明monitoringUrls为全局变量，以便在函数内部进行修改  
      
    with open(Paths.settingJsonPath, 'r') as file:  
        settings = json.load(file)  # 读取JSON文件中的数据为settings字典  
        monitoringUrls = settings['monitoringUrls'] 
    # 遍历monitoringUrls列表中的每个元素（字典），找出savedUrl为targetUrl的记录并删除  
    for i, url in enumerate(monitoringUrls):  
        if url['savedUrl'] == targetUrl:  
            del monitoringUrls[i]  # 删除目标URL记录  
            break  # 找到目标后退出循环  
              
    # 将修改后的monitoringUrls列表保存回settings字典中  
    settings['monitoringUrls'] = monitoringUrls  
      
    # 将修改后的settings字典保存回setting.json文件中  
    with open(Paths.settingJsonPath, 'w') as file:  # 将修改后的settings字典保存回setting.json文件中  
        json.dump(settings, file, indent=4)  # 使用缩进进行格式化保存
    print(f"已不再监视{targetUrl}")
  
urls = GetMonitoringUrls()  # 调用GetMonitoringUrls方法获取监控URL列表  
print("当前的监控URL列表：", urls)

#print(GetFinalPage("https://bbs.nga.cn/read.php?tid=38675941"))


#invalidUrl = input("无效化的URL: ")  # 修改了提示信息  
#InvalidMonitoringUrls(invalidUrl)

#DeleteInvalidUrls()
#DeleteMonitoringUrl("https://bbs.nga.cn/read.php?tid=38668561")