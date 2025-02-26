from pytube import YouTube
from pytube import Search
import time
import csv
import datetime
import os
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

searchTerms = ['tradwives', 'unschooling', 'how to unschool your child']

def getVideos(term):
    videos = []
    s = Search(term)
    for i in range(0, 7):
        res = s.results

        for r in res:
            video = {
                'id': r.video_id,
                'author': r.author,
                'title': r.title,
            }

            videos.append(video)
            print(video)
        
        s.get_next_results()
        time.sleep(30)
    return videos

def exportData(term, videos):
    fieldnames = videos[0].keys()

    if not os.path.isdir('./media'):
        os.mkdir('./media')

    with open(f'./{term}_{datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")}.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for video in videos:
            writer.writerow(video)


for search in searchTerms:
    videos = getVideos(search)
    exportData(videos)
