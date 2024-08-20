from selenium import webdriver
import os
from selenium.webdriver.common.by import By
import time

from bs4 import BeautifulSoup

# 用校园网的IP登录

# 判断页面元素是否存在。element处传入XPATH路径。
def isElementExist(driver, element):
    try:
        driver.find_element(By.XPATH, element)
        return True
    except:
        return False


# 以下是主要调用的核心函数
def startdownload(url, SAVE_TO_DIRECTORY):
    '''url -> 检索结果网址; \n
       SAVE_TO_DIRECTORY -> 记录导出存储路径(文件夹)，在代码末尾设置;\n
       tip1:首次打开wos必须登录,在学校统一身份认证处需要手动输入验证码并点击登录，需要用login函数;IP登录请忽视，强烈建议校园网IP登录！！！
       tip2:第一次导出时，需要手动在10秒内（下文可修改）设置好定制的内容，后续都会直接点击定制好的导出字段
       tip3:建议以下都用完整XPATH进行元素寻找，绝对不会找不到！！！
    '''
    try:
        # 创建一个Chrome配置文件对象
        ch = webdriver.ChromeOptions()
        # 设置下载目录为SAVE_TO_DIRECTORY变量的值，这应该是一个有效的本地路径,最新版selenium4无executable_path
        ch.add_experimental_option("prefs", {
            "download.default_directory": SAVE_TO_DIRECTORY,
            "download.prompt_for_download": False, })
        # 创建一个Chrome驱动对象，使用chromedriver的可执行路径和自定义的配置文件
        driver = webdriver.Chrome(options=ch)
        # 导航到url变量指定的网址，这应该是一个有效的网址
        driver.get(url)
        driver.maximize_window()  # 窗口最大化
        # 暂停脚本执行4秒，等待网页加载或渲染
        time.sleep(10)
        # 调用函数，判断是否有弹窗存在，如果有，就关闭它
        isElementExist(driver, '//*[@id="onetrust-accept-btn-handler"]')  # 调用函数，判断“接受Cookies”是否出现
        if isElementExist:
            print("Ture")
            driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()  # 按掉接受Cookies按钮
        time.sleep(15)  # 这次等待是为了让右下角的弹窗加载出来
        isElementExist(driver, '//*[@id="pendo-button-ad6c2c35"]')  # 调用函数，判断“右下角弹窗”是否出现
        if isElementExist:
            print("Ture")
            driver.find_element(By.XPATH, '//*[@id="pendo-button-ad6c2c35"]').click()  # 关闭接受COOKIES后右下角的弹窗
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="pendo-button-7775f566"]').click()  # 关闭接受COOKIES后右下角的弹窗
        time.sleep(2)
            
        driver.find_element(By.XPATH, '//*[@id="snRecListTop"]/app-export-menu/div/button/span[1]/mat-icon').click()  # 点击导出按钮
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="exportToHtmlButton"]').click() 
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '#radio3 > label > span.mat-radio-label-content').click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'body > app-wos > main > div > div > div.holder > div > div > div.held > app-input-route:nth-child(3) > app-export-overlay > div > div.window > div.window-content.ng-star-inserted > app-export-out-details > div > div.window-content.ng-star-inserted > form > div > div.flex-align.margin-top-20 > button.mat-focus-indicator.mat-flat-button.mat-button-base.mat-primary').click()
        time.sleep(5)
        driver.quit()
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    # WOS“检索结果”页面的网址
    tasks = [
        {
            "url": "被引检索页面",
            "o_authors": "原文作者列表",
            "o_title": "原文题目"
        },
        {
            "url": "被引检索页面",
            "o_authors": "原文作者列表",
            "o_title": "原文题目"
        }
    ]
    # 导出到本地的存储路径(自行修改)
    references_res = {}
    pc = 0
    for t in tasks:
        url = t['url']
        o_authors = t['o_authors']
        o_authors = o_authors.split(';')
        o_title = t['o_title']

        download_path = r'D:\wos-spider'  # 最前面加r，就可以避免保留字符冲突问题，注意斜杠是向右下
        download_file = os.path.join(download_path, 'savedrecs.html')
        if pc >= 1:
            download_file = os.path.join(download_path, 'savedrecs (' + str(pc) + ').html')
        res = False
        while not res:
            time.sleep(5)
            res = startdownload(url, download_path)  # 主要函数的参数在这设定
        with open(download_file, 'r', encoding='utf-8') as fin:
            html = fin.read()
        soup = BeautifulSoup(html, 'html.parser')
        articals = soup.find_all('table')
        count = 0
        res_list = []
        for arti in articals:
            eles = arti.find_all('tr')
            if len(eles) < 2:
                continue
            authors = ''
            title = ''
            for e in eles:
                content = e.text
                if 'Author Identifiers:' in content:
                    continue
                if 'By:' in content:
                    authors = content
                if 'Title:' in content:
                    title = content
                    break
            if authors == '' or title == '':
                continue
            flag = True
            for origin in o_authors:
                origin = origin.strip()
                # print(origin)
                if origin in authors:
                    flag = False
                    break
            if flag:
                count += 1
                res_list.append(title)
        references_res[o_title] = count
        pc += 1
        print(references_res)
    print(references_res)