from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from datetime import datetime
from TikTokApi import TikTokApi
from tkinter import messagebox
import subprocess
import sys
import os
import json
import youtubeAPI
import instagramAPI
import time
import pickle

PATH = "chromedriver.exe"
options = webdriver.ChromeOptions()
# options.add_argument(f'user-agent={userAgent}')
options.headless = True
driver = webdriver.Chrome(executable_path=PATH, options=options)
dirPath = ""
tiktokCookiePath = r"tiktokCookie.txt"
instagramCookiePath = r"instagramCookie.txt"

def  test(a):
    print(a)

def Controller(tag,n,path,platform):
    global dirPath
    dirPath = path
    match platform:
        case "Youtube":
            Youtube(tag,n)
        case "Tiktok":
            TikTok(tag,n)
        case "Instagram":
            Instagram(tag,n)
        case "Facebook":
            print("Facebook")

def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)
    print('Cookie loaded')

def TikTok(tag,n):
    driver.maximize_window()
    driver.get(f"https://www.tiktok.com/search/video?q=%23{tag}")
    driver.implicitly_wait(5)
    load_cookie(driver, tiktokCookiePath)
    # ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
    # WebDriverWait(driver, 10,ignored_exceptions=ignored_exceptions)\
    #                     .until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@id='tiktok-verify-ele']")))
    # time.sleep(5)
    # driver.find_element_by_xpath("//a[@id='verify-bar-close']").click()
    time.sleep(2.7923)
    # driver.find_element_by_xpath("//button[@data-e2e='search-button']").click()
    driver.refresh()
    time.sleep(1.2485)
    driver.implicitly_wait(5)
    vId = []
    try:
        for i in range(n):
            id = driver.find_element_by_xpath(f"//div[@id='app']//div[@data-e2e='search_video-item-list']//div[@class='tiktok-1soki6-DivItemContainerForSearch e19c29qe9'][{i+1}]//div[@data-e2e='search_video-item']//a").get_attribute('href')
            print(id)
            vId.append(id.split('/')[5])
            # driver.execute_script("window.scrollBy(0, 5000)")
            if (i+1)%10 == 0:
                driver.find_element_by_xpath("//button[@data-e2e='search-load-more']").click()
            driver.implicitly_wait(1)
    except NoSuchElementException:
        print("NoSuchElementException")
    
    print(vId)
    result = getTikTokAPI(tag, vId)
    writeToFile(result, vId, "T")
    messagebox.showinfo(title="Data Extract Complete", message="Successfully extract data from Tiktok")
    print("COMPLETE TIKTOK")

def getTikTokAPI(tag, vId):
    subprocess.run(["python", "-m", "playwright", "install"])
    print("Playwright Installed")
    api = TikTokApi()
    data = []
    for id in vId:
        try:
            vidInfo = api.video(id=f'{id}').info()
            vidInfoData = json.dumps(vidInfo).replace("\'","\"")
            data.append(parseData(tag,json.loads(vidInfoData)))
        except:
            continue
    print(data)
    return data

def parseData(tag,data):
    try:
        vId = data['video']['id']
        author = data['author']['nickname']
        commentCount = data['stats']['commentCount']
        likeCount = data['stats']['diggCount']
        viewCount = data['stats']['playCount']
        shareCount = data['stats']['shareCount']
        return [vId,author,viewCount,likeCount,commentCount,shareCount,tag]
    except KeyError:
        print("KeyError Tiktok")

    
def Youtube(tag,n):
    cleanFileData("Youtube")
    driver.get(f"https://www.youtube.com/results?search_query=%23{tag}&sp=CAMSAhABQgUSA2cyMA%253D%253D")
    links = []
    vidTag = []

    if n%20 == 0:
        nCount = n//20
    else:
        nCount = (n//20)+1

    try:
        for i in range(nCount):
            for j in range(20):
                link = driver.find_element_by_xpath(f"//div[@id='primary']//ytd-item-section-renderer[{i+1}]//ytd-video-renderer[{j+1}]//div[@id='dismissible']//a[@id='video-title']").get_attribute('href')
                print(link)
                if "shorts" in link:
                    links.append(link.split('/')[4])
                    vidTag.append("S")
                else:
                    links.append(link.split('=')[1])
                    vidTag.append("V")
            driver.execute_script("window.scrollBy(0, 10000)")
            time.sleep(3)
        getLikesYoutubeAPI(tag, breakList(links), vidTag)
    except NoSuchElementException as e:
        print("NoSuchElementExecption", str(e))
        getLikesYoutubeAPI(tag, breakList(links), vidTag)
        
    print(links)

def breakList(my_list):
    n=50
    final = [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n )]
    return final

