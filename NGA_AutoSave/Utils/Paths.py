import json
import os
import subprocess


settingFolderPath='.\Settings'
cookieTxtPath=settingFolderPath+'\cookie.txt'
settingJsonPath=settingFolderPath+'\setting.json'
settingTemplatePath=settingFolderPath+'\settingTemplate.json'

def InitSettingsFile():  
    """  
    检查./Settings文件夹下是否存在setting.json文件，  
    如果不存在，则将同一文件夹下的settingTemplate.json复制并重命名为setting.json。  
    """  
  
    # 检查目标文件是否存在  
    if not os.path.exists(settingJsonPath):  
        # 如果目标文件不存在，则复制源文件到目标文件  
        with open(settingTemplatePath, 'rb') as source:  
            with open(settingJsonPath, 'wb') as target:  
                target.write(source.read())  
        print("已生成setting.json")  

def InitCookieFile():
    if not os.path.exists(cookieTxtPath):  
        # 如果不存在，则在settingFolderPath下创建新的cookie文件  
        new_cookie_file_path = os.path.join(settingFolderPath, 'cookie.txt')  
        with open(new_cookie_file_path, 'w') as file:  
            file.write('')  # 创建空白文件  
        print(f"Cookie文件不存在，已在 {settingFolderPath} 下创建新的cookie.txt文件")  
        subprocess.run(["notepad", cookieTxtPath])


# 检测以创建setting.json文件
InitSettingsFile()
InitCookieFile()

saveHtmlFolderPath=''
if(len(saveHtmlFolderPath)==0):
    with open(settingJsonPath, 'r', encoding='utf-8') as f:  
        settings = json.load(f)
        saveHtmlFolderPath=settings['saveHtmlFolderPath']
