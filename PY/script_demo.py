from seleniumwire.webdriver import Chrome

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait

USER_NAME = 'bhzx147'
PASSWORD = 'BHZX223344'

TARGET_PROJECT_ID = 'ZCYJ2024010400019918'
ISAPS_TOKEN = 'AA6ACD356907B8BB77050B6B35FBC1E5'


def main():
    # driver = webdriver.Chrome()
    driver = Chrome()
    wait = WebDriverWait(driver, 10, 0.5)
    driver.get("https://te.pingan.com.cn/#/login?redirect=%2Fpersonal%2Fmod%2Finfo")
    
    
    
    WebDriverWait(driver, 50, 0.5).until(lambda diver:driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/header/div[1]/div/div[2]/a'))
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/header/div[1]/div/div[2]/a').click()
    # time.sleep(5)
    

    wait.until(lambda diver:driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/main/section/div/ul/li[1]/ul/li/span'))
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/main/section/div/ul/li[1]/ul/li/span').click()
    time.sleep(3)

    window_handle = driver.window_handles[-1]
    driver.switch_to.window(window_handle)

    wait.until(lambda diver:driver.find_element(by=By.XPATH, value='//*[@id="sidebarContainerId"]/div[3]/div[1]/div/ul/div[2]/li/ul/div/a/li'))
    driver.find_element(by=By.XPATH, value='//*[@id="sidebarContainerId"]/div[3]/div[1]/div/ul/div[2]/li/ul/div/a/li').click()
    # time.sleep(5)
    wait.until(lambda diver:driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[3]/div/ul/li[3]'))
    project_num = int(driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[3]/div/ul/li[3]').text)
    for _ in range(project_num):
        time.sleep(3)
        projects = driver.find_elements(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[2]/div/div')
        for p_num, project in enumerate(projects):
            if TARGET_PROJECT_ID not in project.text:
                continue
            project.click()
            # time.sleep(5)
            wait.until(lambda diver:driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[2]/div/div[2]/div[2]/table/thead/tr/th[4]/div/div/div/p'))
            driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[2]/div/div[2]/div[2]/table/thead/tr/th[4]/div/div/div/p').click()
            
            time.sleep(3)
            driver.switch_to.active_element.send_keys('LN1J')

            wait.until(lambda diver:driver.find_element(by=By.XPATH, value='/html/body/div[5]/div/div[3]/div/button[1]'))
            driver.find_element(by=By.XPATH, value='/html/body/div[5]/div/div[3]/div/button[1]').click()
            time.sleep(3)

            row_num = len(driver.find_elements(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[2]/div/div[2]/div[3]/table/tbody/tr'))
            
            try:
                page_num = int(driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[3]/div/ul/li[8]').text)
            except:
                page_num = int(driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[3]/div/ul/li[7]').text)
            data = pd.DataFrame(columns=['合同号', '客户名称', '证件号码', '家庭住址', '工作单位', '单位地址', '手机号码'])
            for cur_page in range(page_num):
                time.sleep(2)
                
                max_try = 5
                while max_try:
                    try:
                        wait.until(lambda diver:driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[3]/div/span[2]/div/input'))
                        temp = driver.find_element(by=By.XPATH, value=f'//*[@id="app"]/div/article/section/div/div[3]/div/span[2]/div/input')
                        temp.clear()
                        time.sleep(0.3)
                        temp.send_keys(f'{cur_page+1}')
                        time.sleep(0.3)
                        temp.send_keys(Keys.ENTER)
                        time.sleep(0.4)
                        wait.until(lambda diver:driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[2]/div/div[2]/div[3]/table/tbody/tr[50]/td[4]/div/div'))
                        time.sleep(0.5)
                        break
                    except:
                        driver.refresh()
                        max_try -= 1
                if not cur_page:
                    token = get_token(driver)
                for index in range(row_num):
                    wait.until(lambda diver:driver.find_element(by=By.XPATH, value=f'//*[@id="app"]/div/article/section/div/div[2]/div/div[2]/div[3]/table/tbody/tr[{index+1}]/td[5]/div'))
                    contract_no = driver.find_element(by=By.XPATH, value=f'//*[@id="app"]/div/article/section/div/div[2]/div/div[2]/div[3]/table/tbody/tr[{index+1}]/td[5]/div').text
                    get_info(data, contract_no, token, index, cur_page)
                    time.sleep(1)
                    # do something
                    
                    
                    
                driver.refresh()
            data.to_excel(f'{p_num}.xlsx')
            return
        time.sleep(5)
        driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[3]/div/button[2]/i').click()
    print('结束')



import requests
import json

def get_info(df_data, contract_no, token, index, cur_page):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'bfiles.pingan.com.cn',
        'Origin': 'https://te.pingan.com.cn',
        'Referer': 'https://te.pingan.com.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'isaps-token': token,
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    data = json.dumps({
        "projectId": TARGET_PROJECT_ID,
        "contractNo": contract_no
    })
    url_data = requests.post(url='https://bfiles.pingan.com.cn/brcp/stp/openapi/servgw/servicegateway/personalLoanAssets/customerDetail', headers=headers, data=data)
    response_data = json.loads(url_data.text)
    df_data.at[index + 50 * cur_page, '合同号'] = response_data['data']['customerId']
    df_data.at[index + 50 * cur_page, '客户名称'] = response_data['data']['customerName']
    df_data.at[index + 50 * cur_page, '证件号码'] = response_data['data']['certId']
    df_data.at[index + 50 * cur_page, '家庭住址'] = response_data['data']['familyAdd']
    df_data.at[index + 50 * cur_page, '工作单位'] = response_data['data']['workCorp']
    df_data.at[index + 50 * cur_page, '单位地址'] = response_data['data']['workAdd']
    df_data.at[index + 50 * cur_page, '手机号码'] = response_data['data']['mobiletelePhone']
    print(response_data)


def get_token(driver):
    max_try = 5
    while max_try:
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[2]/div/div[2]/div[3]/table/tbody/tr[1]/td[4]/div/div').click()
            break
        except:
            max_try -= 1
            time.sleep(2)
    time.sleep(2)
    # max_try = 5
    # while max_try:
    #     try:
    #         time.sleep(1.5)
    #         data.at[index + cur_page * row_num, '合同号'] = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/article/section/div/div[1]/div[2]/div[2]/div[2]').text
    #         data.at[index + cur_page * row_num, '客户名称'] = driver.find_element(by=By.XPATH, value='//*[@id="pane-caseBaseInfoCustomer"]/div/div/div/div/table/tr[1]/td[2]').text
    #         data.at[index + cur_page * row_num, '证件号码'] = driver.find_element(by=By.XPATH, value='//*[@id="pane-caseBaseInfoCustomer"]/div/div/div/div/table/tr[2]/td[4]').text
    #         data.at[index + cur_page * row_num, '家庭住址'] = driver.find_element(by=By.XPATH, value='//*[@id="pane-caseBaseInfoCustomer"]/div/div/div/div/table/tr[3]/td[4]').text
    #         data.at[index + cur_page * row_num, '工作单位'] = driver.find_element(by=By.XPATH, value='//*[@id="pane-caseBaseInfoCustomer"]/div/div/div/div/table/tr[4]/td[2]').text
    #         data.at[index + cur_page * row_num, '单位地址'] = driver.find_element(by=By.XPATH, value='//*[@id="pane-caseBaseInfoCustomer"]/div/div/div/div/table/tr[4]/td[4]').text
    #         data.at[index + cur_page * row_num, '手机号码'] = driver.find_element(by=By.XPATH, value='//*[@id="pane-caseBaseInfoCustomer"]/div/div/div/div/table/tr[5]/td[2]').text
    #         break
    #     except:
    #         driver.refresh()
    #         max_try -= 1
    driver.back()
    result, cookie = '', ''
    for request in driver.requests:
        temp = dict(request.headers)
        for key, value in temp.items():
            if key == 'isaps-token' and value:
                result = value
    return result
            
    
if __name__ == '__main__':
    main()
