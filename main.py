import os
import time
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup

os.system("cls")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMEDRIVER_PATH = 'chromedriver_win32\\chromedriver.exe'
USER_FAV_URL = 'https://story.kakao.com/bjpowerll/favorites'
KAKAO_EMAIL = 'bjpowerll@naver.com'
KAKAO_PASSWORD = 'seasoner1@#'

from_url = input("From: ")
to_url = input("To: ")

driver = webdriver.Chrome(f'{BASE_DIR}\\{CHROMEDRIVER_PATH}')

driver.implicitly_wait(3)

# Login.

driver.get(USER_FAV_URL)

login_button = driver.find_element_by_css_selector(
    "#kakaoHead > div.login_btn > a")
login_button.click()

input_email = driver.find_element_by_css_selector("#id_email_2")
input_pw = driver.find_element_by_css_selector("#id_password_3")

input_email.send_keys(KAKAO_EMAIL)
input_pw.send_keys(KAKAO_PASSWORD)

submit_button = driver.find_element_by_css_selector(
    "#login-form > fieldset > div.wrap_btn > button.btn_g.btn_confirm.submit")
submit_button.click()

index = 0
flag = False
image_list = []

while True:
    try:
        index += 1
        story = driver.find_element_by_css_selector(
            f"div._listContainer > div:nth-child({index})")
        link = story.find_element_by_css_selector("a.link_story")

        # 올블 게시글 체크.
        txt = link.find_element_by_css_selector("p.txt_story").text
        if txt == "카카오 운영 정책 위반으로 열람 제한된 게시물입니다.":
            continue

        link.click()
        now_url = driver.current_url

        # now_url이 from_url과 같으면 크롤링 시작.
        if now_url == from_url:
            flag = True
        if flag:
            img_list = driver.find_elements_by_css_selector(
                "div.img_wrap div.img")
            for img in img_list:
                image = img.find_element_by_css_selector("img._mediaImage")
                src = image.get_attribute("src")
                image_list.append(src)

        # now_url이 to_url과 같으면 크롤링 종료.
        if now_url == to_url:
            break
        driver.back()
    except:
        continue

for image in image_list:
    image_type = image.split('/')[7].split('?')[0].split('.')[1]
    image_name = f"img_xl - {image.split('/')[4]}-{image.split('/')[5]}-{image.split('/')[6]}"
    urllib.request.urlretrieve(
        image, f"{BASE_DIR}\\download\\{image_name}.{image_type}")


time.sleep(5)
driver.quit()
