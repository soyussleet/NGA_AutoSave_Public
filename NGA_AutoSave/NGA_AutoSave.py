from datetime import datetime  
import json  
import threading  
import time
import DownloadMonitoringPages  
import monitor_fid_urls_manager
import find_hot_posts_in_monitoring_fids
from Utils import Paths  
#import MonitorUrls  
import MonitorUrlsV2
  
def auto_save():  
    with open(Paths.settingJsonPath, 'r', encoding='utf-8') as f:  
        settings = json.load(f)  
    saveCycleTimes = settings['saveCycleTime']  # 注意这里变成了times，因为现在是一个列表  

    while True:  
        # 打印当前时间  
        print(f"开始下载，当前时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  
          
        # 调用版面热帖监控  
        if monitor_fid_urls_manager.get_need_auto_add_hot_post():
            print("版面热帖监控")
            find_hot_posts_in_monitoring_fids.add_hot_posts_to_save_urls()
        # 调用网页下载函数  
            print("帖子自动下载")
        DownloadMonitoringPages.DownloadMonitoringPages()  
          
        print("\n\n输入选项: 1:新增监控URL, 2:取消监控URL, 3:取消监控不可用的URL \n4:开关版面热帖监控, 5:新增监控热帖的版面, 6:取消监控热帖的版面, 7:调整热帖回帖数阈值\n")  

        # 更新小时和对应的等待时间  
        saveCycleTime = saveCycleTimes[datetime.now().hour]
        print(f"下次循环于{saveCycleTimes[datetime.now().hour]}秒后")
        # 等待指定的循环时间  
        time.sleep(saveCycleTime)  

  
def receive_input():  
    while True:  
        choice = input("输入选项: 1:新增监控URL, 2:取消监控URL, 3:取消监控不可用的URL \n4:开关版面热帖监控, 5:新增监控热帖的版面, 6:取消监控热帖的版面, 7:调整热帖回帖数阈值\n")  
        if choice == '1':  
            targetUrl = input("请输入要新增的监控URL：\n")  
            #MonitorUrls.AddMonitoringUrl(new_url)  
            ok=MonitorUrlsV2.AddUrl(targetUrl)
            if ok:
                DownloadMonitoringPages.DownloadMonitoringPages()
        elif choice == '2':  
            targetUrl = input("请输入要取消监控的URL：\n")  
            #MonitorUrls.DeleteMonitoringUrl(target_url) 
            MonitorUrlsV2.DeleteUrl(targetUrl) 
        elif choice == '3':  
            #MonitorUrls.DeleteInvalidUrls() 
            MonitorUrlsV2.DeleteInvalidUrls() 
        elif choice == '4':  
            needAutoAddHotPostInt = input("开启版面监控输入1，关闭版面监控输入0：\n") 
            monitor_fid_urls_manager.update_need_auto_add_hot_post(needAutoAddHotPostInt)
        elif choice == '5':  
            monitoring_fid_url=input("请输入要添加监控热度的版面的URL：\n")
            monitor_fid_urls_manager.add_monitoring_fid_url(monitoring_fid_url)
        elif choice == '6':  
            monitoring_fid_url=input("请输入要添加监控热度的版面的URL：\n")
            monitor_fid_urls_manager.remove_monitoring_fid_url(monitoring_fid_url)
        elif choice == '7':  
            hotPostLowestLimit=input("请输入版面热帖回帖数阈值：\n")
            monitor_fid_urls_manager.update_hot_post_lowest_limit(hotPostLowestLimit)
            print("如要使该阈值生效，请重新启动本程序")
            
        else:  
            print("无效的输入，请重新输入。\n")  
  
if __name__ == "__main__":  
    download_thread = threading.Thread(target=auto_save)  
    input_thread = threading.Thread(target=receive_input)  
  
    download_thread.start()  # 开始运行自动保存线程  
    input_thread.start()  # 开始运行用户输入线程