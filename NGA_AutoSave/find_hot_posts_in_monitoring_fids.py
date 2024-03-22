# 假设M_requests是您自定义的模块，它基于requests库  

from bs4 import BeautifulSoup  
from Utils import M_requests
import CookieFormat  
import monitor_fid_urls_manager 
import MonitorUrlsV2

threshold = monitor_fid_urls_manager.get_hot_post_lowest_limit()  
BASE_URL = 'https://bbs.nga.cn' 
  
# 获取监控的URL列表  
monitoring_fid_urls = monitor_fid_urls_manager.get_monitoring_fid_urls()  
cookies = CookieFormat.GetCookies() 
  
def get_html_content(url):  
    """使用M_requests和提供的Cookie获取指定URL的HTML内容"""  
    global cookies
      
    try:  
        # 使用M_requests发送GET请求，并传入cookies参数  
        response = M_requests.get(url, cookies=cookies)  
        response.raise_for_status()  # 检查请求是否成功  
        
        print(f"获取版面内容: {url}")
        return response.text  
    except M_requests.RequestException as e:  
        print(f"Error fetching HTML content from {url}: {e}")  
        return None  
  
def extract_post_info(html):  
    """从HTML内容中提取帖子标题、链接和回帖数量"""  
    soup = BeautifulSoup(html, 'html.parser')  
    # 查找所有帖子行  
    post_rows = soup.find_all('tr', class_=['row1 topicrow', 'row2 topicrow'])  # 假设帖子行是'row1'或'row2'  
    post_info = []  
      
    for post_row in post_rows:  
        # 查找回帖数量的<a>标签  
        replies_elem = post_row.find('a', class_='replies')  
        if replies_elem:  
            replies = replies_elem.text  
        else:  
            replies = None  
          
        # 查找帖子标题的<a>标签  
        title_elem = post_row.find('a', class_='topic')  
        if title_elem:  
            title = title_elem.text  
            link = title_elem.get('href')  
        else:  
            title = None  
            link = None  
          
        # 收集信息  
        post_info.append({  
            'title': title,  
            'link': link,  
            'replies': replies  
        })  
    return post_info 
  
def collect_post_info():  
    all_post_info = []  
    for url in monitoring_fid_urls:  
        html_content = get_html_content(url)  
        if html_content:  
            posts_info = extract_post_info(html_content)  
            all_post_info.extend(posts_info)  
    return all_post_info  
  
def add_hot_posts_to_save_urls(collected_post_info=None):  
    """将高热帖子保存入监控url中"""
    global threshold
    
    if(collected_post_info==None):
        collected_post_info=collect_post_info()
      
    # 遍历所有帖子分析数据  
    for post_info in collected_post_info:  
        # 检查是否满足阈值条件  
        if int(post_info['replies']) > threshold:  # 回复数量  
            post_title=post_info['title']
            
            #过滤标题，使其不含关键字
            titleFilteredWords=monitor_fid_urls_manager.getHotPostTitleFilter()
            titleFilteredPass=False
            for titleFilteredWord in titleFilteredWords:
               if titleFilteredWord in post_title:
                   titleFilteredPass=True
                   break
            if titleFilteredPass:
               continue

            # 提取帖子链接并补足URL  
            relative_url = post_info['link']  
            target_url = BASE_URL+relative_url
              
            # 调用MonitorUrlsV2.AddUrl函数添加URL  
            MonitorUrlsV2.AddUrl(target_url, isAutoAddHotPost=True)  
            print(f"热帖链接: {target_url}，标题：{post_info['title']}，回帖数：{post_info['replies']}") 


# 调用collect_post_info函数并打印结果  
#all_posts_analysis = collect_post_info()  
#print(all_posts_analysis)
#process_hot_posts()