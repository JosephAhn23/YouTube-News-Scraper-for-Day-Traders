from googleapiclient.discovery import build
from datetime import datetime

#API key
api_key = '[YOUR API KEY]'

#Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=api_key)

#Channel to search
channels = ['BBC News', 'CBC News', 'Fox News', 'CNN', 'Al Jazeera English']

#Filtering with Keywords
keywords = ['china', 'raises', 'us']

#Date after April 10
published_after = '2025-04-10T00:00:00Z'

#Must have ("China" "US" "Raises") AND ("%") in youtube title
def title_matches(title):
    lower_title = title.lower()
    return (
        '%' in title and
        any(keyword in lower_title for keyword in keywords)
    )

def get_channel_videos(channel_name):
    print(f"\n🔍 Searching for channel: {channel_name}")
    
    # Search for the channel
    search_response = youtube.search().list(
        q=channel_name,
        type='channel',
        part='id,snippet',
        maxResults=1
    ).execute()

    if not search_response['items']:
        print(f"Channel '{channel_name}' not found.")
        return

    channel_id = search_response['items'][0]['id']['channelId']

    #Get recent videos since April 10
    videos_response = youtube.search().list(
        channelId=channel_id,
        part='snippet',
        order='date',
        maxResults=25,
        publishedAfter=published_after
    ).execute()

    found = False
    for item in videos_response['items']:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        url = f"https://www.youtube.com/watch?v={video_id}"

        if title_matches(title):
            print(f"🎯 {title}\n   {url}")
            found = True

    if not found:
        print("⚠️ No matching videos found.")

#Run it
for channel in channels:
    get_channel_videos(channel)
