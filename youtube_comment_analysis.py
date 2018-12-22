
from apiclient.discovery import build
from oauth2client.tools import argparser
import sys
import requests
import json
from textblob import TextBlob
import re




DEVELOPER_KEY = "***developer key assigned***"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"




def clean_comment(comment): 
        
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", comment).split()) 
def get_comment_sentiment(comment): 
       
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(clean_comment(comment)) 
        
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  


def youtube_search(query,max_results):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  
  # query term.
  search_response = youtube.search().list(
    q=query,
    part="id,snippet",
    maxResults=max_results
  ).execute()

  videos = []
  sent_count=[]
  
  for search_result in search_response.get("items", []):
    if(search_result["id"]["kind"] == "youtube#video"):
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
      print(search_result["id"]["videoId"])


     
      comments=requests.get('https://www.googleapis.com/youtube/v3/commentThreads?key=***your developerkey***&textFormat=plainText&part=snippet&videoId='+search_result["id"]["videoId"]+'&maxResults=20')
      data = comments.json()
      print("video_link : "+(search_result["snippet"]["title"]).translate(non_bmp_map)+" ,\nComments: ")
      check=0
      if("error" in data):
        check=1
        #videos here yet to be explored much
      if(check==0):
        pcount=0
        ncount=0
        for item in data["items"]:
          comment = item["snippet"]["topLevelComment"]
          author = comment["snippet"]["authorDisplayName"]
          text = comment["snippet"]["textDisplay"]
          parsed_comment = {}
          parsed_comment['text'] = text
          parsed_comment['sentiment'] =get_comment_sentiment(text)
          if(parsed_comment['sentiment']=='positive'):
            pcount+=1
          if(parsed_comment['sentiment']=='negative'):
            ncount+=1
          print("Comment by "+author.translate(non_bmp_map)+" : "+text.translate(non_bmp_map)+"\nSentiment is:"+parsed_comment['sentiment'])
        print("\n")
        ratio_count=(pcount+1)/(ncount+1)
        print(ratio_count)
        sent_count.append((search_result["id"]["videoId"],ratio_count))
   


  print("Sorted youtube Videos:")
  for k in sorted(sent_count,key=lambda x:x[1],reverse=True):
          print("https://www.youtube.com/watch?v="+str(k[0]))
          
   
                
                  
              
          



non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
query=input("Enter the query you want to search:  ")
max_results=20
youtube_search(query,max_results)
