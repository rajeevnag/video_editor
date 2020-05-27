from flask import Flask, render_template, url_for, redirect, request
from pytube import YouTube
import os
from time import sleep
from threading import Thread

def downloadYouTubeVideo(videourl, path):
    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not os.path.exists(path):
        os.makedirs(path)
    yt.download(path)
    return 0
    


app = Flask(__name__)
loading=False



@app.route('/',methods = ["POST","GET"])
def index():
    print('method:' + request.method)
    if request.method == "POST":
        url = request.form["urlSub"]
        if url != "": #if they have provided URL, start program
            downloadResult = downloadYouTubeVideo(url,'./videos/')
            if downloadResult == 0:
                return render_template("index.html",testStr = "GOOD")
            return render_template("index.html",testStr="BAD")

    # GET request or POST request with no input (user hit submit without giving URL)
    else:
        return render_template("index.html",testStr="NEUTRAL")
        
# @app.route('/returnVideo')
# def returnVideo():



if __name__ == '__main__':
    app.run(debug=True)



# if request.method == 'POST':
#         url = request.form["urlSubmission"]
#         finishedLoading = False

#         #make thread to render template and then load video
#         thr=Thread(target=downloadYouTubeVideo,args=[url,"./videos"])
#         thr.start()

#         return redirect(url_for("loading"))

#     else:
#         return render_template("index.html")