# For get storage.json
# from gsheets import Sheets
# sheets = Sheets.from_files('~/client_secrets.json', '~/storage.json')

import gspread
from google.oauth2.service_account import Credentials
import requests
import json
import os
import google_auth_oauthlib.flow
# from googleapiclient.discovery import build
import googleapiclient.discovery
import googleapiclient.errors


def getDataSheetInstagram(link):
    gc = gspread.oauth(
        credentials_filename='client_secrest.json',
        authorized_user_filename='storage.json'
    )

    sh = gc.open_by_key(link)
    # sh = gc.open_by_key('18k_NEd0jVj6x0gBcF0dAM3CF9O-lKJES5J5DJLbSZ5E')

    result = sh.sheet1.col_values(3)

    IgID = []

    for i in range(1,len(result)):
        if "/p/" in result[i]:
            IgID.append(result[i].split("p/")[1].split("/")[0])
        elif "/reel/" in result[i]:
            IgID.append(result[i].split('reel')[1].split('/')[1])

    print(IgID)
    return IgID

# getDataSheet()

def getDataSheetFacebook(link):
    gc = gspread.oauth(
        credentials_filename='client_secrest.json',
        authorized_user_filename='storage.json'
    )

    sh = gc.open_by_key(link)
    # sh = gc.open_by_key('1H-iD-mZnIH0b4WGQJlbUuafvPeEH1BLgR5w_RIBuWTk')

    result = sh.sheet1.col_values(3)

    postLink = []
    
    for i in range(1,len(result)):
        postLink.append(result[i])
    
    print(postLink)
    return postLink


def getInstagramAPI(tag,links):
    data = []
    for id in links:
        url = "https://instagram-data1.p.rapidapi.com/post/info"

        querystring = {"post":"https://www.instagram.com/p/%s/"%id}

        headers = {
                "X-RapidAPI-Key": "a55e034d55mshbc70cc52c774ecfp169a4ejsn4ccf9fef4b1c",
                "X-RapidAPI-Host": "instagram-data1.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring).text
        # print(response)
        data.append(parseInstagramResponse(tag,json.loads(response)))
    print(data)
    return data

def getInstagramAPIv2(tag,links):
    data = []
    for id in links:
        url = "https://instagram-data1.p.rapidapi.com/post/info"

        querystring = {"post":"%s"%id}

        headers = {
            "X-RapidAPI-Key": "a55e034d55mshbc70cc52c774ecfp169a4ejsn4ccf9fef4b1c",
            "X-RapidAPI-Host": "instagram-data1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring).text
        # print(response)
        data.append(parseInstagramResponse(tag,json.loads(response)))
    print(data)
    return data

def parseInstagramResponse(tag,response):
        try:
            if response['media_type'] == 2:
                id = response['code']
                username = response['owner']['username']
                viewCount = response['view_count']
                # playCount = response['play_count']
                likeCount = response['like_count']
                commentCount = response['comment_count']

                if id is None:
                    id = ""
                if username is None:
                    username = ""
                if viewCount is None:
                    viewCount = ""
                if likeCount is None:
                    likeCount = ""
                if commentCount is None:
                    commentCount = ""
                
                return [id,username,viewCount,"",likeCount,commentCount,tag]
            else:
                id = response['code']
                username = response['owner']['username']
                # viewCount = response['view_count']
                # playCount = response['play_count']
                likeCount = response['like_count']
                commentCount = response['comment_count']

                if id is None:
                    id = ""
                if username is None:
                    username = ""
                if likeCount is None:
                    likeCount = ""
                if commentCount is None:
                    commentCount = ""

                return [id,username,"","",likeCount,commentCount,tag]

        except KeyError as e:
            print(str(e))


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def YoutubeAPI(videoID):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    # client_secrets_file = "client_secret_80453553129-rh62lfh4b51eu42jqbpcjqdiooc2cs01.apps.googleusercontent.com.json"
    # api_key = "AIzaSyCfdFlQbSZorzCoSMTsM2cV_3UM3nDO5DI"
    api_key = "AIzaSyArIm3sQ0SlNiseIfKWmGacgeIcRsAhePY"


    # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     client_secrets_file, scopes)
    # credentials = flow.run_console()
    # youtube = googleapiclient.discovery.build(
    #     api_service_name, api_version, developerKey=api_key)

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key, static_discovery=False)

    vID = ",".join(videoID)
    # print(vID)
    request = youtube.videos().list(
        part ="id,snippet,contentDetails,statistics,status,topicDetails",
        id = f"{vID}"
    )
    response = request.execute()

    # print(response)
    return response