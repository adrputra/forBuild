from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from datetime import datetime
from TikTokApi import TikTokApi
from tkinter import messagebox
import handlerAPI
import subprocess
import time
import pickle

# Config
PATH = "chromedriver.exe"
options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome(executable_path=PATH, options=options)
dirPath = ""
tiktokCookiePath = r"tiktokCookie.txt"
instagramCookiePath = r"instagramCookie.txt"
facebookCookiePath = r"facebookCookie.txt"

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
        case "InstagramV2":
            InstagramV2(tag,n)
        case "Facebook":
            FacebookV2(tag,n)

def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)
    print('Cookie loaded')

def cleanFileData(platform):
    clean1 = open(f"{dirPath}\{platform}_Get_Data_Result"+".txt","w", encoding='utf-8')
    clean2 = open(f"{dirPath}\{platform}_VideoID.txt","w",encoding='utf-8')

def writeToFile(data,videoID,platform):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    if platform == "Y":
        result = open(f"{dirPath}\Youtube_Get_Data_Result.txt","a+", encoding='utf-8')
        for val in data:
            result.writelines(f"{val[0]};;{val[1]};;{val[2]};;{val[3]};;{val[4]};;{val[5]};;{val[6]};;{val[7]};;\n")
        saveVideoID = open(f"{dirPath}\Youtube_VideoID.txt","a+",encoding='utf-8')
        for val in videoID:
            saveVideoID.writelines(f"{val};")
        print("Written Youtube Data")
    elif platform == "T":
        result = open(f"{dirPath}\Tiktok_Get_Data_Result.txt","a+", encoding='utf-8')
        for val in data:
            result.writelines(f"{val[0]};;{val[1]};;{val[2]};;{val[3]};;{val[4]};;{val[5]};;{val[6]};;\n")
        saveVideoID = open(f"{dirPath}\Tiktok_VideoID.txt","a+",encoding='utf-8')
        for val in videoID:
            saveVideoID.writelines(f"{val};")
        print("Written Tiktok Data")
    elif platform == "I":
        result = open(f"{dirPath}\Instagram_Get_Data_Result.txt","a+", encoding='utf-8')
        for val in data:
            result.writelines(f"{val[0]};;{val[1]};;{val[2]};;{val[3]};;{val[4]};;{val[5]};;{val[6]};;\n")
        saveVideoID = open(f"{dirPath}\Instagram_VideoID.txt","a+",encoding='utf-8')
        for val in videoID:
            saveVideoID.writelines(f"{val};")
        print("Written Instagram Data")
    elif platform == "F":
        result = open(f"{dirPath}\Facebook_Get_Data_Result.txt","a+", encoding='utf-8')
        for val in data:
            result.writelines(f"{val[0]};;{val[1]};;{val[2]};;{val[3]};;{val[4]};;{val[5]};;\n")
        saveVideoID = open(f"{dirPath}\Facebook_VideoID.txt","a+",encoding='utf-8')
        for val in videoID:
            saveVideoID.writelines(f"{val};")
        print("Written Facebook Data")

def Youtube(tag,n):

    def breakList(my_list):
        n=50
        final = [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n )]
        return final

    def getLikesYoutubeAPI(tag, videoID, vidTag):
        vidTagIndex = 0
        for i in range(len(videoID)):
            resp = handlerAPI.YoutubeAPI(videoID[i])
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

    cleanFileData("Youtube")
    driver.get(f"https://www.youtube.com/results?search_query=%23{tag}&sp=EgIIBUINEgtmYWJuMmphdGVuZw%253D%253D")
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
                time.sleep(0.748)
                # <yt-formatted-string id="message" class="style-scope ytd-message-renderer">No more results</yt-formatted-string>
        getLikesYoutubeAPI(tag, breakList(links), vidTag)
    except NoSuchElementException as e:
        print("NoSuchElementExecption", str(e))
        getLikesYoutubeAPI(tag, breakList(links), vidTag)
        
    print(links)
    driver.close()


