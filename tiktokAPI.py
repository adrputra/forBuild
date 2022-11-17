# import TikTokApi
# import json


# def getTikTokAPI(tag, vId):
#     api = TikTokApi()
#     data = []
#     for id in vId:
#         vidInfo = api.video(id=f'{id}').info()
#         vidInfoData = json.dumps(vidInfo).replace("\'","\"")
#         data.append(parseData(tag,json.loads(vidInfoData)))
#     print(data)
#     return data

# def parseData(tag,data):
#     vId = data['video']['id']
#     author = data['author']['nickname']
#     commentCount = data['stats']['commentCount']
#     likeCount = data['stats']['diggCount']
#     viewCount = data['stats']['playCount']
#     shareCount = data['stats']['shareCount']
#     return [vId,author,viewCount,likeCount,commentCount,shareCount,tag]
    
# # getTikTokAPI("g20",['7164362493689662722'])
# # video = api.video(id='7164362493689662722').info()
# # print(video)

# # for video in api.hashtag(name='indonesia').videos(count=5):
# #     print(video)