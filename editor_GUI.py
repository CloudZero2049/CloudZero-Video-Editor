import os
import glob
from os import path

from PySide6.QtWidgets import QMainWindow, QMenu, QLabel, QWidget, QGridLayout, QPushButton, QLineEdit, QProgressBar, QComboBox, QListWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog, QAbstractItemView, QListWidgetItem, QSizePolicy
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QFont
from shiboken6 import isValid

from editor_engine import *
# from cloudzero_video_editor import master_shutdown

VERSION = "0.1.5"

# check or create storage folders
# stored_editor_clips = glob.glob("editor_clips/*")


class editorWindow(QMainWindow):
    def __init__(self, win_id, main_window, editor, tool_type):
        super().__init__()
        self.win_id = win_id
        self.setWindowTitle(f'{tool_type} Window')
        self.resize(500, 300)
        self.editor = editor

# ! Keeps the middle
class ExtractWindow(editorWindow):
    def __init__(self, main_window, win_id, editor, tool_type):
        super().__init__(main_window, win_id, editor, tool_type)

        # Central Container
        central = QWidget()
        self.setCentralWidget(central)
        central_layout = QGridLayout()
        central.setLayout(central_layout)

        font = QFont()
        font.setPointSize(main_window.font_size)
        central.setFont(font)

        about_label = QLabel("Choose a start and end time. The middle portion will be kept and the ends will be removed")
        about_label.setAlignment(Qt.AlignCenter)
        about_label.setWordWrap(True)
        central_layout.addWidget(about_label, 0, 0, 1, 1)

        start_label = QLabel("Start: ")
        central_layout.addWidget(start_label, 1, 0, 1, 1)
        # IMPORTANT
        # can be expressed in seconds (15.35), in (min, sec), in (hour, min, sec), or as a string: ‘01:03:05.35’.
        # Example validation:
        # import re
        # pattern = r"^\d{1,2}:\d{2}(:\d{2}(\.\d+)?)?$"

        start_time = QLineEdit()
        start_time.setPlaceholderText('1 min, 20 second Example: 1:20 or (1, 20) or 00:01:20.00')
        central_layout.addWidget(start_time, 2, 0, 1, 1)

        end_label = QLabel("End: ")
        central_layout.addWidget(end_label, 3, 0, 1, 1)
        end_time = QLineEdit()
        end_time.setPlaceholderText('1 hour, 5 min, 40 second, 10 milisecond Example: (1, 5, 40) or 01:05:40.10') # ? 1.05.40 or
        central_layout.addWidget(end_time, 4, 0, 1, 1)


        # Bottom buttons
        toolbar = QHBoxLayout()
        accept_btn = QPushButton(f'Accept {tool_type}')
        accept_btn.clicked.connect(lambda: editor.extract_clip(self, main_window, start_time.text(), end_time.text()))
        
        toolbar.addWidget(accept_btn)
        # addWidget(widget, row, column, rowSpan, columnSpan, alignment) # Qt.AlignCenter
        central_layout.addLayout(toolbar, 5, 1, 1, 1)


# ! removes the middle
class CutOutWindow(editorWindow):
    def __init__(self,main_window, win_id, editor, tool_type):
        super().__init__(main_window, win_id, editor, tool_type)
        # Central Container
        central = QWidget()
        self.setCentralWidget(central)
        central_layout = QGridLayout()
        central.setLayout(central_layout)

        font = QFont()
        font.setPointSize(main_window.font_size)
        central.setFont(font)

        about_label = QLabel("Choose a start and end time. The middle portion will be removed and the ends will be kept")
        about_label.setAlignment(Qt.AlignCenter)
        about_label.setWordWrap(True)
        central_layout.addWidget(about_label, 0, 0, 1, 1)

        start_label = QLabel("Start: ")
        central_layout.addWidget(start_label, 1, 0, 1, 1)

        start_time = QLineEdit()
        start_time.setPlaceholderText('1 min, 20 second Example: 1:20 or (1, 20) or 00:01:20.00')
        central_layout.addWidget(start_time, 2, 0, 1, 1)

        end_label = QLabel("End: ")
        central_layout.addWidget(end_label, 3, 0, 1, 1)
        end_time = QLineEdit()
        end_time.setPlaceholderText('1 hour, 5 min, 40 second, 10 milisecond Example: (1, 5, 40) or 01:05:40.10') # ? 1.05.40 or
        central_layout.addWidget(end_time, 4, 0, 1, 1)


        # Bottom buttons
        toolbar = QHBoxLayout()
        accept_btn = QPushButton(f'Accept {tool_type}')
        accept_btn.clicked.connect(lambda: editor.cut_out_clip(self, main_window, start_time.text(), end_time.text()))
        
        toolbar.addWidget(accept_btn)
        # addWidget(widget, row, column, rowSpan, columnSpan, alignment) # Qt.AlignCenter
        central_layout.addLayout(toolbar, 5, 1, 1, 1)

