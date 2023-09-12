# main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os

# Capture
from capture import Capture

class CaptureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config = Capture()  # Captureクラスのインスタンスを作成

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
        self.config.csv_name = self.csv_entry.get()  # CSVファイル名を設定

        if self.config.start_flag == 0:
            self.config.start_flag = 1
            self.config.record_thread = threading.Thread(target=self.config.record)
            self.config.record_thread.start()
        
            # カメラキャプチャを開始
            self.config.camera_thread = threading.Thread(target=self.config.capture_frames, args=(self.csv_entry.get(),))  # 引数を追加
            self.config.camera_thread.start()

    def record_stop(self):
        if self.config.start_flag == 1:
            self.config.stop_flag = 1
            if self.config.record_thread is not None:
                self.config.record_thread.join()
                self.config.camera_thread.join()
                
            self.update_output_folder_label()
            self.config.stop_flag = 0
            self.config.start_flag = 0
        else:
            messagebox.showerror("Error", "Please start recording first.")

    def select_output_folder(self):
        self.config.output_folder = filedialog.askdirectory()
        self.update_output_folder_label()

def main():
    app = CaptureApp()
    app.mainloop()

if __name__ == '__main__':
    main()
