import time, os, requests, re
from lxml import etree
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument('log-level=3')

# driver = webdriver.Chrome("C:\Users\VIP\AppData\Local\Google\Chrome\Application\chrome.exe")
driver = webdriver.Chrome(options=option)

driver.implicitly_wait(1)
driver.maximize_window()
driver.get('https://www.taobao.com')
# time.sleep(1)

s = driver.find_element_by_class_name('drop-wrapper')
s.click()

# os.system("load_image.exe D:\\dataset_object_detect\\food-101\\images\\apple_pie\\134.jpg" )
os.system("load_image.exe D:\\comb_001.jpg")

time.sleep(0.1)

def get_html(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    html = etree.HTML(r.text)
    return r.text

html_text =  get_html(driver.current_url)

raw_title = re.findall(r'\"raw_title\"\:\".*?\"', html_text)
view_price = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html_text)

# print(raw_title)
# print(view_price)

result = dict()
for k,v in zip(raw_title, view_price):
    result.update({k.split(':')[1]: v.split(':')[1]})

print(result)