# Split a clip into 2 separate clips
class SplitWindow(editorWindow):
    def __init__(self,main_window, win_id, editor, tool_type):
        super().__init__(main_window, win_id, editor, tool_type)
        # Central Container
        central = QWidget()
        self.setCentralWidget(central)
        central_layout = QGridLayout()
        central.setLayout(central_layout)

        font = QFont()
        font.setPointSize(main_window.font_size)
        central.setFont(font)

        about_label = QLabel("Choose a split time. 2 new timeline items will replace the single timeline item")
        about_label.setAlignment(Qt.AlignCenter)
        about_label.setWordWrap(True)
        central_layout.addWidget(about_label, 0, 0, 1, 1)

        split_label = QLabel("Split Time: ")
        central_layout.addWidget(split_label, 1, 0, 1, 1)

        split_time = QLineEdit()
        split_time.setPlaceholderText('1 min, 20 second Example: 1:20 or (1, 20) or 00:01:20.00')
        central_layout.addWidget(split_time, 2, 0, 1, 1)


        # Bottom buttons
        toolbar = QHBoxLayout()
        accept_btn = QPushButton(f'Accept {tool_type}')
        accept_btn.clicked.connect(lambda: editor.split_clip(self, main_window, split_time.text()))
        
        toolbar.addWidget(accept_btn)
        # addWidget(widget, row, column, rowSpan, columnSpan, alignment) # Qt.AlignCenter
        central_layout.addLayout(toolbar, 5, 1, 1, 1)

class Insert_Text_Window(editorWindow):
    def __init__(self,main_window, win_id, editor, tool_type):
        super().__init__(main_window, win_id, editor, tool_type)

class BlackFadeWindow(editorWindow):
    def __init__(self,main_window, win_id, editor, tool_type):
        super().__init__(main_window, win_id, editor, tool_type)

class SoundFadeWindow(editorWindow):
    def __init__(self,main_window, win_id, editor, tool_type):
        super().__init__(main_window, win_id, editor, tool_type)

class VolumeWindow(editorWindow):
    def __init__(self,main_window, win_id, editor, tool_type):
        super().__init__(main_window, win_id, editor, tool_type)

class ProgressWindow(QMainWindow):
    def __init__(self, main_window, win_id):
        super().__init__()
        self.setWindowTitle("Export Progress")
        self.resize(400, 200)

        # Central Container
        central = QWidget()
        self.setCentralWidget(central)

        central_layout = QVBoxLayout()
        central.setLayout(central_layout)
        font = QFont()
        font.setPointSize(main_window.font_size)
        central.setFont(font)

        # Status Label
        self.status_label = QLabel("Preparing...")
        central_layout.addWidget(self.status_label)

        # Time estimate label
        self.time_estimate_label = QLabel("Estimated time: ?:?? minutes (need to calculate new estimates)")
        central_layout.addWidget(self.time_estimate_label)
        
        # progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        central_layout.addWidget(self.progress_bar)

class ExportWindow(QMainWindow):
    def __init__(self, main_window, win_id):
        super().__init__()
        self.setWindowTitle("Export Window")
        self.resize(500, 300)

        # font = QFont()
        # font.setPointSize(12)

        # Central Container
        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.central_layout = QGridLayout()
        self.central.setLayout(self.central_layout)
        self.central_layout.setColumnStretch(0, 1)
        font = QFont()
        font.setPointSize(main_window.font_size)
        self.central.setFont(font)
        # Examples
        # self.central_layout.setColumnStretch(0, 1)  # label column gets 1 part
        # self.central_layout.setColumnStretch(1, 3)  # input column gets 3 parts
        #The general rule of thumb: use QGridLayout for overall structure, then nest QHBoxLayout/QVBoxLayout 
        # inside cells when you need a row to behave differently. This gives you the best of both worlds.

        # Export Info
        self.about_label = QLabel("Choose an output location and a resolution. If a video clip is not the selected resolution then it will be resized (at the cost of export time)")
        self.about_label.setAlignment(Qt.AlignCenter)
        self.about_label.setWordWrap(True)
        self.central_layout.addWidget(self.about_label, 0, 0, 1, 1)

        # Size Detection
        self.size_check_label = QLabel("Checking video resolutions...")
        self.size_check_label.setAlignment(Qt.AlignCenter)
        self.central_layout.addWidget(self.size_check_label, 1, 0, 1, 1)
        
        # for clip in main_window.editor.timeline:
        #     size = None
        #     if clip['video']['path']:
        #         if size is not None and clip['video']['size'] != size:
        #             about_label.setText("Video size mismatch found. Some clips will be resized")
        #             break
        #         size = clip['video']['size']
        #     about_label.setText("no video size mismatches found. Maximum output speed ensured")

        self.row3_widget = QWidget()
        self.row3_layout = QHBoxLayout(self.row3_widget)
        self.row4_widget = QWidget()
        self.row4_layout = QHBoxLayout(self.row4_widget)
        # row_layout.addWidget(self.res_combo)
        # row_layout.addWidget(self.accept_btn)
        # self.central_layout.addWidget(row_widget, 3, 1, 1, 2)

        # Export destination
        self.export_label = QLabel("Export Destination: ")
        self.row3_layout.addWidget(self.export_label)
        self.export_dest = QLineEdit()
        self.export_dest.setPlaceholderText('output/CZVE_video.mp4')
        self.export_dest.setText('output/CZVE_video.mp4')
        self.export_dest.setAlignment(Qt.AlignLeft)
        self.row3_layout.addWidget(self.export_dest)


        # Export Resolution Selector
        self.res_label = QLabel("Export Resolution:")
        self.row4_layout.addWidget(self.res_label)
        self.res_combo = QComboBox()
        self.res_combo.addItems(['640x360', '1280x720', '1920x1080'])
        self.res_combo.setCurrentIndex(1)
        self.row4_layout.addWidget(self.res_combo)

        self.accept_btn = QPushButton(f'Start Export')
        self.accept_btn.clicked.connect(lambda: main_window.editor.export(main_window, self.res_combo.currentText(), self.export_dest.text()))
        #                                   cut_clip(self, window, main_window, timeline_clip, start_time, end_time):
        self.row4_layout.addWidget(self.accept_btn)
        self.central_layout.addWidget(self.row3_widget, 2, 0, 1, 1)
        self.central_layout.addWidget(self.row4_widget, 3, 0, 1, 2)
        # addWidget(widget, row, column, rowSpan, columnSpan, alignment) # Qt.AlignCenter
        self.res_combo.currentIndexChanged.connect(lambda: main_window.update_export_size_check(self))
        main_window.update_export_size_check(self)
        

