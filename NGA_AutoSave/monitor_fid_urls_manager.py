import json  
import os  
  
# 设置setting.json文件的路径  
SETTINGS_FILE_PATH = os.path.join('Settings', 'setting.json')  
  
def read_settings():  
    """读取setting.json文件并返回其内容"""  
    with open(SETTINGS_FILE_PATH, 'r', encoding='utf-8') as file:  
        return json.load(file)  
  
def write_settings(settings):  
    """将设置写回setting.json文件"""  
    with open(SETTINGS_FILE_PATH, 'w', encoding='utf-8') as file:  
        json.dump(settings, file, indent=4)  
  
def add_monitoring_fid_url(url):  
    """向monitoringFidUrls列表中添加一个fid_url"""  
    settings = read_settings()  
    monitoring_fids = settings.get('monitoringFidUrls', [])  
    if url not in monitoring_fids:  
        monitoring_fids.append(url)  
        settings['monitoringFidUrls'] = monitoring_fids  
        write_settings(settings)  
        print(f"Added {url} to monitoring fids.")  
    else:  
        print(f"{url} is already in monitoring fids.")  
  
def remove_monitoring_fid_url(url):  
    """从monitoringFidUrls列表中移除一个fid"""  
    settings = read_settings()  
    monitoring_fids = settings.get('monitoringFidUrls', [])  
    if url in monitoring_fids:  
        monitoring_fids.remove(url)  
        settings['monitoringFidUrls'] = monitoring_fids  
        write_settings(settings)  
        print(f"Removed {url} from monitoring fids.")  
    else:  
        print(f"{url} is not in monitoring fids.")  
        
def get_monitoring_fid_urls():  
    """返回所有的monitoringFidUrls"""  
    settings = read_settings()  
    return settings.get('monitoringFidUrls', [])  

def get_hot_post_lowest_limit():
    """返回热帖最小值"""  
    settings = read_settings()  
    return settings.get('hotPostLowestLimit')  

def update_hot_post_lowest_limit(new_limit):  
    """更新热帖最小值，仅当new_limit为整数时进行修改""" 
    try  :
        new_limit=int(new_limit)
    except: 
        print("热帖阈值必须是整数")  
        return False  
      
    settings = read_settings()  
    settings['hotPostLowestLimit'] = new_limit  
    write_settings(settings)  
    return True  
  
def update_need_auto_add_hot_post(new_value):  
    """更新是否需要监控版面热帖，仅当new_value为0或1时进行修改"""  
    if not isinstance(new_value, int) or new_value not in [0, 1]:  
        print("开关版面热帖监控必须为 0 (for False) or 1 (for True).")  
        return False  
      
    settings = read_settings()  
    settings['needAutoAddHotPost'] = bool(new_value)  # 将0或1转换为False或True  
    write_settings(settings)  
    return True

def get_need_auto_add_hot_post():  
    """获取是否需要监控版面热帖"""  
    settings = read_settings()  
    return settings.get('needAutoAddHotPost', None)  

def getHotPostTitleFilter():
    """获取热帖标题过滤器"""  
    settings = read_settings()  
    return settings.get('hotPostTitleFilter', None)  
    
  