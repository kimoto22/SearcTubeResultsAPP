import cv2
import numpy as np
import pyautogui
from pynput.mouse import Listener
import time
import os
import threading
import pandas as pd

class Camera:
    def __init__(self):
        self.start_flag = 0
        self.stop_flag = 0
        self.fps = 15
        self.h, self.w = np.array(pyautogui.screenshot()).shape[:2]
        self.frame_queue = []
        self.output_folder = ""
        self.record_thread = None
        self.video_name = ""
        self.csv_name = ""
        self.click_timestamps = []

    def draw_red_dot(self, img, x, y, radius=5):
        red_color = (0, 0, 255)
        img = cv2.circle(img, (x, y), radius, red_color, -1)
        return img

    def get_mouse_position(self):
        last_capture_time = time.time()
        with Listener(on_click=self.on_click) as listener:
            while not self.stop_flag:
                current_time = time.time()
                if current_time - last_capture_time >= 1.0 / self.fps:
                    last_capture_time = current_time
                    img = pyautogui.screenshot()
                    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                    x, y = pyautogui.position()
                    img = self.draw_red_dot(img, x, y)

                    # クリック回数をテキストでフレームに描画
                    click_count_text = f"Clicks: {len(self.click_timestamps)}"
                    cv2.putText(img, click_count_text, (self.w - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    self.frame_queue.append(img)

                    if self.video_writer is not None:
                        self.video_writer.write(img)  # ビデオにフレームを書き込む

    def on_click(self, x, y, button, pressed):
        if pressed:
            timestamp = time.time()
            microseconds = int((timestamp - int(timestamp)) * 1e6)
            timestamp_str = time.strftime("%H:%M:%S", time.localtime(timestamp)) + f".{microseconds:06d}"
            self.click_timestamps.append(timestamp_str)

    def save_click_timestamps(self):
        if self.click_timestamps and self.csv_name:
            csv_file_path = os.path.join(self.output_folder, self.csv_name + ".csv")
            df = pd.DataFrame({'Timestamp': self.click_timestamps})
            df.to_csv(csv_file_path, index=False)

    def record(self):
        self.frame_queue = []
        save_path = os.path.join(self.output_folder, self.video_name)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(save_path, fourcc, self.fps, (self.w, self.h))
        self.get_mouse_position()
        self.video_writer.release()
        self.save_click_timestamps()
