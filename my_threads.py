from threading import Thread
from pytube import YouTube
from yt_dlp import YoutubeDL

class YoutubeThread():
    video = ""
    thumbnail = ''
    get_video_thread = ""
    download_thread = ""
    
    def __init__(self, link:str, destination: str, progress_callback):
        self.search_link = link.strip()
        self.destination = destination
        self.on_progress = progress_callback
        self.ydl_opts = { 'format': 'best', 'outtmpl': f'{self.destination}/%(title)s.%(ext)s', "progress_hooks":[self.progress]}
        self.get_video_thread = Thread(target=self.get_video)
        self.get_video_thread.start()

    def set_params(self, search_link):
        self.search_link = search_link


    def get_video(self):
        self.video = YoutubeDL(self.ydl_opts)
        info_dict = self.video.extract_info(self.search_link,download=False)
        thumbnail_url = info_dict.get("thumbnail",'No thumbnail found')
        self.thumbnail = thumbnail_url


    def download_video(self):        
        self.video.download([self.search_link])

    def start_download_video_thread(self):
        self.download_thread = Thread(target=self.download_video)
        self.download_thread.start()

    def progress(self,d):
        if d['status'] == "downloading":
            downloaded = d.get("downloaded_bytes",0)
            total = d.get("total_bytes",1)
            progress_value = int(downloaded/total * 100)
            self.on_progress(progress_value)
        if d['status'] == 'finished':
            self.on_progress(100)
