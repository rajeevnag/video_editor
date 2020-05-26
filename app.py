from flask import Flask, render_template, url_for, redirect, request
from pytube import YouTube
import os
from time import sleep
from threading import Thread

def downloadYouTubeVideo(videourl, path):
    #delay start by 2 seconds so that index page has time to return html code before loading
    sleep(2)
    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not os.path.exists(path):
        os.makedirs(path)
    yt.download(path)
    finishedLoading = True


app = Flask(__name__)
finishedLoading = False #for downloading videos


@app.route("/loading")
def loading():
    if(finishedLoading):
        return redirect(url_for("index"))

    return render_template("loading.html")

@app.route('/'  ,methods = ["POST","GET"])
def index():
    needToLoad = False
    if request.method == "POST":
        url = request.form["urlSubmission"]
        if url != "": #if they have provided URL, start program
            return render_template("index.html",loading=True)

    # GET request or POST request with no input (user hit submit without giving URL)
    return render_template("index.html",loading=False)
        


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