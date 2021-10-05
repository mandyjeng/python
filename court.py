#!/usr/bin/env python
# coding: utf-8

# In[69]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from datetime import timedelta, date
import base64
import requests
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('—disable-gpu')
executable_path = './chromedriver'


driver = webdriver.Chrome(executable_path=executable_path,options =chrome_options)
driver.get('https://sports.tms.gov.tw/venues/vselectvenues.php?MVSN=1&VSNA=&Category=2&YM=')
driver.find_element_by_xpath("//*[@id='OrderForm']/div[3]/div/button").click()

email_subject = '紅館沒場地不用看了'
email_content = '沒場'

def remove_duration(str):
    str1 = str.split(' ) ')[1]
    str2 = str1.split(':00 ~ ')[0]
    
    x = int(str2)
        
    if (x<8 or x>17):
        return "N"
    return "Y"
    
def remove_duplicates(duplist):
    return list(set(duplist))
    
# 727-1 728-2 729-3
def format_Num(x):
    x = int(x)
    no = "找不到場地"
       
    if x==727:
        return "第1場地"
    elif  x==728:
        return "第2場地"
    elif  x==729:
        return "第3場地"
    elif  x==730:
        return "第4場地"
    elif  x==731:
        return "第5場地"
    elif  x==732:
        return "第6場地"
    elif  x==733:
        return "第7場地"
    elif  x==734:
        return "第8場地"
    elif  x==735:
        return "第9場地"
    elif  x == 736:
        return "第10場地"
    return no
   
try:
    import datetime
    #處理日期
    now = datetime.datetime.now()  
   
    #找最近的周六    周日
    this_sat = (now + timedelta(days=5 - now.weekday())).strftime("%Y-%m-%d")
    this_sun = (now + timedelta(days=6 - now.weekday())).strftime("%Y-%m-%d")
    nxt_sat = (now + timedelta(days=12 - now.weekday())).strftime("%Y-%m-%d")
    nxt_sun = (now + timedelta(days=13 - now.weekday())).strftime("%Y-%m-%d")
#     this_test = (now + timedelta(days=14 + now.weekday())).strftime("%Y-%m-%d") #10-13 有可以租借的
    print ('周六: {0}'.format(this_sat))
    print ('周日: {0}'.format(this_sun))
    print ('下周六: {0}'.format(nxt_sat))
    print ('下周日: {0}'.format(nxt_sun))
#     print ('測試日期: {0}'.format(this_test))
   
    #可租借日期
    date_list = list()
    date_list.append(this_sat) #周六
    date_list.append(this_sun) #周日
    date_list.append(nxt_sat) #下周日
    date_list.append(nxt_sun) #下周日
#     date_list.append(this_test) #測試日期
   
    print ('要搜尋的日期: {0}'.format(date_list))
   
    # 結果檔
    res_list = list()


   #迴圈找要搜尋的日期
    for s in date_list:
        process_pick_date = '可租借時段 - '+ s
        print('=========process_pick_date: {0}'.format(process_pick_date))
        e1 = driver.find_elements_by_xpath("//td[contains(@title, '{}')]".format(process_pick_date))
       
        for e in e1:
            element_attribute_title = e.get_attribute('title')
            element_attribute_v = e.get_attribute('v')
#             print ('e.get_attribute(\'title\'): {0}'.format(element_attribute_title))
#             print ('e.get_attribute(\'v\'): {0}'.format(element_attribute_v))
            str = format_Num(element_attribute_v.split(":")[0])
#             print('========v: {0}'.format(element_attribute_v.split(":")[0]))
#             print('========format_Num: {0}'.format(format_Num(element_attribute_v.split(":")[0])))
            if str not in '找不到場地':
                if remove_duration(element_attribute_title) is "Y":
                    res_list.append( element_attribute_title  + "=> " + str)
       
    res_list = remove_duplicates(res_list) 
    list(dict.fromkeys(res_list))
    
#     print ('res_list: {0}'.format(res_list))

           
    if(res_list):
        email_content = '\n'.join(res_list)
        email_subject = '紅館有場地快點租'
        #print ('resStr: {0}'.format(email_content))  
       
    #寄信  
    #print (email_content)
    #print (email_subject)
    content = MIMEMultipart() #建立MIMEMultipart物件
    content["subject"] = email_subject #郵件標題
    content["from"] = "mjengcht5@gmail.com" #寄件者
    recipients = ['earldom.jeng@gmail.com,hoshinfu@gmail.com'] #收件者
    content["to"] = ", ".join(recipients)
    content.attach(MIMEText(email_content)) #郵件內容
    with smtplib.SMTP(host="smtp.gmail.com", port="587", timeout=10) as smtp: # 設定SMTP伺服器
        try:
            smtp.ehlo() # 驗證SMTP伺服器
            smtp.starttls() # 建立加密傳輸
            smtp.login("mjengcht5@gmail.com", "rindmbqhykkyxxti") # 登入寄件者gmail
            smtp.send_message(content) # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)
                
except NoSuchElementException as exc:
    #print(exc) # and/or other actions to recover
    driver.close()
    driver.quit()
    time.sleep(10)


# In[ ]:




