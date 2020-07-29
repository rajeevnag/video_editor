from pytube import YouTube

video = YouTube('https://www.youtube.com/watch?v=NqC_1GuY3dw')

video.streams.filter(file_extension = "mp4").all()

video.streams.get_by_itag(18).download()
