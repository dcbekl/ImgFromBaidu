from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from time import sleep
import os

options = Options()
options.add_argument('--headless')  # 设置firefox浏览器无界面模式（不显示打开浏览器的界面）
"""
******** 替换 **********，如果你使用的不是火狐驱动，请替换代码
driver = webdriver.Chorme(options=options)  # 比如换成谷歌浏览器驱动
"""
driver = webdriver.Firefox(options=options)  # 火狐驱动

# 访问的网页地址
url = 'https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%B7%E7%BE%B0%CD%BC' \
      '%C6%AC&fr=ala&ala=1&alatpl=normal&pos=0&dyTabStr=MCw2LDMsMSw1LDQsMiw3LDgsOQ%3D%3D '
driver.get(url)     # 访问页面

# 根据id查询，返回一个列表，只有一个元素（css的id是唯一标识一个标签）
ls = driver.find_elements(by='id', value='imgid')[0]  # id=imgid 的标签下存放着许多class为 imgpage 的图片页，每一页存放一定量的图片，动态imgid

# 滑轮滚动次数越多，加载出的imgpage就相应越多
for i in range(2):  # 因为随着我们向下浏览图片，imgpage 是动态增加的，模拟滚轮下滚，获得更多imgpage
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    print('滚轮下滑。。。')
    sleep(0.5)

imgpages = ls.find_elements(By.CLASS_NAME, value='imgpage')  # 取出所有图片页
print('查找到的图片页数：', len(imgpages))
n = 0   # 下载图片的次数

for imgpage in imgpages:    # 遍历每一页（其实就是个ul）
    img_ls = imgpage.find_elements(By.CLASS_NAME, 'imgitem')   # 找到每页的所有图片（ul下的li）
    for img in img_ls:
        try:
            img_name = img.text + '.jpg'  # 取出li中的文本作为照片名称
            img_name = img_name.replace('/', '_')  # 如果照片名称中存在'/', 会导致文件的下载位置发生改变，故将其替换成'_'
            img_img = img.find_element(By.TAG_NAME, 'img')  # 找到 img 标签，其下的 data-imgurl 属性存放着图片的下载地址
            url_img = img_img.get_attribute('data-imgurl')  # 取出图片的下载地址
            if not os.path.exists('img_downloads'):  # 如果当前目录下没有img_downloads目录，则创建img_downloads目录，用来存放下载的图片
                os.mkdir('img_downloads')
            img_path = 'img_downloads/' + img_name   # 拼接图片的下载路径
            # urlretrieve(url_img, img_path)         # 下载图片
            n += 1
        except:
            print(img_name + '下载失败')
        else:
            print(img_name + '下载成功')
print(n)
driver.quit()   # 退出驱动