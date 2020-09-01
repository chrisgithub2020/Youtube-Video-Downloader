import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from main_window_ui import Ui_main_window
from pytube import YouTube
from my_threads import YoutubeThread


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        self.streamer = None

        # sets default path when it doesn't exist
        home = os.path.expanduser('~')
        self.folder_path = os.path.join(home, 'Downloads')
        with open('.\icons\path.txt','r+') as path_read1:
            path1 = path_read1.read()
            path_read1.seek(0)
            if path1 == '':
                print('yes')
                path_read1.write(self.folder_path)
        # connect widgets to actions
        self.connect_widgets_to_actions()        

    def connect_widgets_to_actions(self):
        self.ui.search.clicked.connect(self.start_links)
        
        self.ui.change_dest.clicked.connect(self.directory)
        with open('.\icons\path.txt','r') as path_read:
            path = path_read.read()
            path_read.seek(0)
            print(path)
            self.ui.dest_browser.setText(path)
            self.folder_path = path

        self.ui.resolution_combo.activated.connect(self.handleActivated)
        self.ui.dowload_button.clicked.connect(self.download_vid)
        
    def handleActivated(self):
        print(self.ui.resolution_combo.currentData())
 
        
    def directory(self):
        dialog = QFileDialog()
        self.folder_path = dialog.getExistingDirectory(None,"Select folder")
        self.ui.dest_browser.setText(self.folder_path)
        with open('.\icons\path.txt','w') as path:
            path.write(self.folder_path)
        print(self.folder_path)

    def start_links(self):
        self.youtube_thread = YoutubeThread()
        self.youtube_thread.success_signal.connect(self.links)
        self.youtube_thread.progress_signal.connect(self.progress_func)
        self.youtube_thread.set_params(self.ui.paste_link_edit.text())
        self.youtube_thread.start()

    def links(self, result):
        self.streamer = result['streamer']
        self.ui.resolution_combo.clear()
        for stream in result['streamer']:
            self.ui.resolution_combo.addItem(stream.resolution + ' ' + ': ' + str(round(stream.filesize/1024/1024,2)) + '' + 'MB', stream.resolution)
        
        self.ui.language_combo.clear()
        self.ui.language_combo.addItem('English', 'en')
        self.ui.language_combo.addItem('English (UK)', 'en-GB')
        self.ui.language_combo.addItem('Spanish', 'es')

        self.ui.title_browser.setText('Title: ' + result['title'])
        self.ui.descrip_browser.setText(result['desc'])
        self.ui.size_browser.setText('Author: ' + result['author'])
        self.ui.views_browser.setText('This video has ' + str(result['views']) + ' views')

        
    def progress_func(self, progress):
        self.ui.progressBar.setValue(progress)
        
    def download_vid(self):
        if self.streamer != None:
            selected_res = self.ui.resolution_combo.currentData()
            for stream in self.streamer:
                if stream.resolution == selected_res:
                    self.ui.change_dest.setEnabled(False)
                    self.ui.resolution_combo.setEnabled(False)
                    self.ui.language_combo.setEnabled(False)
                    self.youtube_thread.download_video(stream, self.folder_path)
                    self.ui.change_dest.setEnabled(True)
                    self.ui.resolution_combo.setEnabled(True)
                    self.ui.language_combo.setEnabled(True)
                    break

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = MainWin()
    main_window.show()
    sys.exit(app.exec_())
