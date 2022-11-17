# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
# from googleapiclient.discovery import build
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main(videoID):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    # client_secrets_file = "client_secret_80453553129-rh62lfh4b51eu42jqbpcjqdiooc2cs01.apps.googleusercontent.com.json"
    api_key = "AIzaSyCfdFlQbSZorzCoSMTsM2cV_3UM3nDO5DI"

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

# if __name__ == "__main__":
#     main()