import os
from moviepy import *
from PySide6.QtCore import Qt, QThread, QObject, Signal
from PySide6.QtWidgets import QListWidgetItem
from proglog import ProgressBarLogger
import time

VERSION = "0.1.5"

class EditorEngine:
    def __init__(self):
        self.main_window = None
        self.id_counter = 0
        self.timeline = []
#    clip_data = {
#                 'id': self.editor.id_counter,
#                 'video': {'path': path,'clip': VideoFileClip(path), 'width': 0, 'height': 0, 'size': (0,0), 'fps': 30,'duration': 0},
#                 'audio': {'path': None,'clip': None, 'duration': 0},
#                 'vfx': [],
#                 'afx': []
#             }
        self.clips_build_list = []

    # Editing
    def copy_clip(self):
        pass
    def paste_clip(self):
        pass
    def extract_clip(self, window, main_window, clip_from, clip_to):
        timeline_clip, type = main_window.get_timeline_clip()

        if not timeline_clip:
            main_window.status.setText(f'please select a clip to extract')
            return
        
        if not clip_from and not clip_to:
            print('Error: No time frame set for extract')
            main_window.status.setText(f'please type in a start time and/or an end time')
            return
        
        if type == 'video':
            timeline_clip['video']['clip'] = timeline_clip['video']['clip'].subclipped(clip_from, clip_to)
        else:
            timeline_clip['audio']['clip'] = timeline_clip['audio']['clip'].subclipped(clip_from, clip_to)

        main_window.update_duration(timeline_clip)
        main_window.update_export_size_check(None)
        # if auto_close_windows:
        #   window.close()
        

    def cut_out_clip(self, window, main_window, clip_from, clip_to):
        timeline_clip, type = main_window.get_timeline_clip()
        if not timeline_clip:
            main_window.status.setText(f'please select a clip to cut-out')
            return
        
        if not clip_from and not clip_to:
            print('Error: No time frame set for cut-out')
            main_window.status.setText(f'please type in a start time and/or an end time')
            return
        if type == 'video': # all_clips[-3] = all_clips[-3].with_section_cut_out(start_time=4, end_time=8)
            timeline_clip['video']['clip'] = timeline_clip['video']['clip'].with_section_cut_out(clip_from, clip_to)
        else:
            timeline_clip['audio']['clip'] = timeline_clip['audio']['clip'].with_section_cut_out(clip_from, clip_to)
        main_window.update_duration(timeline_clip)
        main_window.update_export_size_check(None)
        # window.close()
    # if video:
    # 1) Create video data for clip-B
    # 2) modify video data for clip-A
    # 3) Add video clip-B
    # else: Audio only -->
    # if audio:
    # 4) Create audio data for clip-B
    # 5) modify audio data for clip-A
    # 6) Add audio clip-B
    # else: <-- From Video

    def split_clip(self, window, main_window, split_time):
        timeline_clip, type = main_window.get_timeline_clip()
        if not timeline_clip:
            main_window.status.setText(f'please select a clip to split')
            return
        
        if not split_time:
            print('Error: No split time set for split')
            main_window.status.setText(f'please type in a split time')
            return

        #--------------------------
        # Creating split clip
        #--------------------------
        clip_B_data = {
                'id': self.id_counter,
                'video': {'path': None,'clip': None,'name': None, 'width': 0, 'height': 0, 'size': [0,0], 'fps': 30,'duration': 0},
                'audio': {'path': None,'clip': None, 'name': None,'duration': 0},
                'vfx': [],
                'afx': []
            }
        self.id_counter += 1
        
        row = None
        for i in range(main_window.video_list.count()):
            item = main_window.video_list.item(i)
            item_data = item.data(Qt.UserRole)
            if item_data and item_data['id'] == timeline_clip['id']:
                row = i

        video_list_item_A = main_window.video_list.item(row)
        audio_list_item_A = main_window.audio_list.item(row)

        if timeline_clip['video']['path']:
            clip_BV_path = timeline_clip['video']['path']
            clip_BV_clip = timeline_clip['video']['clip'].subclipped(split_time)
            clip_BV_name = timeline_clip['video']['name'] + '-B'
            # Entering clip-B video data
            clip_B_data['video'] = {'path': clip_BV_path,'clip': clip_BV_clip,'name': clip_BV_name, 'width': 0, 'height': 0, 'size': [0,0], 'fps': 30,'duration': 0}
            clip_B_data['video']['width'] = clip_B_data['video']['clip'].w
            clip_B_data['video']['height'] = clip_B_data['video']['clip'].h
            clip_B_data['video']['size'] = clip_B_data['video']['clip'].size
            clip_B_data['video']['fps'] = clip_B_data['video']['clip'].fps
            clip_B_data['video']['duration'] = clip_B_data['video']['clip'].duration

            #--------------------------
            # Modifying Original Video
            #--------------------------
            timeline_clip['video']['clip'] = timeline_clip['video']['clip'].subclipped(0, split_time)
            timeline_clip['video']['name'] = timeline_clip['video']['name'] + '-A'
            timeline_clip['video']['size'] = timeline_clip['video']['clip'].size
            timeline_clip['video']['duration'] = timeline_clip['video']['clip'].duration
            dur_min_base = timeline_clip['video']['duration'] / 60
            dur_min = round(dur_min_base, 2)
            size_info = f'{timeline_clip["video"]["width"]}x{timeline_clip["video"]["height"]}, ' if {timeline_clip["video"]["path"]} else ""
            video_list_item_A.setData(Qt.UserRole, timeline_clip)
            video_list_item_A.setText(f'🎬 {timeline_clip['video']['name']}: {size_info}{dur_min} minutes')
            #--------------------------
            # Adding Split Video
            #--------------------------
            dur_min_base = clip_B_data['video']['duration'] / 60
            dur_min = round(dur_min_base, 2)
            size_info = f'{clip_B_data["video"]["width"]}x{clip_B_data["video"]["height"]}, ' if {clip_B_data["video"]["path"]} else ""

            video_list_item_B = QListWidgetItem(f'🎬 {clip_BV_name}: {size_info}{dur_min} minutes')
            video_list_item_B.setData(Qt.UserRole, clip_B_data)
            main_window.video_list.insertItem((row + 1), video_list_item_B)
            # main_window.video_list.addItem(video_list_item_B)
            
        else:
            video_list_item_B = QListWidgetItem(f'*Audio Only* -->')
            video_list_item_B.setData(Qt.UserRole, clip_B_data)
            main_window.video_list.insertItem((row + 1), video_list_item_B)
            # self.video_list.addItem(video_list_item_B)

        if timeline_clip['audio']['path']:
            clip_BA_path = timeline_clip['audio']['path']
            clip_BA_clip = timeline_clip['audio']['clip'].subclipped(split_time)
            clip_BA_name = timeline_clip['audio']['name'] + '-B'
            # Entering Audio data
            clip_B_data['audio']= {'path': clip_BA_path,'clip': clip_BA_clip, 'name': clip_BA_name, 'duration': 0}
            clip_B_data['audio']['duration'] = clip_B_data['audio']['clip'].duration
            
            
            #--------------------------
            # Modifying Original Audio
            #--------------------------
            timeline_clip['audio']['clip'] = timeline_clip['audio']['clip'].subclipped(0, split_time)
            timeline_clip['audio']['name'] = timeline_clip['audio']['name'] + '-A'
            timeline_clip['audio']['duration'] = timeline_clip['audio']['clip'].duration
            dur_min_base = timeline_clip['audio']['duration'] / 60
            dur_min = round(dur_min_base, 2)
        
            audio_list_item_A.setData(Qt.UserRole, timeline_clip)
            audio_list_item_A.setText(f'🎬 {timeline_clip['audio']['name']}: {dur_min} minutes')
            #--------------------------
            # Adding Split Audio
            #--------------------------
            dur_min_base = clip_B_data['audio']['duration'] / 60
            dur_min = round(dur_min_base, 2)
            audio_list_item_B = QListWidgetItem(f"🎵 {clip_BA_name}: {dur_min} minutes")
            audio_list_item_B.setData(Qt.UserRole, clip_B_data)
            main_window.audio_list.insertItem((row + 1), audio_list_item_B)
            # self.audio_list.addItem(audio_list_item_B)
            
            
        else:
            audio_list_item_B = QListWidgetItem(f'<-- *From Video Clip*')
            audio_list_item_B.setData(Qt.UserRole, clip_B_data)
            main_window.audio_list.insertItem((row + 1), audio_list_item_B)    
            # main_window.audio_list.addItem(audio_list_item_B)

        main_window.update_duration(timeline_clip)
        
        
        # Find the index on editor timeline
        index = self.timeline.index(timeline_clip)
        # Insert after clip index
        self.timeline.insert((index + 1), clip_B_data)
    
        main_window.update_export_size_check(None)
        # window.close()
        
    def insert_text_frame(self):
        pass
    def insert_black_fade(self):
        pass
    def insert_sound_fade(self):
        pass
    def edit_volume(self):
        pass
    

    def export(self, main_window, res_text, export_dest):
        # Create folder if it doesn't exist
        output_dir = os.path.dirname(export_dest)
        if output_dir:  # avoid empty string if no directory in path
            # exist_ok=True means it won't raise an error if the folder already exists, so no need for a manual check first. 
            os.makedirs(output_dir, exist_ok=True)
        
        export_start_time = time.time()
        prog_window = main_window.new_window('Progress')
         
        self.clips_build_list.clear()
        size = [1280, 720]
        match res_text:
            case '640x360': size = [640, 360]
            case '1280x720': size = [1280, 720]
            case '1920x1080': size = [1920, 1080]
            case _: 
                print("an error occurated setting resolution")
                return
        # size should look like [1920,1080]
        width = size[0]
        height = size[1]
        for item in self.timeline:
            # Apply sound override
            if item['video']['clip'] and item['audio']['clip'] is not None:
                item['audio']['clip'] = item['audio']['clip'].with_duration(item['video']['duration'])
                item['video']['clip'] = item['video']['clip'].with_audio(item['audio']['clip'])
        
            # Check resolution resizing
            if item['video']['width'] != width and item['video']['height'] != height:
                self.clips_build_list.append(item['video']['clip'].resized(new_size=size).with_position(("center", "center")))
            elif item['video']['width'] != width:
                self.clips_build_list.append(item['video']['clip'].resized(width=width).with_position(("center", "center")))
            elif item['video']['height'] != height:
                self.clips_build_list.append(item['video']['clip'].resized(height=height).with_position(("center", "center")))
            else:
                self.clips_build_list.append(item['video']['clip'])


        composite_video = concatenate_videoclips(self.clips_build_list, method="chain", transition=None)
        avg_factor = 1
        found_timings = False
        matched_size = main_window.update_export_size_check(None) # False if needs resizing
        if matched_size:
            match res_text:
                case '640x360':
                    if len(self.main_window.master.low_timings_max) > 0:
                        # reduce the timings list if it's more than max_timings
                        if len(self.main_window.master.low_timings_max) >= self.main_window.master.max_timings:
                            self.main_window.master.low_timings_max = self.main_window.master.low_timings_max[-self.main_window.master.max_timings:]
                        avg_factor = sum(self.main_window.master.low_timings_max) / len(self.main_window.master.low_timings_max)
                        found_timings = True
                case '1280x720':
                    if len(self.main_window.master.mid_timings_max) > 0:
                        if len(self.main_window.master.mid_timings_max) >= self.main_window.master.max_timings:
                            self.main_window.master.mid_timings_max = self.main_window.master.mid_timings_max[-self.main_window.master.max_timings:]
                        avg_factor = sum(self.main_window.master.mid_timings_max) / len(self.main_window.master.mid_timings_max)
                        found_timings = True
                case '1920x1080':
                    if len(self.main_window.master.high_timings_max) > 0:
                        if len(self.main_window.master.high_timings_max) >= self.main_window.master.max_timings:
                            self.main_window.master.high_timings_max = self.main_window.master.high_timings_max[-self.main_window.master.max_timings:]
                        avg_factor = sum(self.main_window.master.high_timings_max) / len(self.main_window.master.high_timings_max)
                        found_timings = True
                case _: 
                    print("an error occurated setting time estimation (timings_max)")
                    return
        else:
            match res_text:
                case '640x360':
                    if len(self.main_window.master.low_timings) > 0:
                        # reduce the timings list if it's more than max_timings
                        if len(self.main_window.master.low_timings) >= self.main_window.master.max_timings:
                            self.main_window.master.low_timings = self.main_window.master.low_timings[-self.main_window.master.max_timings:]
                        avg_factor = sum(self.main_window.master.low_timings) / len(self.main_window.master.low_timings)
                        found_timings = True
                case '1280x720':
                    if len(self.main_window.master.mid_timings) > 0:
                        if len(self.main_window.master.mid_timings) >= self.main_window.master.max_timings:
                            self.main_window.master.mid_timings = self.main_window.master.mid_timings[-self.main_window.master.max_timings:]
                        avg_factor = sum(self.main_window.master.mid_timings) / len(self.main_window.master.mid_timings)
                        found_timings = True
                case '1920x1080':
                    if len(self.main_window.master.high_timings) > 0:
                        if len(self.main_window.master.high_timings) >= self.main_window.master.max_timings:
                            self.main_window.master.high_timings = self.main_window.master.high_timings[-self.main_window.master.max_timings:]
                        avg_factor = sum(self.main_window.master.high_timings) / len(self.main_window.master.high_timings)
                        found_timings = True
                case _: 
                    print("an error occurated setting time estimation")
                    return

        if found_timings:
            estimated_base_time = composite_video.duration / avg_factor
            est_dur_min_base = estimated_base_time / 60
            est_dur_min = round(est_dur_min_base, 2)
            prog_window.time_estimate_label.setText(f'Estimated time: {est_dur_min} minutes')
        

        comp_dur_min_base = composite_video.duration / 60
        comp_dur_min = round(comp_dur_min_base, 2)
        prog_window.progress_bar.setValue(0)
        prog_window.progress_bar.show()

        self.thread = RenderThread(composite_video, export_dest)

        # Connect thread signal to GUI
        self.thread.progress.connect(prog_window.progress_bar.setValue)
        self.thread.status.connect(prog_window.status_label.setText)
        self.thread.render_finished.connect(lambda: self.on_export_finished(prog_window, composite_video, res_text, matched_size, export_start_time, comp_dur_min, composite_video.duration))
        
        self.thread.start()

    def on_export_finished(self, prog_window, composite_video, res_text, matched_size, export_start_time, comp_dur_min, base_dur): # (self, path, err)
        prog_window.progress_bar.setValue(100)
        prog_window.close()

        # This causes the need to rebuild clips
        # for clip in self.clips_build_list:
        #             clip.close()
        self.clips_build_list.clear()

        composite_video.close()

        self.main_window.status.setText('Export Successful')
        base_export_time = time.time() - export_start_time
        export_min_base = base_export_time / 60
        export_min = round(export_min_base, 2)

        time_factor = base_dur / base_export_time

        if matched_size: # True if did not need resizing
            match res_text:
                case '640x360':
                    if len(self.main_window.master.low_timings_max) >= self.main_window.master.max_timings:
                        self.main_window.master.low_timings_max.pop(0)
                    self.main_window.master.low_timings_max.append(time_factor)
                    self.main_window.master.save_settings()
                case '1280x720':
                    if len(self.main_window.master.mid_timings_max) >= self.main_window.master.max_timings:
                        self.main_window.master.mid_timings_max.pop(0)
                    self.main_window.master.mid_timings_max.append(time_factor)
                    self.main_window.master.save_settings()
                case '1920x1080':
                    if len(self.main_window.master.high_timings_max) >= self.main_window.master.max_timings:
                        self.main_window.master.high_timings_max.pop(0)
                    self.main_window.master.high_timings_max.append(time_factor)
                    self.main_window.master.save_settings()
                case _: 
                    print("an error occurated setting time estimation")
                    return
        else: # False, needed resizing
            match res_text:
                case '640x360':
                    if len(self.main_window.master.low_timings) >= self.main_window.master.max_timings:
                        self.main_window.master.low_timings.pop(0)
                    self.main_window.master.low_timings.append(time_factor)
                    self.main_window.master.save_settings()
                case '1280x720':
                    if len(self.main_window.master.mid_timings) >= self.main_window.master.max_timings:
                        self.main_window.master.mid_timings.pop(0)
                    self.main_window.master.mid_timings.append(time_factor)
                    self.main_window.master.save_settings()
                case '1920x1080':
                    if len(self.main_window.master.high_timings) >= self.main_window.master.max_timings:
                        self.main_window.master.high_timings.pop(0)
                    self.main_window.master.high_timings.append(time_factor)
                    self.main_window.master.save_settings()
                case _: 
                    print("an error occurated setting time estimation")
                    return
            
        print(f'Video rendering time: {export_min} minutes')
        print(f'Combined video duration: {comp_dur_min} minutes')
        # self.export_btn.setEnabled(True)
        # if err:
        #     QMessageBox.critical(
        #         self, 'Export Error', f'Failed:\n{str(err)}'
        #     )
        #     self.status.setText('Export failed')
        # else:
        #     QMessageBox.information(
        #         self, 'Export Complete', f'Video saved to:\n{path}'
        #     )
        #     self.status.setText('Export complete')

    
    def shutdown(self):
        print("Shutting down editor engine...")

        for clip in self.timeline:
            if clip['video']['clip']:
                clip['video']['clip'].close()

            if clip['audio']['clip']:
                clip['audio']['clip'].close()

        # for clip in self.clips_build_list:
        #     if clip and clip['video']['clip']:
        #         clip['video']['clip'].close()

        #     if clip and clip['audio']['clip']:
        #         clip['audio']['clip'].close()

        self.timeline.clear()