def TikTok(tag,n):

    def getTikTokAPI(tag, vId):
        subprocess.run(["python", "-m", "playwright", "install"])
        print("Playwright Installed")
        api = TikTokApi()
        data = []
        for id in vId:
            try:
                vidInfo = api.video(id=f'{id}').info()
                # vidInfoData = json.dumps(vidInfo).replace("'",'"')
                # data.append(parseData(tag,json.loads(vidInfoData)))
                data.append(parseData(tag,vidInfo))
                time.sleep(0.431)
            except Exception as e:
                print(str(e))
                continue
        print(data)
        return data

    def parseData(tag,data):
        try:
            vId = data['video']['id']
            author = data['author']['uniqueId']
            commentCount = data['stats']['commentCount']
            likeCount = data['stats']['diggCount']
            viewCount = data['stats']['playCount']
            shareCount = data['stats']['shareCount']
            return [vId,author,viewCount,likeCount,commentCount,shareCount,tag]
        except KeyError:
            print("KeyError Tiktok")
    
    cleanFileData("Tiktok")
    driver.maximize_window()
    driver.get(f"https://www.tiktok.com/search/video?q=%23{tag}")
    # driver.implicitly_wait(5)
    load_cookie(driver, tiktokCookiePath)
    time.sleep(2.7923)
    driver.refresh()
    time.sleep(3.2485)
    driver.implicitly_wait(5)
    vId = []
    try:
        for i in range(n):
            id = driver.find_element_by_xpath(f"//div[@id='app']//div[@data-e2e='search_video-item-list']//div[@class='tiktok-1soki6-DivItemContainerForSearch e19c29qe9'][{i+1}]//div[@data-e2e='search_video-item']//a").get_attribute('href')
            print(id)
            vId.append(id.split('/')[5])
            if (i+1)%10 == 0:
                ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
                WebDriverWait(driver, 60,ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@data-e2e='search-load-more']")))
                driver.find_element_by_xpath("//button[@data-e2e='search-load-more']").click()
                time.sleep(1.234)
            driver.implicitly_wait(1)
        print("Please wait..! Getting Data ..")
        result = getTikTokAPI(tag, vId)
    except NoSuchElementException as e:
        print("NoSuchElementException", str(e))
        print("Please wait..! Getting Data ..")
        result = getTikTokAPI(tag, vId)
    
    print(vId)
    writeToFile(result, vId, "T")
    messagebox.showinfo(title="Data Extract Complete", message="Successfully extract data from Tiktok")
    print("COMPLETE TIKTOK")
    driver.close()

