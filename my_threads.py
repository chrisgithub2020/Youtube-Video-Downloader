from PyQt5.QtCore import QThread, pyqtSignal
from pytube import YouTube


class YoutubeThread(QThread):

    success_signal = pyqtSignal(dict)
    progress_signal = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        self.search_link = ""

    def set_params(self, search_link):
        self.search_link = search_link

    def progress_func(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        progress = (float(abs(int(bytes_remaining)-size))/size)*float(100)
        self.progress_signal.emit(progress)

    def download_video(self, stream, folder_path):
        
        stream.download(folder_path)

    def run(self):
        link = YouTube(self.search_link, on_progress_callback=self.progress_func)
        title = link.title
        desc = link.description
        views = link.views
        subtitle = link.captions.all()
        streamer = link.streams.filter(only_video=True).all()
        result_dict = {'title': title, 'desc': desc, 'streamer': streamer, 'views':views, 'subtitle':subtitle}
        self.success_signal.emit(result_dict)
