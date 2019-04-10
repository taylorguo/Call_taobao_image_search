import time, os, requests, re, csv, time
from lxml import etree
from selenium import webdriver

img_folder = 'D:\\dataset_object_detect\\open_image_dataset\\train_00\\train_00'

img_files = list()
for root, dirs, files in os.walk(img_folder):
    for name in files:
        file_path = os.path.join(img_folder, name)
        img_files.append(file_path)

# print(img_files[0])
# print(img_files[0].split('\\')[-1])

# img_files = ["D:\\dataset_object_detect\\food-101\\images\\apple_pie\\134.jpg", "D:\\dataset_object_detect\\food-101\\images\\apple_pie\\134.jpg"]

nb = 1
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
with open("result.csv", "a", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file, dialect='excel')


    for img_path in img_files:

        print("\n", img_path)
        option = webdriver.ChromeOptions()
        option.add_argument('log-level=3')
        # option.add_argument('--headless')
        # option.add_argument('--disable-gpu')
        # option.add_argument('--no-sandbox')

        # driver = webdriver.Chrome("C:\Users\VIP\AppData\Local\Google\Chrome\Application\chrome.exe")
        driver = webdriver.Chrome(options=option)

        driver.implicitly_wait(2)
        driver.maximize_window()
        driver.get('https://www.taobao.com')
        time.sleep(1)

        current_address_tb = driver.current_url 

        s = driver.find_element_by_class_name('drop-wrapper')
        s.click()

        # os.system("load_image.exe D:\\dataset_object_detect\\food-101\\images\\apple_pie\\134.jpg" )
        os.system("load_image.exe "+img_path)

        time.sleep(2)

        current_address_s = driver.current_url

        if current_address_tb == current_address_s:
            driver.quit()
            continue
        else:


            def get_html(url):
                r = requests.get(url)
                r.encoding = 'utf-8'
                html = etree.HTML(r.text)
                return r.text

            html_text =  get_html(driver.current_url)

            try:

                raw_title = re.findall(r'\"raw_title\"\:\".*?\"', html_text)
                pic_url = re.findall(r'\"pic_url\"\:\".*?\"', html_text)
                view_price = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html_text)

                print("第{}张图: {} -价格：{}".format(nb, raw_title[0].split(':')[1].strip('"'), view_price[0].split(':')[1].strip('"')))
                # print(nb)
                # print(raw_title[0])
                # print(view_price[0])
                print(pic_url[0])

                

                # result = dict()
                # for k,v in zip(raw_title, view_price):
                #     result.update({k.split(':')[1]: v.split(':')[1]})

                # print(result)

                driver.quit()

                csv_writer.writerow([nb, img_path, raw_title[0].split(':')[1].strip('"'), view_price[0].split(':')[1].strip('"'), pic_url[0].split(':')[1].strip('"')[2:]])
                nb += 1
                os.system("move "+img_path+" "+os.path.join(img_folder, "old"))
            
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

            except IndexError:
                driver.quit()

