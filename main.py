import os
from kivymd.app import MDApp
from pytube import YouTube
from kivy.uix.modalview import ModalView
from kivymd.uix.filemanager import MDFileManager
from plyer import  filechooser
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
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
            self.root.ids.spinner.active = False
            self.root.ids.thumbnail.source = self.youtube.thumbnail
            self.root.ids.search_btn.disabled = False
            self.root.ids.download_btn.disabled = False
            self.root.ids.cancel_btn.disabled = False
    

    def download(self):
        if self.youtube:
            self.youtube.start_download_video_thread()
        


    def progress(self, value):
        self.root.ids.progress_bar.value = value
    



    # def start_links(self):
    #     self.youtube_thread = YoutubeThread()
    #     self.youtube_thread.success_signal.connect(self.links)
    #     self.youtube_thread.progress_signal.connect(self.progress_func)
    #     self.youtube_thread.set_params(self.ui.paste_link_edit.text())
    #     self.youtube_thread.start()

    # def links(self, result):
    #     self.streamer = result['streamer']
    #     self.ui.resolution_combo.clear()
    #     for stream in result['streamer']:
    #         self.ui.resolution_combo.addItem(stream.resolution + ' ' + ': ' + str(round(stream.filesize/1024/1024,2)) + '' + 'MB', stream.resolution)
        
    #     self.ui.language_combo.clear()
    #     self.ui.language_combo.addItem('English', 'en')
    #     self.ui.language_combo.addItem('English (UK)', 'en-GB')
    #     self.ui.language_combo.addItem('Spanish', 'es')

    #     self.ui.title_browser.setText('Title: ' + result['title'])
    #     self.ui.descrip_browser.setText(result['desc'])
    #     self.ui.size_browser.setText('Author: ' + result['author'])
    #     self.ui.views_browser.setText('This video has ' + str(result['views']) + ' views')

        
    # def progress_func(self, progress):
    #     self.ui.progressBar.setValue(progress)
        
    # def download_vid(self):
    #     if self.streamer != None:
    #         selected_res = self.ui.resolution_combo.currentData()
    #         for stream in self.streamer:
    #             if stream.resolution == selected_res:
    #                 self.ui.change_dest.setEnabled(False)
    #                 self.ui.resolution_combo.setEnabled(False)
    #                 self.ui.language_combo.setEnabled(False)
    #                 self.youtube_thread.download_video(stream, self.folder_path)
    #                 self.ui.change_dest.setEnabled(True)
    #                 self.ui.resolution_combo.setEnabled(True)
    #                 self.ui.language_combo.setEnabled(True)
    #                 break

if __name__ == "__main__":
    import sys
    main_window = MainApp()
    main_window.run()
