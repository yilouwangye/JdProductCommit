# !usr/bin/env python
# -*-coding:utf-8 -*-

# @FileName: action.py
# @Author:tian
# @Time:06/07/2020

from appium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from jdmall.config import *

class jdMall():
    def __init__(self):
        '''初始化'''
        self.desired_caps = {
            'platformName':PLANTFORM,
            'deviceName':DEVICE_NAME,
            'appPackage':'com.jingdong.app.mall',
            'appActivity':'.main.MainActivity'
        }
        self.driver = webdriver.Remote(DRIVER_SERVER,self.desired_caps)
        self.wait = WebDriverWait(self.driver,30)

    def search_process(self):
        '''
        搜索商品
        :return:
        '''
        # 同意条款
        agree = self.wait.until(EC.presence_of_element_located((By.ID,'com.jingdong.app.mall:id/a4y')))
        agree.click()
        # 点击开始
        start = self.wait.until(EC.presence_of_element_located((By.ID,'com.jingdong.app.mall:id/bbv')))
        start.click()
        time.sleep(2)
        # 权限获取
        go_on = self.wait.until(EC.presence_of_element_located((By.ID,'com.jingdong.app.mall:id/a4y')))
        go_on.click()
        authorize = self.wait.until(EC.presence_of_element_located((By.ID,'android:id/button1')))
        authorize.click()
        time.sleep(10)
        # 去广告
        ad = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@class="android.widget.Image"]')))
        if ad:
            self.driver.tap([(998,155),],1000)
        else:
            pass
        # 点击搜索跳转
        main_page_button = self.wait.until(EC.presence_of_element_located((By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[3]/android.widget.ViewFlipper/android.widget.LinearLayout/android.widget.TextView')))
        main_page_button.click()
        # 搜索框输入文本
        button = self.wait.until(EC.presence_of_element_located((By.ID,'com.jd.lib.search:id/a3q')))
        button.click()
        button.clear()
        button.set_text(KEYWORD)
        # 点击搜索
        search = self.wait.until(EC.element_to_be_clickable((By.ID,'com.jingdong.app.mall:id/a9b')))
        search.click()
        # 关闭红包弹窗
        borad = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'android.view.View')))
        time.sleep(6)
        if borad:
            self.driver.tap([(538,2030),],1000)
        else:
            pass
        time.sleep(2)
        # 选择商品
        self.wait.until(EC.presence_of_element_located((By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout'))).click()
        time.sleep(2)
        self.driver.swipe(600,1800,600,500)
        self.driver.swipe(600,1600,600,600)
        # 点击评论
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@resource-id="com.jd.lib.productdetail:id/a9e"]'))).click()
        time.sleep(2)

    def flick(self):
        '''
        向上滑动，刷新评论
        :return:
        '''
        try:
            while True:
                self.driver.swipe(START_X, START_Y + DISTANCE, START_X,START_Y)
                time.sleep(SCROLL_TIME)
        except(TimeoutException,NoSuchElementException) as e:
           print(e)

    def main(self):
        self.search_process()
        self.flick()
        self.driver.quit()

if __name__ == '__main__':
    '''此处可设置定时关闭'''
    j = jdMall()
    j.main()


