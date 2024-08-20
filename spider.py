# This is a sample Python script.

# 原始思路和代码于CSDN博主「Parzival_」的原创文章中提出，链接：https://blog.csdn.net/Parzival_/article/details/122360528
# 本代码由lijinhai0804进行优化，主要是升级使用为selenium 4版本的包，且适配了更通用的Chrome浏览器，版本118.2993.70（正式版本）（64 位）。
# 交流讨论：lijinhai0804@whu.edu.cn;https://github.com/lijinhai0804
# 使用前需要安装selenium 4和 webdriver-manager, openpyxl, xlrd, pandas. 在pycharm中可以直接安装最新版，非常方便！
# 转载请附上原文出处链接及上述声明。

from selenium import webdriver
import os
from selenium.webdriver.common.by import By
import time

from bs4 import BeautifulSoup

# 强烈建议用校园网的IP登录，非常方便不用进行login。login函数默认注释掉，有需要的人可以启用。
# def login(driver):
#     '''登录wos'''
#     # 通过CHINA CERNET Federation登录
#     driver.find_element(By.CSS_SELECTOR, '.mat-select-arrow').click()
#     driver.find_element(By.CSS_SELECTOR, '#mat-option-9 span:nth-child(1)').click()
#     driver.find_element(By.CSS_SELECTOR,
#                         'button.wui-btn--login:nth-child(4) span:nth-child(1) span:nth-child(1)').click()
#     time.sleep(3)
#     login = driver.find_element(By.CSS_SELECTOR, '#show')
#     login.send_keys('武汉大学')  # 改成你的学校名
#     time.sleep(2)
#     driver.find_element(By.CSS_SELECTOR, '.dropdown-item strong:nth-child(1)').click()
#     driver.find_element(By.CSS_SELECTOR, '#idpSkipButton').click()
#     time.sleep(1)
#     # ! 跳转到学校的统一身份验证(想自动输入账号密码就把下面两行注释解除,按照自己学校的网址修改一下css选择器路径)
#     # driver.find_element(By.CSS_SELECTOR, 'input#un').send_keys('你的学号') # 改成你的学号/账号
#     # driver.find_element(By.CSS_SELECTOR, 'input#pd').send_keys('你的密码') # 改成你的密码
#     time.sleep(20)  # ! 手动输入账号、密码、验证码，点登录


def send_key(driver, path, value):
    '''driver -> driver;\n
       path -> css选择器;\n
       value -> 填入值
    '''
    markto = driver.find_element(By.CSS_SELECTOR, path)
    markto.clear()
    markto.send_keys(value)


def rename_file(SAVE_TO_DIRECTORY, name, record_format='excel'):
    '''导出文件重命名 \n
       SAVE_TO_DIRECTORY -> 导出记录存储位置(文件夹)；\n
       name -> 重命名为
    '''
    # files = list(filter(lambda x:'savedrecs' in x and len(x.split('.'))==2,os.listdir(SAVE_TO_DIRECTORY)))
    while True:
        files = list(filter(lambda x: 'savedrecs' in x and len(x.split('.')) == 2, os.listdir(SAVE_TO_DIRECTORY)))
        if len(files) > 0:
            break

    files = [os.path.join(SAVE_TO_DIRECTORY, f) for f in files]  # add path to each file
    files.sort(key=lambda x: os.path.getctime(x))
    newest_file = files[-1]
    # newest_file=os.path.join(SAVE_TO_DIRECTORY,'savedrecs.txt')
    if record_format == 'excel':
        os.rename(newest_file, os.path.join(SAVE_TO_DIRECTORY, name + ".xls"))
    elif record_format == 'bib':
        os.rename(newest_file, os.path.join(SAVE_TO_DIRECTORY, name + ".bib"))
    else:
        os.rename(newest_file, os.path.join(SAVE_TO_DIRECTORY, name + ".txt"))


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
       record_num -> 需要导出的记录条数(检索结果数); \n
       SAVE_TO_DIRECTORY -> 记录导出存储路径(文件夹)，在代码末尾设置;\n
       reverse -> 是否设置检索结果降序排列, default=False \n
       ----------------------------------------------------
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


# 主要参数修改在此
# 所参考的原创代码出自于CSDN博主「Parzival_」的原创文章,转载请附上原文出处链接及本声明。
# 原创文章链接：https://blog.csdn.net/Parzival_/article/details/122360528
# 本代码由@lijinhai0804(https://github.com/lijinhai0804)进行优化，主要是升级使用为selenium 4版本的包，且适配了更通用的Chrome浏览器。