def Instagram(tag, n):
    cleanFileData("Instagram")
    driver.maximize_window()
    driver.get(f"https://www.instagram.com/explore/tags/{tag}/")
    # driver.implicitly_wait(5)
    load_cookie(driver, instagramCookiePath)
    time.sleep(2.7923)
    driver.refresh()
    time.sleep(1.2485)
    driver.implicitly_wait(5)
    igID = []
    # Top Post
    try:
        try:
            for i in range(4):
                for j in range(3):
                    id = driver.find_element_by_xpath(f"//article//div[@class='_aaq8']//div[@class='_ac7v _aang'][{i+1}]//div[@class='_aabd _aa8k _aanf'][{j+1}]//a").get_attribute('href')
                    print(id)
                    igID.append(id.split("/")[4])
        except NoSuchElementException as e:
            print(str(e))

        for i in range(n//3):
            for j in range(3):
                id = driver.find_element_by_xpath(f"//article//div[2]//div[@class='_ac7v _aang'][{i+1}]//div[@class='_aabd _aa8k _aanf'][{j+1}]//a").get_attribute('href')
                print(id)
                igID.append(id.split("/")[4])
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(3)
        result = handlerAPI.getInstagramAPI(tag,igID)
    except NoSuchElementException:
        print("NoSuchElementException")
        result = handlerAPI.getInstagramAPI(tag,igID)
    
    print(igID)
    writeToFile(result, igID, "I")
    messagebox.showinfo(title="Data Extract Complete", message="Successfully extract data from Instagram")
    print("COMPLETE INSTAGRAM")
    driver.close()

def InstagramV2(tag,n):
    cleanFileData("Instagram")
    igID = handlerAPI.getDataSheetInstagram()
    result = handlerAPI.getInstagramAPIv2(tag, igID)
    print(igID)
    writeToFile(result, igID, "I")
    messagebox.showinfo(title="Data Extract Complete", message="Successfully extract data from Instagram")
    print("COMPLETE INSTAGRAM")
    
def Facebook(tag, n):

    def getName(i):
        try:
            print("Name",end=" ")
            xpath = f"//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']//div[{i+1}]//div[@class='x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z']//div[@class='x1iyjqo2']//span[@dir='ltr'][1]//span[@class='xt0psk2']//span"
            name = driver.find_element_by_xpath(xpath).text
            print(name)
            return name
        except NoSuchElementException as e:
            print("Name", str(e))
            return False
            # return ""
    
    def getName2(i):
        try:
            print("Name2",end=" ")
            xpath = f"//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']//div[{i+1}]//div[@class='x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z']//div[@class='x1iyjqo2']//span[@class='xt0psk2']//strong//span"
            name2 = driver.find_element_by_xpath(xpath).text
            print(name2)
            return name2
        except NoSuchElementException as e:
            print("Name2", str(e))
            # return ""

    def getLike(i):
        try:
            print("Like",end=" ")
            xpath = f"//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']//div[{i+1}]//div[@class='x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z']//span[@class='x16hj40l']"
            like = driver.find_element_by_xpath(xpath).text
            print(like)
            return like
        except NoSuchElementException as e:
            print("Like", str(e))
            return ""
    
    def getComment(i):
        try:
            print("Comment",end=" ")
            xpath = f"//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']//div[{i+1}]//div[@class='x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z']//div[@class='xnfveip'][2]//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa']"
            comment = driver.find_element_by_xpath(xpath).text
            print(comment)
            return comment
        except NoSuchElementException as e:
            print("Comment", str(e))
            return ""

    def getShare(i):
        try:
            print("Share",end=" ")
            xpath = f"//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']//div[{i+1}]//div[@class='x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z']//div[@class='xnfveip'][3]//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa']"
            share = driver.find_element_by_xpath(xpath).text
            print(share)
            return share
        except NoSuchElementException as e:
            print("Share", str(e))
            return ""
    
    def getPostLink(i):
        try:
            postLink = driver.find_element_by_xpath(f"//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']//div[{i+1}]//div[@class='x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z']//div[@class='x1iyjqo2']//div[@class='xu06os2 x1ok221b'][2]//a").get_attribute('href')
            print(postLink)
            return postLink
        except NoSuchElementException as e:
            print("PostLink", str(e))
            # return ""
    
    def parseLike(like):
        fLike = like.split(" ")
        if len(fLike) == 1:
            return like
        elif fLike[1] == "rb":
            return fLike[0] + "000"
        elif "," in fLike[0] and fLike[1] == "rb":
            return fLike[0].split(',')[0] + fLike[0].split(',')[1] + "00"
        else:
            return like
    
    def parseComment(comment):
        fComment = comment.split(" ")
        if len(fComment) == 2:
            return fComment[0]
        elif len(fComment) == 3:
            if "," in fComment[0]:
                return fComment[0].split(',')[0] + fComment[0].split(',')[1] + "00"
            else:
                return fComment[0] + "000"
        else:
            return comment

    def parseShare(share):
        fShare = share.split(" ")
        if len(fShare) == 3:
            return fShare[0]
        elif len(fShare) == 4:
            if "," in fShare[0]:
                return fShare[0].split(',')[0] + fShare[0].split(',')[1] + "00"
            else:
                return fShare[0] + "000"
        else:
            return share
        
    cleanFileData("Facebook")
    driver.maximize_window()
    driver.get(f"https://www.facebook.com/hashtag/{tag}")
    driver.implicitly_wait(5)
    load_cookie(driver, facebookCookiePath)
    time.sleep(2.7923)
    driver.refresh()
    time.sleep(2.535)

    data = []
    links = []

    for i in range(n):
        print('loop ke ',i)
        if (getName(i) == False):
            name = getName2(i)
        else:
            name = getName(i)
        like = getLike(i)
        comment = getComment(i)
        share = getShare(i)
        postLink = getPostLink(i)

        links.append(postLink.split('/?')[0])
        data.append([postLink.split('/?')[0], name, parseLike(like), parseComment(comment), parseShare(share), tag])
        if i==7 or i%10 == 0:
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(3.432)
        print(name,like,comment,share,tag)

    print(data)
    writeToFile(data, links, "F")
    messagebox.showinfo(title="Data Extract Complete", message="Successfully extract data from Facebook")
    print("COMPLETE FACEBOOK")

def FacebookV2(tag,n):

    def parseLike(like):
        fLike = like.split(" ")
        if len(fLike) == 1:
            return like
        elif "," in fLike[0] and fLike[1] == "rb":
            return fLike[0].split(',')[0] + fLike[0].split(',')[1] + "00"
        elif fLike[1] == "rb":
            return fLike[0] + "000"
        else:
            return like
    
    def parseComment(comment):
        fComment = comment.split(" ")
        if len(fComment) == 2:
            return fComment[0]
        elif len(fComment) == 3:
            if "," in fComment[0]:
                return fComment[0].split(',')[0] + fComment[0].split(',')[1] + "00"
            else:
                return fComment[0] + "000"
        else:
            return comment

    def autoGetData(postLink,namePath,likePath,commentPath,sharePath,tag):
        postLink = ""
        name = ""
        like = ""
        comment = ""
        share = ""

        if check(namePath):
            name = driver.find_element_by_xpath(namePath).text

        if check(likePath):
            like = driver.find_element_by_xpath(likePath).text

        if check(commentPath):
            comment = driver.find_element_by_xpath(commentPath).text

        if check(sharePath):
            share = driver.find_element_by_xpath(sharePath).text
        
        return [item,name,parseLike(like),parseComment(comment),share,tag]

    cleanFileData("Facebook")
    driver.maximize_window()
    driver.get(f"https://www.facebook.com/hashtag/{tag}")
    load_cookie(driver, facebookCookiePath)
    time.sleep(2.7923)
    load_cookie(driver, facebookCookiePath)
    time.sleep(2.7923)
    driver.refresh()
    time.sleep(3.2485)
    result = []
    postLink = handlerAPI.getDataSheetFacebook()
    for item in postLink:
        driver.get(item)
        if "/reel/" in item:
            namePath = "//div[@class='x1n2onr6 x1ja2u2z x9f619 x78zum5 xdt5ytf x2lah0s x193iq5w']//a"
            likePath = "//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w x1xmf6yo x1e56ztr xzboxd6 x14l7nz5'][2]//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w x6s0dn4 x1gslohp x12nagc xzboxd6 x14l7nz5'][2]//span[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84']"
            commentPath = "//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w x1xmf6yo x1e56ztr xzboxd6 x14l7nz5'][3]//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w x6s0dn4 x1gslohp x12nagc xzboxd6 x14l7nz5'][2]//span[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84']"
            sharePath = "//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w x1xmf6yo x1e56ztr xzboxd6 x14l7nz5'][4]//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w x6s0dn4 x1gslohp x12nagc xzboxd6 x14l7nz5'][2]//span[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84']"
        
            result.append(autoGetData(item,namePath,likePath,commentPath,sharePath,tag))
                
        elif "/posts/" in item:
            namePath = "//div[@class='x1swvt13 x1pi30zi xyamay9']//span//h2//strong//span"
            likePath = "//div[@class='x78zum5 xdt5ytf x1huibft x1n6yrxt']//div[@class='x6s0dn4 xi81zsa x78zum5 x1a02dak x13a6bvl xyesn5m x6ikm8r x10wlt62']//div[@class='x6s0dn4 x78zum5 x1iyjqo2 x13a6bvl x6ikm8r x10wlt62']//div[@role='button']//span[@class='x4k7w5x x1h91t0o x1h9r5lt xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j x1jfb8zj']"
            commentPath = "//div[@class='x78zum5 xdt5ytf x1huibft x1n6yrxt']//div[@class='x6s0dn4 xi81zsa x78zum5 x1a02dak x13a6bvl xyesn5m x6ikm8r x10wlt62']//div[@class='x6s0dn4 x78zum5 x2lah0s']//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xi81zsa']"
            sharePath = "//div[@class='x78zum5 xdt5ytf x1huibft x1n6yrxt']//div[@class='x6s0dn4 xi81zsa x78zum5 x1a02dak x13a6bvl xyesn5m x6ikm8r x10wlt62']//span[@class='_26fq']//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xi81zsa']"
        
            result.append(autoGetData(item,namePath,likePath,commentPath,sharePath,tag))
        else:
            pass
    
    writeToFile(result, postLink, "F")
    messagebox.showinfo(title="Data Extract Complete", message="Successfully extract data from Facebook")
    print("COMPLETE FACEBOOK")

def check(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True