def cleanFileData(platform):
    clean1 = open(f"{dirPath}\{platform}_Get_Data_Result"+".txt","w", encoding='utf-8')
    clean2 = open(f"{dirPath}\{platform}_VideoID.txt","w",encoding='utf-8')

def getLikesYoutubeAPI(tag, videoID, vidTag):
    # resp = json.load(youtubeAPI.main(videoID))
    vidTagIndex = 0
    for i in range(len(videoID)):
        resp = youtubeAPI.main(videoID[i])
        data = []
        items = resp['items']
        dt = datetime.now().strftime("%Y%m%d")
        # rawData = open("Raw_Data_"+dt+"_"+str(i)+".txt","w+", encoding='utf-8')
        # rawData.writelines(str(items))
        for item in items:
            try:
                vid = item['id']
                channel = item['snippet']['channelTitle']
                title = item['snippet']['title']
                viewCount = item['statistics']['viewCount']
                if "likeCount" in item['statistics']:
                    likeCount = item['statistics']['likeCount']
                else:
                    likeCount = 0
                commentCount = item['statistics']['commentCount']
                data.append([vid,title,viewCount,likeCount,commentCount,tag,channel,vidTag[vidTagIndex]])
                vidTagIndex += 1
            except KeyError as e:
                print("KeyError", str(e))
                continue
        # print(data)
        writeToFile(data,videoID[i],"Y")
    messagebox.showinfo(title="Data Extract Complete", message="Successfully extract data from Youtube")
    print("COMPLETE YOUTUBE")

def writeToFile(data,videoID,platform):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    if platform == "Y":
        result = open(f"{dirPath}\Youtube_Get_Data_Result.txt","w+", encoding='utf-8')
        for val in data:
            result.writelines(f"{val[0]};;{val[1]};;{val[2]};;{val[3]};;{val[4]};;{val[5]};;{val[6]};;{val[7]};;\n")
        saveVideoID = open(f"{dirPath}\Youtube_VideoID.txt","w+",encoding='utf-8')
        for val in videoID:
            saveVideoID.writelines(f"{val};")
        print("Written Youtube Data")
    elif platform == "T":
        result = open(f"{dirPath}\Tiktok_Get_Data_Result.txt","w+", encoding='utf-8')
        for val in data:
            result.writelines(f"{val[0]};;{val[1]};;{val[2]};;{val[3]};;{val[4]};;{val[5]};;{val[6]};;\n")
        saveVideoID = open(f"{dirPath}\Tiktok_VideoID.txt","w+",encoding='utf-8')
        for val in videoID:
            saveVideoID.writelines(f"{val};")
        print("Written Tiktok Data")
    elif platform == "I":
        result = open(f"{dirPath}\Instagram_Get_Data_Result.txt","w+", encoding='utf-8')
        for val in data:
            result.writelines(f"{val[0]};;{val[1]};;{val[2]};;{val[3]};;{val[4]};;{val[5]};;{val[6]};;\n")
        saveVideoID = open(f"{dirPath}\Instagram_VideoID.txt","w+",encoding='utf-8')
        for val in videoID:
            saveVideoID.writelines(f"{val};")
        print("Written Instagram Data")

def Instagram(tag, n):
    cleanFileData("Instagram")
    driver.maximize_window()
    driver.get(f"https://www.instagram.com/explore/tags/{tag}/")
    driver.implicitly_wait(5)
    load_cookie(driver, instagramCookiePath)
    time.sleep(2.7923)
    driver.refresh()
    time.sleep(1.2485)
    driver.implicitly_wait(5)
    igID = []
    # Top Post
    try:
        for i in range(3):
            for j in range(3):
                id = driver.find_element_by_xpath(f"//article//div[@class='_aaq8']//div[@class='_ac7v _aang'][{i+1}]//div[@class='_aabd _aa8k _aanf'][{j+1}]//a").get_attribute('href')
                print(id)
                igID.append(id.split("/")[4])
        for i in range(n):
            for j in range(3):
                id = driver.find_element_by_xpath(f"//article//div[2]//div[@class='_ac7v _aang'][{i+1}]//div[@class='_aabd _aa8k _aanf'][{j+1}]//a").get_attribute('href')
                print(id)
                igID.append(id.split("/")[4])
    except NoSuchElementException:
        print("NoSuchElementException")
    
    print(igID)
    result = instagramAPI.getInstagramAPI(tag,igID)
    writeToFile(result, igID, "I")
    messagebox.showinfo(title="Data Extract Complete", message="Successfully extract data from Instagram")
    print("COMPLETE INSTAGRAM")
    
# Youtube("indonesia",100,"D:/ADR/Personal/ADR/Self-Project/Test/get-data-selenium-build/data")
# TikTok("g20", 2)

# Instagram("tag", 2)
