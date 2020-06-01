from flask import Flask, render_template, url_for, redirect, request
from pytube import YouTube
import os
from time import sleep
from threading import Thread
from pyimagesearch.face_blurring import anonymize_face_pixelate
from pyimagesearch.face_blurring import anonymize_face_simple
import numpy as np
import cv2



def download_youtube_video(videourl, path):
    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not os.path.exists(path):
        os.makedirs(path)
    yt.download(path,filename="vid")
    return 0

def getFirstWidthHeight(cap,net):
    ret,frame = cap.read()
    if ret == False:
        #if done 
        return -1,-1,-1,1 #return nonreal width height image and code 1
    image = frame
    (h, w) = image.shape[:2]

    # construct a blob from the image
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
        (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is greater
        # than the minimum confidence
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # extract the face ROI
            face = image[startY:endY, startX:endX]

            face = anonymize_face_pixelate(face,blocks=20)

            # store the blurred face in the output image
            image[startY:endY, startX:endX] = face

    # display the original image and the output image with the blurred
    # face(s) side by side
    # output = np.hstack([orig, image])
    # cv2.imshow("Output", output)
    # cv2.imshow("Output",image)
    # cv2.waitKey(0)
    return w,h,image,0




def modify_video():
    # load our serialized face detector model from disk
    print("[INFO] loading face detector model...")
    #path to face detector model
    face_path = './face_detector/'
    prototxtPath = os.path.sep.join([face_path, "deploy.prototxt"])
    weightsPath = os.path.sep.join([face_path,
        "res10_300x300_ssd_iter_140000.caffemodel"])
    net = cv2.dnn.readNet(prototxtPath, weightsPath)
    # print('1')
    # load the input image from disk, clone it, and grab the image spatial
    # dimensions
    cap = cv2.VideoCapture('./videos/vid.mp4')

    #grab audio from video 
    from moviepy.editor import VideoFileClip
    import sys
    audio = VideoFileClip('./static/videos/vid.mp4').audio

    if cap.isOpened() == False:
        print("Error opening file")
        exit(1)
    # print('2')

    frameIdx = 0



    #blur first frame to get width and height of video
    width,height,firstFrame, code = getFirstWidthHeight(cap,net)


    #get fps of video
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)

    # print('3')

    #make output video file 
    outVideo = cv2.VideoWriter("./static/videos/blurVid.avi",cv2.VideoWriter_fourcc(*'MJPG'),fps,(width,height))

    #write first frame
    outVideo.write(firstFrame)

    #get rest of frames
    while cap.isOpened():
        # if frameIdx >= 100:
        #     break

        width,height,frame,code = getFirstWidthHeight(cap,net)
        if code == 1:
            break
        outVideo.write(frame)
        print(frameIdx)
        frameIdx += 1

    # print('4')
        
    # cv2.imshow("Output", frames[699])
    # cv2.waitKey(0)
    outVideo.release()
    cap.release()
    cv2.destroyAllWindows()

    # set audio to final video
    newVid = VideoFileClip('./static/videos/blurVid.avi')
    newVid = newVid.set_audio(audio)
    newVid.write_videofile('./static//videos/finalBlur.mp4')


app = Flask(__name__)
loading=False

@app.route('/',methods = ["POST","GET"])
def index():
    print('method:' + request.method)
    if request.method == "POST":
        url = request.form["urlSub"]
        if url != "": #if they have provided URL, start program
            downloadResult = download_youtube_video(url,'./static/videos/')
            if downloadResult == 0:
                modify_video()
                return render_template("index.html",status="working")
            return render_template("index.html",status="err")

    # GET request
    else:
        # return render_template("index.html",vidName="N/A")
        return render_template("index.html",status="")
        
# @app.route('/returnVideo')
# def returnVideo():



if __name__ == '__main__':
    app.run(debug=True)