class MainWindow(QMainWindow):
    def __init__(self, master, editor):
        super().__init__()
        self.setWindowTitle("CloudZero Video Editor")
        self.resize(1000, 750)
        self.font_size = 12
        self.master = master
        self.editor = editor
        self.window_counter = 1
        self.windows = []
        self.export_open = False
        self.extract_open = False
        self.cut_out_open = False
        self.split_open = False
        #self.insert_text_open = False
        #self.black_fade_open = False
        #self.sound_fade_open = False
        #self.volume_open = False
        self._setup_ui()


    def _setup_ui(self):
        # menu
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")
        view_menu = menu_bar.addMenu("View")
        help_menu = menu_bar.addMenu("Help")

        submenu = file_menu.addMenu("Submenu")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.master.master_shutdown)
        exit_action2 = submenu.addAction("Exit")
        exit_action2.triggered.connect(self.master.master_shutdown)

        about_action = help_menu.addAction("About")
        about_action.triggered.connect(lambda: print("This is a PySide6 testing application."))

        # Central Container
        central = QWidget()
        self.setCentralWidget(central)

        central_layout = QGridLayout()
        central.setLayout(central_layout)
        font = QFont()
        font.setPointSize(self.font_size)
        central.setFont(font)
        # --------------------------------------------------
        # Top toolbar
        # --------------------------------------------------
        toolbar = QHBoxLayout()
        
        self.import_btn = QPushButton('📂 Import Files')
        self.import_btn.clicked.connect(self.import_files)
        toolbar.addWidget(self.import_btn)

        self.import_vidc_btn = QPushButton('📁 Import From editor_clips')
        self.import_vidc_btn.clicked.connect(self.import_from_editor_clips)
        toolbar.addWidget(self.import_vidc_btn)

        self.clear_media_btn = QPushButton('🗑️ Clear Media list')
        self.clear_media_btn.clicked.connect(self.clear_media_list)
        toolbar.addWidget(self.clear_media_btn)

        toolbar.addStretch()

        # Export Button
        self.export_btn = QPushButton('💾 Export Window (.mp4)')
        self.export_btn.clicked.connect(lambda: self.new_window('Export'))
        toolbar.addWidget(self.export_btn)

        # addWidget(widget, row, column, rowSpan, columnSpan, alignment) # Qt.AlignCenter
        central_layout.addLayout(toolbar, 0, 0, 1, 2)

        # --------------------------------------------------
        # Main Split
        # --------------------------------------------------
        main_split = QHBoxLayout()
        # LEFT PANEL: Import & Media Library
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel('<b>Media Library</b>'))
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.file_list.setMinimumHeight(80)
        left_panel.addWidget(self.file_list)

        import_buttons = QHBoxLayout()
        add_item_btn = QPushButton('🎥 Add to Timeline')
        add_item_btn.clicked.connect(self.add_selected_to_timeline)
        import_buttons.addWidget(add_item_btn)
        override_audio_btn = QPushButton('🎵 Override Audio')
        override_audio_btn.clicked.connect(self.override_audio)
        import_buttons.addWidget(override_audio_btn)
        remove_item_btn = QPushButton('❌ Remove From Timeline')
        remove_item_btn.clicked.connect(self.remove_selected_from_timeline)
        import_buttons.addWidget(remove_item_btn)
        left_panel.addLayout(import_buttons)
        
        main_split.addLayout(left_panel, 1)
        

        # CENTER: Playback + Controls
        center_panel = QVBoxLayout()
        #self.video_widget = QtMultimediaWidgets.QVideoWidget()
        #self.video_widget.setStyleSheet("background-color: black;")
        #center_panel.addWidget(self.video_widget, 4)
        
        controls = QHBoxLayout()
        self.play_btn = QPushButton('▶️ Preview')
        #self.play_btn.clicked.connect(self.preview_project)
        controls.addWidget(self.play_btn)
        # self.stop_btn = QPushButton('⏹ Stop')
        # self.stop_btn.clicked.connect(self.stop_preview)
        # controls.addWidget(self.stop_btn)
        
        controls.addStretch()
        self.status_label = QLabel('Ready')
        controls.addWidget(self.status_label)
        
        center_panel.addLayout(controls)
        main_split.addLayout(center_panel, 1)

        # media player area
        # Actual preview will be in a separate window

        # Show first frame of selected clip

        # RIGHT PANEL: Edit Tools
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel('<b>Edit Tools</b>'))

        tool_buttons = [
            #('Copy', self.editor.copy_clip),
            #('Paste', self.editor.paste_clip),
            ('✂️ Extract (keep)', lambda: self.new_window('Extract')), # extract and use middle
            ('Cut Out (delete)', lambda: self.new_window('Cut_Out')), # cut out middle and use (merge) sides.
            ('Split', lambda: self.new_window('Split')), # Divide a clip at a point into two separate clips
            ('Insert Text Frame', lambda: self.new_window('Insert_Text')),
            ('Add Black Fade', lambda: self.new_window('Black_Fade')),
            ('Add Sound Fade', lambda: self.new_window('Sound_Fade')),
            ('Edit Volume', lambda: self.new_window('Volume')),
        ]
        for text, func in tool_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(func)
            right_panel.addWidget(btn)
        
        right_panel.addStretch()

        main_split.addLayout(right_panel, 1)
        central_layout.addLayout(main_split, 1, 0, 1, 1)

        # --------------------------------------------------
        # TIMELINE: Dual track view
        # --------------------------------------------------
        # timeline_label = QLabel('<b>Timeline</b>')
        # central_layout.addWidget(timeline_label, 2, 0, 1, 1, Qt.AlignCenter)
        
        timeline = QHBoxLayout()

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('Video Track'))
        self.video_list = QListWidget()
        self.video_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.video_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.video_list.setMinimumHeight(80)
        self.video_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.video_list.customContextMenuRequested.connect(self.video_context_menu)

        vbox.addWidget(self.video_list)
        timeline.addLayout(vbox, 1)

        abox = QVBoxLayout()
        abox.addWidget(QLabel('Audio Track'))
        self.audio_list = QListWidget()
        self.audio_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.audio_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.audio_list.setMinimumHeight(80)
        abox.addWidget(self.audio_list)
        timeline.addLayout(abox, 1)

        central_layout.addLayout(timeline, 2, 0, 1, 2)

        self.video_list.installEventFilter(self)
        self.audio_list.installEventFilter(self)
        
        # status bar
        self.status = QLabel('Ready')
        central_layout.addWidget(self.status)

        # version
        central_layout.addWidget(QLabel(f'Version {VERSION}'))

        self.master.check_resources()
        self.master.load_settings()
        self.master.check_for_update(self)


    def import_files(self):
        # paths = stored_video_paths
        paths, _ = QFileDialog.getOpenFileNames(
            self, 'Import media', '', 
            'Media files (*.mp4 *.mov *.mp3 *.wav *.m4a *.mpg *.avi *.mkv);;All files (*)'
        )
       
        for p in paths:
            if p and os.path.exists(p):
                for i in range(self.file_list.count()):
                    if self.file_list.item(i).text() == p:
                        self.file_list.takeItem(i)
                        break

                ext = os.path.splitext(p)[1].lower()
                if ext in [".mp4", ".mov", ".mkv", ".avi"]:
                    icon = "🎬"
                elif ext in [".mp3", ".wav", ".m4a"]:
                    icon = "🎵"
                else:
                    icon = "📄"

                # item = QListWidgetItem(p)
                item = QListWidgetItem(f"{icon} {os.path.basename(p)}")
                item.setToolTip(p)
                
                self.file_list.addItem(item)
                # self.file_list.addItem(os.path.basename(p))
                self.status.setText(f'Imported {os.path.basename(p)}')

    def import_from_editor_clips(self):
        paths = glob.glob("editor_clips/*")
        
        for p in paths:
            if p and os.path.exists(p):
                for i in range(self.file_list.count()):
                    if self.file_list.item(i).text() == p:
                        self.file_list.takeItem(i)
                        break

                ext = os.path.splitext(p)[1].lower()
                if ext in [".mp4", ".mov", ".mkv", ".avi"]:
                    icon = "🎬"
                elif ext in [".mp3", ".wav", ".m4a"]:
                    icon = "🎵"
                else:
                    icon = "📄"            
                item = QListWidgetItem(f"{icon} {os.path.basename(p)}")
                item.setToolTip(p)
                #print(item.toolTip())
                # item = QListWidgetItem(p)
                self.file_list.addItem(item)
                # self.file_list.addItem(os.path.basename(p))
                self.status.setText(f'Imported {os.path.basename(p)}')

    def clear_media_list(self):
        self.file_list.clear()
        self.status.setText('Cleared media list')

    def update_export_size_check(self,from_window):
        width = None
        height = None
        
        if from_window:
            res_text = from_window.res_combo.currentText()
            match res_text:
                case '640x360':
                    width = 640
                    height = 360
                case '1280x720':
                    width = 1280
                    height = 720
                case '1920x1080':
                    width = 1920
                    height = 1080
                case _: 
                    print("an error occurated getting resolution from combo box")
                    from_window.size_check_label.setText("unabled to verify size from combo box")
                    return False
            for clip in self.editor.timeline:
                if clip['video']['path']:
                    if width is not None and (clip['video']['width'] != width or clip['video']['height'] != height):
                        from_window.size_check_label.setText("Video size mismatch found. Some clips will be resized")
                        return False
                    width = clip['video']['width']
                    height = clip['video']['height']
            from_window.size_check_label.setText("no video size mismatches found. Maximum output speed ensured")
            return True
        else:
            for window in self.windows:
                if window.windowTitle() == "Export Window":
                    res_text = window.res_combo.currentText()
                    match res_text:
                        case '640x360':
                            width = 640
                            height = 360
                        case '1280x720':
                            width = 1280
                            height = 720
                        case '1920x1080':
                            width = 1920
                            height = 1080
                        case _: 
                            print("an error occurated getting resolution from combo box")
                            window.size_check_label.setText("unabled to verify size from combo box")
                            return False
                    for clip in self.editor.timeline:
                        if clip['video']['path']:
                            if width is not None and (clip['video']['width'] != width or clip['video']['height'] != height):
                                window.size_check_label.setText("Video size mismatch found. Some clips will be resized")
                                return False
                            width = clip['video']['width']
                            height = clip['video']['height']
                            
                    window.size_check_label.setText("no video size mismatches found. Maximum output speed ensured")
                    return True# only 1 windows of each allowed

    def add_selected_to_timeline(self):
        if not self.file_list.selectedItems():
            self.status.setText(f'Nothing is selected from file list')
            return
        
        
        for it in self.file_list.selectedItems():
            path = it.toolTip()
            basename = os.path.basename(path)
            ext = os.path.splitext(path)[1].lower()
            if ext not in [".mp4", ".mov", ".mkv", ".avi"]:
                self.add_selected_to_timeline_audio(path, basename, ext)
                # log
                continue
            
            clip_data = {
                'id': self.editor.id_counter,
                'video': {'path': path,'clip': VideoFileClip(path), 'name': basename, 'width': 0, 'height': 0, 'size': [0,0], 'fps': 30,'duration': 0},
                'audio': {'path': None,'clip': None, 'name': None, 'duration': 0},
                'vfx': [],
                'afx': []
            }
            
            clip_data['video']['width'] = clip_data['video']['clip'].w
            clip_data['video']['height'] = clip_data['video']['clip'].h
            clip_data['video']['size'] = clip_data['video']['clip'].size
            clip_data['video']['fps'] = clip_data['video']['clip'].fps
            clip_data['video']['duration'] = clip_data['video']['clip'].duration
            dur_min_base = clip_data['video']['duration'] / 60
            dur_min = round(dur_min_base, 2)

            self.editor.id_counter += 1
            self.editor.timeline.append(clip_data)
            
            size_info = f'{clip_data["video"]["width"]}x{clip_data["video"]["height"]}, ' if {clip_data["video"]["path"]} else ""
            
            timeline_item_V = QListWidgetItem(f"🎬 {basename}: {size_info}{dur_min} minutes")
            timeline_item_V.setData(Qt.UserRole, clip_data)
            
            self.video_list.addItem(timeline_item_V)
        
            timeline_item_A = QListWidgetItem(f'<-- *From Video Clip*')
            timeline_item_A.setData(Qt.UserRole, clip_data)
                
            self.audio_list.addItem(timeline_item_A)

        self.update_export_size_check(None)
        # needs proper status and log handling
        #self.status.setText(f'{os.path.basename(clip_data['video']['path'])} added to video track')

    def add_selected_to_timeline_audio(self, path, basename, ext):
        if ext not in [".mp3", ".wav", ".m4a"]:
            self.status.setText(f'{basename} is not a recognizedvideo or audio file, skipping')
            # log
            return
        
        clip_data = {
            'id': self.editor.id_counter,
            'video': {'path': None,'clip': None, 'name': None, 'width': 0, 'height': 0, 'size': [0,0], 'fps': 30,'duration': 0},
            'audio': {'path': path,'clip': AudioFileClip(path), 'name': basename, 'duration': 0},
            'vfx': [],
            'afx': [] 
        }
        
        clip_data['audio']['duration'] = clip_data['audio']['clip'].duration
        dur_min_base = clip_data['audio']['duration'] / 60
        dur_min = round(dur_min_base, 2)

        self.editor.id_counter += 1
        self.editor.timeline.append(clip_data)
        timeline_item_A = QListWidgetItem(f"🎵 {basename}: {dur_min} minutes")
        timeline_item_A.setData(Qt.UserRole, clip_data)
        
        self.audio_list.addItem(timeline_item_A)

        timeline_item_V = QListWidgetItem(f'*Audio Only* -->')
        timeline_item_V.setData(Qt.UserRole, clip_data)
            
        self.video_list.addItem(timeline_item_V)
        # not checking size for audio
        # log
        #self.status.setText(f'{os.path.basename(clip_data['audio']['path'])} added to audio track')

    

    def get_timeline_clip(self): # can probably send the row in the return statement
        if not self.video_list.selectedItems() and not self.audio_list.selectedItems():
            print('Nothing selected from timeline')
            return None
        elif self.video_list.selectedItems():
            for video_list_item in self.video_list.selectedItems():
                clip = video_list_item.data(Qt.UserRole)
                timeline_clip = None
                for item in self.editor.timeline:
                        if item['id'] == clip['id']:
                            timeline_clip = item
                            break
                return timeline_clip, 'video'
        else:
            for audio_list_item in self.audio_list.selectedItems():
                clip = audio_list_item.data(Qt.UserRole)
                timeline_clip = None
                for item in self.editor.timeline:
                        if item['id'] == clip['id']:
                            timeline_clip = item
                            break
                return timeline_clip, 'audio'

    def remove_selected_from_timeline(self):
        if not self.video_list.selectedItems() and not self.audio_list.selectedItems():
            self.status.setText(f'Nothing is selected from timeline')
            return None
        
        # remove video clip
        if self.video_list.selectedItems():
            for video_item in self.video_list.selectedItems():
                clip = video_item.data(Qt.UserRole)
                clip_id = clip['id']
                timeline_item = None
                for item in self.editor.timeline:
                        if item['id'] == clip['id']:
                            timeline_item = item
                            break

                if timeline_item['audio']['path'] is None or timeline_item['video']['path'] is None:
                    if timeline_item['video']['clip']:
                        timeline_item['video']['clip'].close()

                    if timeline_item['audio']['clip']:
                        timeline_item['audio']['clip'].close()
                        
                    self.editor.timeline = [c for c in self.editor.timeline if c['id'] != clip_id]

                    # remove video info from video list
                    self.video_list.takeItem(self.video_list.row(video_item))

                    # remove audio info from audio list
                    for i in range(self.audio_list.count()):
                        audio_item = self.audio_list.item(i)
                        audio_clip = audio_item.data(Qt.UserRole)

                        if audio_clip and audio_clip['id'] == clip_id:
                            self.audio_list.takeItem(i)
                            break
                else: # either timeline_item video or audio has a path
    
                    clip['video'] = {'path': None,'clip': None}
                    video_item.setText(f'*Audio Only* -->')
                    timeline_item['video'] = {'path': None,'clip': None}
     
        else: # self.audio_list.selectedItems()
            for audio_item in self.audio_list.selectedItems():
                clip = audio_item.data(Qt.UserRole)
                clip_id = clip['id']
                timeline_item = None
                for item in self.editor.timeline:
                        if item['id'] == clip['id']:
                            timeline_item = item
                            break

                if timeline_item['audio']['path'] is None or timeline_item['video']['path'] is None:
                    if timeline_item['video']['clip']:
                        timeline_item['video']['clip'].close()

                    if timeline_item['audio']['clip']:
                        timeline_item['audio']['clip'].close()

                    self.editor.timeline = [c for c in self.editor.timeline if c['id'] != clip_id]

                    # remove audio info from audio list
                    self.audio_list.takeItem(self.audio_list.row(audio_item))

                    # remove video info from video list
                    for i in range(self.video_list.count()):
                        video_item = self.video_list.item(i)
                        video_clip = video_item.data(Qt.UserRole)

                        if video_clip and video_clip['id'] == clip_id:
                            self.video_list.takeItem(i)
                            break
                else:
                    clip['audio'] = {'path': None,'clip': None}
                    audio_item.setText(f'<-- *From Video Clip*')
                    timeline_item['audio'] = {'path': None,'clip': None}            

        self.update_export_size_check(None)

    def video_context_menu(self, pos):
        menu = QMenu()
        override_action = menu.addAction("🎵 Override Audio")
        action = menu.exec_(self.video_list.mapToGlobal(pos))

        if action == override_action:
            self.override_audio()
    
    
    def override_audio(self):

        # Ensure timeline video is selected
        video_items = self.video_list.selectedItems()
        if not video_items:
            self.status.setText("Select a video clip first")
            return

        # Ensure audio from media bin is selected
        media_items = self.file_list.selectedItems()
        if not media_items:
            self.status.setText("Select a single audio file from media bin")
            return

        media_item = media_items[0]
        path = media_item.toolTip()
        ext = os.path.splitext(path)[1].lower()
        basename = os.path.basename(path)

        if ext not in [".mp3", ".wav", ".m4a"]:
            self.status.setText("Selected media from bin is not an audio file")
            return

        for video_item in self.video_list.selectedItems():
            clip_data = video_item.data(Qt.UserRole)

            # Replace audio
            clip_data['audio'] = {'path': path,'clip': AudioFileClip(path)}

            for item in self.editor.timeline:
                    if item['id'] == clip_data['id']:
                        item['audio'] = {'path': path,'clip': AudioFileClip(path)}
                        break

            # add audio info to audio list
            for i in range(self.audio_list.count()):
                audio_item = self.audio_list.item(i)
                audio_item_data = audio_item.data(Qt.UserRole)

                if audio_item_data and audio_item_data['id'] == clip_data['id']:
                    clip_data['audio']['duration'] = clip_data['audio']['clip'].duration
                    dur_min_base = clip_data['audio']['duration'] / 60
                    dur_min = round(dur_min_base, 2)
                    audio_item.setText(f'🎵 {basename}: {dur_min} minutes')
                    break
            
        self.status.setText("Audio override applied")
  
    def update_duration(self, timeline_clip):
        if timeline_clip['video']['path']:
            for i in range(self.video_list.count()):
                    video_item = self.video_list.item(i)
                    video_item_data = video_item.data(Qt.UserRole)

                    if video_item_data and video_item_data['id'] == timeline_clip['id']:
                        # basename = os.path.basename(timeline_clip['video']['path'])
                        timeline_clip['video']['duration'] = timeline_clip['video']['clip'].duration
                        dur_min_base = timeline_clip['video']['duration'] / 60
                        dur_min = round(dur_min_base, 2)
                        size_info = f'{timeline_clip["video"]["width"]}x{timeline_clip["video"]["height"]}, ' if {timeline_clip["video"]["path"]} else ""
                        video_item.setText(f'🎬 {timeline_clip['video']['name']}: {size_info}{dur_min} minutes')
                        break

        if timeline_clip['audio']['path']:                
            for i in range(self.audio_list.count()):
                    audio_item = self.audio_list.item(i)
                    audio_item_data = audio_item.data(Qt.UserRole)

                    if audio_item_data and audio_item_data['id'] == timeline_clip['id']:
                        # basename = os.path.basename(timeline_clip['audio']['path'])
                        timeline_clip['audio']['duration'] = timeline_clip['audio']['clip'].duration
                        dur_min_base = timeline_clip['audio']['duration'] / 60
                        dur_min = round(dur_min_base, 2)
                        audio_item.setText(f'🎵 {timeline_clip['audio']['name']}: {dur_min} minutes')
                        break
                  
    def preview_project(self):
        if not self.editor.clips_build_list: # and not self.audio_clips:
            QMessageBox.warning(self, 'Preview', 'Add clips to timeline first')
            return
        
        self.status.setText('Rendering low-res proxy preview (30-60s)...')
        # self.play_btn.setEnabled(False)
        # QApplication.processEvents()

    # def export_project(self): # THIS WILL BE IN editor_engine.py
    #     if not self.video_clips and not self.audio_clips:
    #         QMessageBox.warning(self, 'Export', 'Add clips to timeline first')
    #         return
        
    #     dest, _ = QFileDialog.getSaveFileName(
    #         self, 'Export to MP4', '', 'MP4 files (*.mp4)'
    #     )
    #     if not dest:
    #         return
        
    #     res_text = self.res_combo.currentText()
    #     if '1920' in res_text:
    #         target = (1920, 1080)
    #         quality_note = 'Full HD (may take 10-15 min per minute on 2017 iMac)'
    #     elif '1280' in res_text:
    #         target = (1280, 720)
    #         quality_note = 'HD (may take 5-8 min per minute on 2017 iMac)'
    #     else:
    #         target = (640, 360)
    #         quality_note = 'Small (may take 2-3 min per minute on 2017 iMac)'
        
    #     self.status.setText(f'Exporting {quality_note}... But I\'m OP so it should be fine')
    #     self.export_btn.setEnabled(False)
    #     QApplication.processEvents()
        
    #     def export_task():
    #         try:
    #             pass
    #             # final = self._build_moviepy_clips(target_res=target)
    #             # final.write_videofile(
    #             #     dest, 
    #             #     codec='libx264', 
    #             #     audio_codec='aac', 
    #             #     fps=24,
    #             #     verbose=False,
    #             #     logger=None
    #             # )
    #             # self.render_finished.emit(dest, None)
    #         except Exception as e:
    #             pass
    #             # self.render_finished.emit('', e)
        
    #     self.render_thread = threading.Thread(target=export_task, daemon=True)
    #     self.render_thread.start()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            if obj == self.video_list:
                self.audio_list.clearSelection()
            elif obj == self.audio_list:
                self.video_list.clearSelection()
        return super().eventFilter(obj, event)

    # def video_list_selected(self):
    #     if self.video_list.selectedItems():
    #         self.audio_list.blockSignals(True)
    #         self.audio_list.clearSelection()
    #         self.audio_list.blockSignals(False)

    # def audio_list_selected(self):
    #     if self.audio_list.selectedItems():
    #         self.video_list.blockSignals(True)
    #         self.video_list.clearSelection()
    #         self.video_list.blockSignals(False)

    def new_version_popup(self, current_version, new_version):
        # Create the QMessageBox instance
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("A New Version Is Available")
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(f'A new version is available.<br><br>'
                        f'Current version: {current_version} → New Version: {new_version}.<br>'
                        f'Find it at:<br>'
                        f'<a href="https://github.com/CloudZero2049/CloudZero-Video-Editor/releases">'
                        f'https://github.com/CloudZero2049/CloudZero-Video-Editor/releases</a>')
        msg_box.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        
        # Set the standard buttons to just "OK"
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Set an icon (optional, e.g., Information, Warning, Critical)
        #msg_box.setIcon(QMessageBox.Icon.Information)

        font = QFont()
        font.setPointSize(12)
        msg_box.setFont(font)
        for label in msg_box.findChildren(QLabel):
            label.setWordWrap(True)
            #label.setFixedWidth(400)
            label.setMinimumWidth(500)
        # Execute the dialog and wait for the user to close it
        msg_box.exec()
        # Code execution continues here after the user clicks "OK"


    def radio_changed(self):
        r = self.sender()
        if r.isChecked():
            print(f"{r.text()} is checked")
        else:
            print(f"{r.text()} is unchecked")
    
    def radio_clicked(self):
        r = self.sender()
        print(f"{r.text()} was clicked")


    def show_choices(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Choose an option")
        msg_box.setText("Please select one of the following options:")

        c1 = msg_box.addButton("Choice A", QMessageBox.ActionRole)
        c2 = msg_box.addButton("Choice B", QMessageBox.ActionRole)
        c3 = msg_box.addButton("Choice C", QMessageBox.ActionRole)
        # choices = ["Choice A", "Choice B", "Choice C"]
        # choice, ok = QInputDialog.getItem(self, "Select Choice", "Choose an option:", choices, 0, False)
        msg_box.exec()

        if msg_box.clickedButton() == c1:
            print("User chose A")
        elif msg_box.clickedButton() == c2:
            print("User chose B")
        elif msg_box.clickedButton() == c3:
            print("User chose C")

    def new_window(self, tool_type):
        new_win = None
        match tool_type:
            case 'Extract':
                if self.extract_open == False:
                    self.extract_open = True
                    new_win = ExtractWindow(self, self.window_counter, self.editor, tool_type)
                else:
                    return
            case 'Cut_Out':
                if self.cut_out_open == False:
                    self.cut_out_open = True
                    new_win = CutOutWindow(self, self.window_counter, self.editor, tool_type)
                else:
                    return
            case 'Split':
                if self.split_open == False:
                    self.split_open = True
                    new_win = SplitWindow(self, self.window_counter, self.editor, tool_type)
                else:
                    return
            case 'Insert_Text':
                return
                if self.insert_text_open == False:
                    self.insert_text_open = True
                    return # new_win = Insert_Text_Window(self, self.window_counter, self.editor, tool_type)
                else:
                    return
            case 'Black_Fade':
                return
                if self.black_fade_open == False:
                    self.black_fade_open = True
                    return # new_win = BlackFadeWindow(self, self.window_counter, self.editor, tool_type)
                else:
                    return
            case 'Sound_Fade':
                return
                if self.sound_fade_open == False:
                    self.sound_fade_open = True
                    return # new_win = SoundFadeWindow(self, self.window_counter, self.editor, tool_type)
                else:
                    return
            case 'Volume':
                return
                if self.volume_open == False:
                    self.volume_open = True
                    return # new_win = VolumeWindow(self, self.window_counter, self.editor, tool_type)
                else:
                    return
            case 'Progress':
                # might need more windows with multi-threading
                new_win = ProgressWindow(self, self.window_counter)
            case 'Export':
                if self.export_open == False:
                    self.export_open = True
                    new_win = ExportWindow(self, self.window_counter)
                else:
                    return    
            case _: return
        
        if not new_win:
            print('something went wrong opening a window. new_win was false')
            # log
        self.windows.append(new_win)  # Keep a reference to prevent garbage collection
        #new_win.destroyed.connect(lambda: self.remove_window(new_win))

        new_win.setAttribute(Qt.WA_DeleteOnClose)
        
        new_win.destroyed.connect(lambda win_ref=new_win, title=new_win.windowTitle(): self.on_window_destroyed(win_ref, title))
        # new_win.destroyed.connect(lambda obj, title=new_win.windowTitle(): self.on_window_destroyed(obj, title))
        # new_win.destroyed.connect(self.on_window_destroyed)
        self.window_counter += 1
        new_win.show()
        return new_win

    def on_window_destroyed(self, win_ref, title):
        match title:
            case "Export Window": self.export_open = False
            case "Extract Window": self.extract_open = False
            case "Cut_Out Window": self.cut_out_open = False
            case "Split Window": self.split_open = False
            case "Insert_Text Window": self.insert_text_open = False
            case "Black_Fade Window": self.black_fade_open = False
            case "Sound_Fade Window": self.sound_fade_open = False
            case "Volume Window": self.volume_open = False

        self.windows = [w for w in self.windows if isValid(w)]
        # self.windows = [w for w in self.windows if w is not win_ref]

        # - != calls the object's __eq__ method to check value equality — it can trigger attribute access or other logic on the object, 
        # which crashes if the C++ side is deleted.
        # - is not compares Python object identity (memory address) only — no method calls, no attribute access, 
        # completely safe on dead wrapper objects.

        # new_win.destroyed.connect(lambda: self.on_window_destroyed(new_win.windowTitle()))
    # def remove_window(self, win):
    #     if win in self.windows:
    #         print(f"Window {win.win_num} removed from tracking list")
    #         # log
    #         self.windows.remove(win)
            

    def shutdown(self):
        print("Closing Main Window...")
        self.close()
    
        


def main():
    print("please use cloud_video_editor.py")
    

if __name__ == "__main__":
    main()
