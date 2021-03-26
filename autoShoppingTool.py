# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import chromedriver_binary
import Tkinter as tk
import tkMessageBox as messagebox
import os
import datetime
import time 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"   # Do not wait for full page load



class App(tk.Frame):
    def __init__(self,master=None,**kw):
        #Create a blank dictionary
        self.answers = {}
        tk.Frame.__init__(self,master=master,**kw)

        root.title('楽天自動購入ツール')
        root.geometry('500x150+350+300')

        tk.Label(self,text="URL").grid(row=0,column=0)
        self.URL = tk.Entry(self,width=40)
        self.URL.grid(row=0,column=1)

        tk.Label(self,text="ID").grid(row=1,column=0)
        self.ID = tk.Entry(self,width=40)
        self.ID.grid(row=1,column=1)

        tk.Label(self,text="Password").grid(row=2,column=0)
        self.Password = tk.Entry(self,show='*',width=40)
        self.Password.grid(row=2,column=1)

        tk.Label(self,text="Activatetime").grid(row=3,column=0)
        self.Activatetime = tk.Entry(self,width=40)
        self.Activatetime.insert(tk.END, u'半角数字で何分後に実施するか入力してください')
        self.Activatetime.grid(row=3,column=1)
        
        tk.Button(self,text="購入",command=self.collectAnswers).grid(row=4,column=1)    
    
    def collectAnswers(self):
        self.answers['URL'] = self.URL.get()    
        self.answers['ID'] = self.ID.get()
        self.answers['Password'] = self.Password.get()
        self.answers['Activatetime'] = int(self.Activatetime.get())
        buyer(self.answers)

def buyer (answers):

    URL = answers['URL']
    ID = answers['ID']
    Password = answers['Password']
    Activatetime = answers['Activatetime']
    Activatetime *= 60

    driver = webdriver.Chrome()
    driver.get(URL)

    wait = WebDriverWait(driver, 30)
    time.sleep(Activatetime)   #入力された分数経過後起動

    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"cart-button-container")))
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"cart-button-container")))

    time.sleep(2)


    driver.find_element_by_class_name('cart-button-container').click()
    driver.find_element_by_class_name('cart-button-container').click()


    time.sleep(2)
 
    wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="myForm"]/div[2]/div[2]/ul/li[1]/a/span[1]')))

    driver.find_element_by_xpath('//*[@id="myForm"]/div[2]/div[2]/ul/li[1]/a/span[1]').click()

    wait.until(EC.presence_of_element_located((By.XPATH,"//input[@value='ご購入手続き']")))


    driver.find_element_by_xpath("//input[@value='ご購入手続き']").click()


    # user info
    name = ID
    passwd = Password

    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"user-id")))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"password")))

    # input user info
    driver.find_element_by_class_name('user-id').send_keys(name)
    driver.find_element_by_class_name('password').send_keys(passwd)
    # login

    wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="login_submit"]')))


    driver.find_element_by_xpath('//*[@id="login_submit"]').click()
    time.sleep(1)
    driver.get('https://basket.step.rakuten.co.jp/rms/mall/bs/mdlvpay/?l2-id=step2_pc_next')
    
    wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="payment_head_331423"]/div[3]/label/input')))
    driver.find_element_by_xpath('//*[@id="payment_head_331423"]/div[3]/label/input').click()
    driver.find_element_by_xpath('//*[@id="dlv_day_type_none_331423"]').click()
    driver.find_element_by_xpath('//*[@id="dlvPaySubmit"]').click()

    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="commit-float"]/div/input').click()



    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="commit-float"]/div/input')))
    #driver.find_element_by_xpath('//*[@id="commit-float"]/div/input').click() #購入実施ボタン押下
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    ret = messagebox.askyesno('確認', '購入完了しました。ウィンドウを閉じますか？')
    if ret == True:
        driver.close()
        root.destroy()

root = tk.Tk()
App(root).grid()
root.mainloop()


# <div id="submit-button" class="big-red-button t-a-c m-b-0 ratTrackingEvent" data-url-parameter-key="l2-id" data-url-parameter-val="step2_pc_next">
                      #  次へ
                    #</div>

#//*[@id="submit-button"]


#購入決定ボタンのXpath //*[@id="commit-float"]/div/input

# driver.find_element_by_partial_link_text("次へ").click()
#driver.get('https://google.com')
# os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')


#<input class="payment-radio" data-supported-dlv-date-time="day,time,my" data-categoryid="15" name="select_payment_map(331423)" type="radio" value="21" data-shopid="331423" data-payment-name="後払い決済" data-payment-iscredit="false" data-payment-iscod="false" data-payment-ispayafterdelivery="true" data-is-display-detail-message="false">

#payment_head_331423 > div:nth-child(4) > label > input

#//*[@id="payment_head_331423"]/div[3]/label/input
