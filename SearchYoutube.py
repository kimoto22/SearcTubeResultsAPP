import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import cv2
import numpy as np
import pyautogui
from pynput.mouse import Listener
import time
import csv
import os

class Config():
    def __init__(self):
        self.start_flag = 0
        self.stop_flag = 0
        self.fps = 15
        self.h, self.w = np.array(pyautogui.screenshot()).shape[:2]
        self.frame_queue = []
        self.output_folder = ""
        self.record_thread = None
        self.video_name = ""
        self.click_timestamps = []

class RecordThread(threading.Thread):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.stop_thread = threading.Event()

    def draw_red_dot(self, img, x, y, radius=5):
        red_color = (0, 0, 255)
        img = cv2.circle(img, (x, y), radius, red_color, -1)
        return img

    def get_mouse_position(self):
        last_capture_time = time.time()
        with Listener(on_click=self.on_click) as listener:
            while not self.stop_thread.is_set():
                current_time = time.time()
                if current_time - last_capture_time >= 1.0 / self.config.fps:
                    last_capture_time = current_time
                    img = pyautogui.screenshot()
                    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                    x, y = pyautogui.position()
                    img = self.draw_red_dot(img, x, y)
                    self.config.frame_queue.append(img)

    def on_click(self, x, y, button, pressed):
        if pressed:
            timestamp = time.time()
            microseconds = int((timestamp - int(timestamp)) * 1e6)
            timestamp_str = time.strftime("%H_%M_%S", time.localtime(timestamp)) + f"_{microseconds:06d}"
            self.config.click_timestamps.append(timestamp_str)

    def run(self):
        self.config.frame_queue = []
        self.get_mouse_position()

    def stop(self):
        self.stop_thread.set()

class CaptureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.config.record_thread = None

        self.title("Screen Capture")
        self.geometry("300x400")

        self.create_widgets()

    def create_widgets(self):
        self.csv_label = ttk.Label(self, text="Video/CSV Name:")
        self.csv_entry = ttk.Entry(self)
        self.start_button = ttk.Button(self, text="Start", command=self.record_start)
        self.stop_button = ttk.Button(self, text="Stop", command=self.record_stop)
        self.select_folder_button = ttk.Button(self, text="Select Folder", command=self.select_output_folder)
        self.output_folder_label = ttk.Label(self, text="Output Folder: ")

        self.csv_label.pack(pady=5)
        self.csv_entry.pack(pady=5)
        self.start_button.pack(pady=10)
        self.stop_button.pack(pady=10)
        self.select_folder_button.pack(pady=10)
        self.output_folder_label.pack(pady=10)

    def update_output_folder_label(self):
        if self.config.output_folder:
            self.output_folder_label.config(text=f"Output Folder: {self.config.output_folder}")
        else:
            self.output_folder_label.config(text="Output Folder: ")

    def record_start(self):
        if not self.config.output_folder:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        self.config.video_name = self.csv_entry.get() + ".mp4"

        if self.config.start_flag == 0:
            self.config.start_flag = 1
            self.config.record_thread = RecordThread(self.config)
            self.config.record_thread.start()

    def record_stop(self):
        if self.config.start_flag == 1:
            self.config.stop_flag = 1
            if self.config.record_thread is not None:
                self.config.record_thread.stop()
            self.record_save()
            self.update_output_folder_label()
            self.config.stop_flag = 0
            self.config.start_flag = 0
        else:
            messagebox.showerror("Error", "Please start recording first.")

    def record_save(self):
        save_path = os.path.join(self.config.output_folder, self.config.video_name)
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video = cv2.VideoWriter(save_path, fourcc, self.config.fps, (self.config.w, self.config.h))
        for frame in self.config.frame_queue:
            video.write(frame)
        video.release()
        messagebox.showinfo("Info", "Video saved successfully.")

        if self.config.click_timestamps:
            csv_file_path = os.path.join(self.config.output_folder, self.config.video_name.replace(".mp4", ".csv"))
            with open(csv_file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for timestamp in self.config.click_timestamps:
                    writer.writerow([timestamp])

    def select_output_folder(self):
        self.config.output_folder = filedialog.askdirectory()
        self.update_output_folder_label()

def main():
    app = CaptureApp()
    app.mainloop()

if __name__ == '__main__':
    main()
