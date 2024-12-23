import os
from kivymd.app import MDApp
from pytube import YouTube
from kivy.uix.modalview import ModalView
from kivymd.uix.filemanager import MDFileManager
from plyer import  filechooser
from kivy.clock import Clock
from kivymd.toast import toast
from my_threads import YoutubeThread


class MainApp(MDApp):
    def __init__(self):
        super().__init__()
        self.streamer = None
        self.manager = None
        self.manager_open = False
        self.path = ""

        # sets default path when it doesn't exist
        home = os.path.expanduser('~')
        self.folder_path = os.path.join(home, 'Downloads')
        with open('.\icons\path.txt','r+') as path_read1:
            path1 = path_read1.read()
            self.path = path1
            path_read1.seek(0)
            if path1 == '':
                path_read1.write(self.folder_path)
        Clock.schedule_once(self.set_dir, 0)

        
        
    def directory(self):
        self.path = filechooser.choose_dir()[0] if len(filechooser.choose_dir()) > 0 else self.path
        self.set_dir('')
        self.save_new_dir(self.path)

    def set_dir(self, _):
        self.root.ids.download_dir.text = "Download destination: " + self.path if self.path else self.folder_path
        
    def save_new_dir(self, path):
        with open("./icons/path.txt", mode="w") as file:
            file.write(path)


    def search(self):
        print("searching...")
        link = self.root.ids.video_link.text
        if link != "":
            self.root.ids.search_btn.disabled = True
            self.root.ids.download_btn.disabled = True
            self.root.ids.cancel_btn.disabled = True
            self.root.ids.spinner.active = True
            Clock.schedule_once(self.check_search_thread,1)
            self.youtube = YoutubeThread(link=link, destination=self.path, progress_callback=self.progress)
            

    def check_search_thread(self, _):
        if self.youtube.get_video_thread.is_alive():
            Clock.schedule_once(self.check_search_thread,1)
        else:
            if self.youtube.link_auth == False:
                toast("link is not valid or check your internet connection")
            self.root.ids.spinner.active = False
            self.root.ids.thumbnail.source = self.youtube.thumbnail if self.youtube.link_auth else "./icons/youtube.png"
            self.root.ids.search_btn.disabled = False
            self.root.ids.download_btn.disabled = False
            self.root.ids.cancel_btn.disabled = False
    

    def download(self):
        if self.youtube:
            self.youtube.start_download_video_thread()
        


    def progress(self, value):
        self.root.ids.progress_bar.value = value
    



if __name__ == "__main__":
    import sys
    main_window = MainApp()
    main_window.run()