if __name__ == '__main__':
    # WOS“检索结果”页面的网址
    tasks = [
        # {
        #     'url': 'https://www.webofscience.com/wos/alldb/summary/32909a2c-18f2-4a0d-8223-850f75a01fee-0102e122e8/date-descending/1',
        #     'o_authors': 'Gao, C (Gao, Chao); Zhu, JY (Zhu, Junyou); Zhang, F (Zhang, Fan); Wang, Z (Wang, Zhen); Li, XL (Li, Xuelong)',
        #     'o_title': 'A Novel Representation Learning for Dynamic Graphs Based on Graph Convolutional Networks'
        # },
        # {
        #     'url': 'https://www.webofscience.com/wos/alldb/summary/e60d6ae9-4932-4d16-b04c-1bcf3ca476c2-0102eb2fbf/date-descending/1',
        #     'o_authors': 'Gao, C (Gao, Chao); Yin, Z (Yin, Ze); Wang, Z (Wang, Zhen); Li, XH (Li, Xianghua); Li, XL (Li, Xuelong)',
        #     'o_title': 'Multilayer Network Community Detection: A Novel Multi-Objective Evolutionary Algorithm Based on Consensus Prior Information'
        # },
        {
            # 'url': 'https://www.webofscience.com/wos/alldb/summary/7ac418cf-4361-44d3-99fd-82544dd59979-0102f0337b/date-descending/1',
            'url': 'https://www.webofscience.com/wos/alldb/basic-search',
            'o_authors': 'Gao, C (Gao, Chao); Su, Z (Su, Zhen); Liu, JM (Liu, Jiming); Kurths, J (Kurths, Juergen)',
            'o_title': 'Even Central Users Do Not Always Drive Information Diffusion'
        },
        # {
        #     'url': 'https://www.webofscience.com/wos/alldb/summary/b63a9f6b-afe8-4a1f-a31b-46bd966a8f52-0102eb3e4b/date-descending/1',
        #     'o_authors': 'Gao, C (Gao, Chao); Fan, Y (Fan, Yi); Jiang, SH (Jiang, Shihong); Deng, Y (Deng, Yue); Liu, JM (Liu, Jiming); Li, XH (Li, Xianghua)',
        #     'o_title': 'Dynamic Robustness Analysis of a Two-Layer Rail Transit Network Model'
        # },
        # {
        #     'url': 'https://www.webofscience.com/wos/alldb/summary/90f593ac-c9e6-4344-81d1-b9cd7808574c-0102eb53b2/date-descending/1',
        #     'o_authors': 'Gao, C (Gao, Chao); Liu, JM (Liu, Jiming); Zhong, N (Zhong, Ning)',
        #     'o_title': 'Network immunization with distributed autonomy-oriented entities'
        # },
        # {
        #     'url': 'https://www.webofscience.com/wos/alldb/summary/f45be0a2-0ea5-46fc-98ea-cfda7860812a-0102eb60ce/date-descending/1',
        #     'o_authors': 'Gao, C (Gao, Chao); Liu, JM (Liu, Jiming)',
        #     'o_title': 'Network-based modeling for characterizing human collective behaviors during extreme events'
        # },
        # {
        #     'url': 'https://www.webofscience.com/wos/alldb/summary/15b3fa67-d557-4f9f-afaf-47009b12770f-0102eb6f23/date-descending/1',
        #     'o_authors': 'Gao, C (Gao, Chao); Liu, JM (Liu, Jiming)',
        #     'o_title': 'Modeling and restraining mobile virus propagation'
        # },
        # {
        #     'url': 'https://www.webofscience.com/wos/alldb/summary/048a1ad7-179d-41ba-bb16-2b89582661ba-0102eb7c36/date-descending/1',
        #     'o_authors': 'Gao, C (Gao, Chao); Liu, JM (Liu, Jiming); Zhong, N (Zhong, Ning)',
        #     'o_title': 'Network immunization and virus propagation in email networks: experimental evaluation and analysis'
        # },
        # {
        #     'url': 'https://www.webofscience.com/wos/alldb/summary/2391d557-3da4-4aee-bd6e-fcce7e57b633-0102eb8819/date-descending/1',
        #     'o_authors': 'Zhu, PC (Zhu, Peican); Cheng, L (Cheng, Le); Gao, C (Gao, Chao); Wang, Z (Wang, Zhen); Li, XL (Li, Xuelong)',
        #     'o_title': 'Locating multi-sources in social networks with a low infection rate'
        # },
        # {
        #     'url': 'https://www.webofscience.com/wos/alldb/summary/ce9a20e9-4c31-4ca0-a09c-aef46aa13082-0102eb9903/date-descending/1',
        #     'o_authors': 'Wang, Z (Wang, Zhen); Hou, DP (Hou, Dongpeng); Gao, C (Gao, Chao); Huang, JJ (Huang, Jiajin); Xuan, Q (Xuan, Qi)',
        #     'o_title': 'A rapid source localization method in the early stage of large-scale network propagation'
        # }
    ]
    # 导出到本地的存储路径(自行修改)
    references_res = {}
    pc = 0
    for t in tasks:
        url = t['url']
        o_authors = t['o_authors']
        o_authors = o_authors.split(';')
        o_title = t['o_title']

        download_path = r'D:\a-study\wos-spider'  # 最前面加r，就可以避免保留字符冲突问题，注意斜杠是向右下
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