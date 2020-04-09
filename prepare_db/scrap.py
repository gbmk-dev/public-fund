from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
import os
import os.path
import shutil
import xlrd
import platform
from openpyxl.workbook import Workbook
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


download_path = '/Users/giubinkang/Downloads'
now = datetime.now()
date = now.strftime("%Y%m%d")
file1 = '펀드매니저 상세정보_운용펀드(기준일)_' + date + '.xls'
file2 = '펀드매니저 상세정보_운용펀드(과거3년)_' + date + '.xls'
file_info = [file1, file2]


def get_driver_path():
    which_os = platform.system()
    if which_os == 'Linux':
        return '/usr/local/bin/chromedriver'
    elif which_os == 'Windows':
        return os.path.join(os.getcwd(), 'chromedriver.exe')
    else:
        return os.path.join(os.getcwd(), 'chromedriver')


def dealing_alert(browser):
    try:
        WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
        alert = browser.switch_to.alert
        alert.accept()
        print("alert accepted")
    except TimeoutException:
        print("no alert")


def move_files(dir_path, file_prefix, filename):
    download_filepath = os.path.join(download_path, filename)
    moved_filepath = os.path.join(dir_path, file_prefix + filename)
    if os.path.exists(download_filepath):
        shutil.move(download_filepath, moved_filepath)
        print(filename + " moved to " + dir_path)
        return True
    else:
        print(filename + " does not exist.")
        return False


def convert_xls_to_xlsx(filename):
    # first open using xlrd
    book = xlrd.open_workbook(filename)
    xlsx_filename = filename[:filename.rfind('.')]
    index = 0
    nrows, ncols = 0, 0
    while nrows * ncols == 0:
        sheet = book.sheet_by_index(index)
        nrows = sheet.nrows
        ncols = sheet.ncols
        index += 1

    # prepare a xlsx sheet
    book1 = Workbook()
    sheet1 = book1.active

    for row in range(0, nrows):
        for col in range(0, ncols):
            sheet1.cell(row=row + 1, column=col + 1).value = sheet.cell_value(row, col)

    book1.save(filename='{}.xlsx'.format(xlsx_filename))
    return book1


def download_excel(driver, els):
    i = 0
    cnt = 0
    for el in els:
        # 10명의 정보만를 다운로드하고 함수를 종료한다.
        if cnt >= 10:
            return

        # 사람 당 짝수 번째 돋보기만 클릭한다.
        if (i % 2 == 0):
            # 다운로드한 사람 수에 1을 추가한다.
            cnt += 1
            # 짝수 번째 돋보기를 클릭한다.
            el.click()
            # 팝업 창이 나타날 때까지 기다린다.
            time.sleep(5)
            # 팝업을 검색한다.
            popup = driver.find_element_by_tag_name('iframe')
            # 기본 브라우저를 팝업으로 전환한다. (다운로드하기 위해서 반드시 필요)
            driver.switch_to.frame(popup)

            # 펀드매니저 정보가 뜰 때까지 기다린다.
            time.sleep(5)
            # 펀드매니저의 이름, 펀드매니저의 회사명을 수집한다.
            name = driver.find_element_by_id('fundMgr').text
            comp = driver.find_element_by_id('compNm').text

            # 기준일 파일을 다운로드한다.
            driver.find_element_by_id('image111').click()
            # 데이터가 없다는 alert가 뜰 경우를 대비한다.
            dealing_alert(driver)
            # 다운로드가 완료될 때까지 기다린다.
            time.sleep(10)

            # 과거3년 파일을 위한 탭 버튼을 찾는다.
            li = driver.find_element_by_id('tabControl1_tab_dtlTtabs2')
            btn = li.find_element_by_tag_name('a')
            # 과거3년 파일을 위한 탭 버튼을 클릭한다.
            btn.click()
            # 정보가 뜰 때까지 기다린다.
            time.sleep(5)

            # 과거3년 파일을 다운로드한다.
            driver.find_element_by_id('image115').click()
            # 데이터가 없다는 alert가 뜰 경우를 대비한다.
            dealing_alert(driver)
            # 다운로드가 완료될 때까지 기다린다.
            time.sleep(10)

            # 다운로드가 완료된 파일들은 이름을 바꾼다.
            # 우선 scrap.py 파일이 위치한 경로를 획득한다.
            dir_path = os.getcwd()
            # 다음으로 다운로드할 파일명의 prefix를 만든다.
            file_prefix = comp + '_' + name + '_'

            for file in file_info:
                # 다운로드가 완료된 파일들의 이름을 바꾸고 위치를 옮긴다.
                # 다운로드가 실패한 경우 xls->xlsx 과정을 거치지 않는다.
                if not move_files(dir_path, file_prefix, file):
                    continue
                moved_filepath = os.path.join(dir_path, file_prefix + file)
                # xls 파일을 xlsx로 바꾼다.
                convert_xls_to_xlsx(moved_filepath)

            # 팝업을 벗어나 기본 브라우저로 돌아간다.
            driver.switch_to.default_content()
            # 팝업 닫기 버튼을 찾는다.
            close_btn = driver.find_element_by_id('textbox1987456321')
            # 팝업을 닫는다.
            close_btn.click()

        i += 1

# 크롬드라이버 경로 획득
driver_path = get_driver_path()
# 크롬드라이버 설정
driver = webdriver.Chrome(driver_path)

# 접속할 url
url = 'http://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/fundMgr/DISFundMgrSrch.xml&divisionId=MDIS03001002000000&serviceId=SDIS03001002000'
# 접속
driver.get(url)

# '검색' 버튼이 클릭 가능할 때까지 기다린다, 최대 300초
WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.ID, 'btnSearImg')))
# '검색' 버튼을 찾고 클릭한다.
driver.find_element_by_id('btnSearImg').click()

# 검색 결과가 조회될 때까지 기다린다, 최대 300초
WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.CLASS_NAME, 'w2grid_image')))
# 검색 결과를 찾아서 els에 저장한다
els = driver.find_elements_by_class_name('w2grid_image')

try:
    # 10개 씩 70번 다운로드한다.
    for down in range(70):
        # 1. els에 담긴 10개의 파일을 다운로드한다.
        download_excel(driver, els)

        # 2. 기본 브라우저로 되돌아온다.
        driver.switch_to.default_content()

        # 3. 다음 10개 로드를 위해 우선 첫 번째 요소를 클릭한다.
        nth = driver.find_elements_by_class_name('gridBodyDefault')[1]
        nth.click()

        # 4. 아래 방향키를 클릭하여 그 다음 10개를 로드한다.
        nth.send_keys(Keys.PAGE_DOWN)

        # 5. 그 다음 10개를 els에 저장한다.
        els = driver.find_elements_by_class_name('w2grid_image')
finally:
    driver.quit()