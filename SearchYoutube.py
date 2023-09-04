import tkinter as tk
from tkinter import ttk, filedialog
import threading
import cv2
import numpy as np
import pyautogui

class Config():
    def __init__(self):
        self.start_flag = 0
        self.stop_flag = 0
        self.fps = 15
        self.m_time = 10
        self.h, self.w = np.array(pyautogui.screenshot()).shape[:2]
        self.frame_queue = []
        self.output_folder = ""

class RecordThread():
    def __init__(self, config):
        self.config = config

    def loop(self):
        self.config.frame_queue = []
        while self.config.stop_flag != 1:
            img = pyautogui.screenshot()
            img = np.array(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            self.config.frame_queue.append(img)

class CaptureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config = Config()

        self.title("Screen Capture")
        self.geometry("300x150")

        self.create_widgets()

    def create_widgets(self):
        self.start_button = ttk.Button(self, text="Start", command=self.record_start)
        self.stop_button = ttk.Button(self, text="Stop", command=self.record_stop)
        self.select_folder_button = ttk.Button(self, text="Select Folder", command=self.select_output_folder)
        self.output_folder_label = ttk.Label(self, text="Output Folder: ")

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
            tk.messagebox.showerror("Error", "Please select an output folder.")
            return

        if self.config.start_flag == 0:
            self.config.start_flag = 1
            self.record_thread = threading.Thread(target=self.record_control)
            self.record_thread.start()

    def record_stop(self):
        if self.config.start_flag == 1:
            self.config.stop_flag = 1
            self.record_thread.join()
            self.record_save()
            self.update_output_folder_label()
            self.config.stop_flag = 0
            self.config.start_flag = 0
        else:
            tk.messagebox.showerror("Error", "Please start recording first.")

    def record_control(self):
        rec = RecordThread(self.config)
        rec.loop()

    def record_save(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if save_path:
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            video = cv2.VideoWriter(save_path, fourcc, self.config.fps, (self.config.w, self.config.h))
            for frame in self.config.frame_queue:
                video.write(frame)
            video.release()
            tk.messagebox.showinfo("Info", "Video saved successfully.")

    def select_output_folder(self):
        self.config.output_folder = filedialog.askdirectory()
        self.update_output_folder_label()

def main():
    app = CaptureApp()
    app.mainloop()

if __name__ == '__main__':
    main()
