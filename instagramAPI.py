import requests
import json

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
        print(response)
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
                return [id,username,viewCount,"",likeCount,commentCount,tag]
            else:
                id = response['code']
                username = response['owner']['username']
                # viewCount = response['view_count']
                # playCount = response['play_count']
                likeCount = response['like_count']
                commentCount = response['comment_count']
                return [id,username,"","",likeCount,commentCount,tag]

        except KeyError as e:
            print(str(e))



        # result = response.json()
    #     # result = response.text
    #     # print(result["data"]["like_count"])
    #     caption = result["data"]["caption"]["text"]
    #     likes = result["data"]["like_count"]
    #     views = "" #sebenarnya untuk viewnya ada view_count tapi gua mau kondisiin error ndra coba nanti kalo bisa gua tes lagi
    #     data.append([caption, likes, views])
    # print(data)

# getInstagramAPI("g20",['ClBP_2YvA5S'])