class QtLogger(QObject, ProgressBarLogger):
    progress_changed = Signal(int) # percent 0..100
    status_changed = Signal(str)

    def __init__(self):
        QObject.__init__(self)
        ProgressBarLogger.__init__(self)

    def callback(self, **changes):
        super().callback(**changes)

        message = changes.get("message")
        if message:
            if "audio" in message.lower():
                self.status_changed.emit("Rendering audio...")
            elif "video" in message.lower():
                self.status_changed.emit("Rendering video...")
            elif "done" in message.lower():
                self.status_changed.emit("Finalizing...")

    def bars_callback(self, bar, attr, value, old_value=None):
        # total = self.bars.get(bar, {}).get("total")

        # if total and total > 0:
        #     percent = int((value / total) * 100)

        #     # Optional: Only show video bar progress
        #     if bar == "t":
        #         self.progress_changed.emit(percent)
        #--------------------------------------------------------
        # bar is usually 't' (time) for video-writing; attr may be 'index' or direct value
        # protect against division by zero and missing 'total'
        try:
            total = self.bars[bar].get('total', None)
        except Exception:
            total = None

        # debug: print every bar callback so you can inspect what is sent
        # print("bars_callback:", {"bar": bar, "attr": attr, "value": value, "total": total})

        if total:
            # In practice `value` or self.bars[bar]['index'] will be the current index/time
            # compute percent using the stored total
            percent = int((value / total) * 100) if total and total > 0 else 0

            # optional: only report when actually writing video (filter by last_message)
            # if 'Writing video' in self.last_message:
            self.progress_changed.emit(max(0, min(100, percent)))

