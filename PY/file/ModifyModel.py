# %%
from collections import defaultdict
from datetime import datetime
import pandas as pd
import re

#%% 期数、期限
def num_periods(num):
    # 查找字符串的中文
    pattern = re.compile("[\u4e00-\u9fa5]+")
    if '年' in str(num):
        result = re.sub(pattern,"",num)
        result = pd.to_numeric(result)
        result = result * 12
    else:
        try:
            result = re.sub(pattern,"",num)
        except:
            pass
        if str(num) != '':
            result = float(num)
            if result/30 >4 :
                result = result/30
    return result

#%% 日期
def date_p(date):
    try:
        result = pd.to_datetime(date)
    except:
        try:
            result = datetime.strptime(date,'%Y/%m/%d')
        except:
            try:
                date = (re.sub(r'(年|月)','/',date)).replace('日','')
                result = datetime.strptime(date,'%Y/%m/%d')
            except:
                result = '1900/1/1'
    return result



# %% 手机号校验
# def tel_type(tel):

# %% 身份证校验
def is_valid_id(id_number):  
    # 长度验证  
    if len(id_number) != 15 and len(id_number) != 18:  
        return False  
  
    # 格式验证  
    if not re.match(r'^\d{15}|\d{17}[\dXx]$', id_number):  
        return False  
  
    # 出生日期验证  
    if len(id_number) == 18:  
        birth_date = id_number[6:14]  
    else:  
        birth_date = id_number[6:12]  
    try:  
        datetime.strptime(birth_date, '%Y%m%d')  
    except ValueError:  
        return False  
  
    # 校验码验证（仅对18位身份证）  
    if len(id_number) == 18:  
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']  
        sum_ = 0  
        for i in range(17):  
            sum_ += int(id_number[i]) * weights[i]  
        if check_codes[sum_ % 11] != id_number[-1].upper():  
            return False  
  
    return True
