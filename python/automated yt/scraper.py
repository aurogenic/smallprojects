from datetime import datetime
import os

import instaloader
#import instalooter
# from instalooter.looters import ProfileLooter


def scrape(username = "", password = "", folder="./vid", days = 1):
    
    lasttime = getlasttime()
    
    today = datetime.today().date()
    
    download_folder = os.path.join(os.getcwd(), "vid", str(today))
    os.makedirs(download_folder, exist_ok = True)
    
    insta = instaloader.Instaloader(
    download_pictures=False,
    download_videos=True,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    post_metadata_txt_pattern=None
)
    insta.login(username, password)
    
    insta.dirname_pattern = download_folder
    
    myprofile = instaloader.Profile.from_username(insta.context, username)
    following = myprofile.get_followees()
    #print(following)
    
    count = 0
    for profile in following:
        acc = profile.username
        print("scraping " + acc)
        
        for post in profile.get_posts():
            if post.is_video and post.typename == "GraphVideo" and post.date > lasttime:
                insta.download_post(post, target=download_folder)
                count += 1
                print("downloaded: "+ count)
           
        setlasttime()
            
def getlasttime():
    f = open("date.txt", 'r')
    d = f.read()
    f.close()
    return datetime.fromtimestamp(float(d))
    
    
def setlasttime():
    f = open("date.txt", 'w')
    d = datetime.now().timestamp()
    f.write(str(d))
    f.close
    
def setdefaultlasttime(days):
    f = open("date.txt", 'w')
    d = datetime.now().timestamp()
    d -= days*24*60*60
    f.write(str(d))
    f.close
    
# setdefaultlasttime(10)
scrape("dummyname15", "dummy1515")