# WORKS
# class QtLogger(QObject, ProgressBarLogger):
#     progress_changed = Signal(int)  # percent 0..100

#     def __init__(self):
#         QObject.__init__(self)
#         ProgressBarLogger.__init__(self)
#         self.last_message = ""   # optional: track the last textual message

#     # called for textual/message updates (often you saw {} here)
#     def callback(self, **changes):
#         # keep internal state updated
#         super().callback(**changes)
#         # optional debugging: log non-empty changes
#         if changes:
#             print("callback changes:", changes)
#         # if MoviePy writes human-readable messages like "Writing video", store them:
#         for (k, v) in changes.items():
#             if isinstance(v, str):
#                 self.last_message = v

#     # called on bar updates (index/total etc.)
#     def bars_callback(self, bar, attr, value, old_value=None):
#         # bar is usually 't' (time) for video-writing; attr may be 'index' or direct value
#         # protect against division by zero and missing 'total'
#         try:
#             total = self.bars[bar].get('total', None)
#         except Exception:
#             total = None

#         # debug: print every bar callback so you can inspect what is sent
#         print("bars_callback:", {"bar": bar, "attr": attr, "value": value, "total": total})

#         if total:
#             # In practice `value` or self.bars[bar]['index'] will be the current index/time
#             # compute percent using the stored total
#             percent = int((value / total) * 100) if total and total > 0 else 0

#             # optional: only report when actually writing video (filter by last_message)
#             # if 'Writing video' in self.last_message:
#             self.progress_changed.emit(max(0, min(100, percent)))

class RenderThread(QThread):
    progress = Signal(int)
    status = Signal(str)
    render_finished = Signal()

    def __init__(self, clip, export_dest, parent=None):
        super().__init__(parent)
        self.clip = clip
        self.export_dest = export_dest

    def run(self):
        logger = QtLogger()

        logger.progress_changed.connect(self.progress.emit)
        logger.status_changed.connect(self.status.emit)

        self.clip.write_videofile(
            self.export_dest,
            logger=logger
        )

        self.render_finished.emit()

# WORKS
# class RenderThread(QThread):
#     progress = Signal(int)
#     render_finished = Signal()

#     def __init__(self, clip):
#         super().__init__()
#         self.clip = clip

#     def run(self):
#         logger = QtLogger()
#         logger.progress_changed.connect(self.progress.emit)

#         self.clip.write_videofile(
#             "output/combined_video.mp4",
#             logger=logger
#         )

#         # Fires when rendering is done
#         self.render_finished.emit()



def main():
    print("please use cloud_video_editor.py")
    
if __name__ == "__main__":
    main()