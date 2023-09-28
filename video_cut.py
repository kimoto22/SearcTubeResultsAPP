import pandas as pd
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from datetime import datetime, timedelta

def get_video_creation_time(video_path):
    # ビデオファイルの作成時刻を取得
    created_time = os.path.getctime(video_path)
    return datetime.fromtimestamp(created_time)

def cut_video_by_timestamp(csv_file, video_path, output_file, start_timestamp, end_timestamp):
    # pandas を使用してタイムスタンプが含まれる CSV ファイルを開く
    timestamp_data = pd.read_csv(csv_file)

    # タイムスタンプ文字列を datetime オブジェクトに変換
    timestamp_data['Timestamp'] = pd.to_datetime(timestamp_data['Timestamp'])

    # ビデオの切り取りのための開始および終了時間を取得
    start_time = start_timestamp
    end_time = end_timestamp

    # ビデオの作成時刻を取得
    video_creation_time = get_video_creation_time(video_path)

    # ビデオ作成時刻に基づいて開始および終了時間を調整
    start_time = (start_time - video_creation_time).total_seconds()
    end_time = (end_time - video_creation_time).total_seconds()

    # ビデオファイルを開く
    video_clip = VideoFileClip(video_path)

    # 指定されたタイムスタンプでビデオを切り取る
    cut_video_clip = video_clip.subclip(start_time, end_time)

    # 新しいファイルに切り取られたビデオを書き込む
    cut_video_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    # ビデオクリップオブジェクトを閉じる
    video_clip.close()
    cut_video_clip.close()

# 例：タイムスタンプの範囲を指定
start_timestamp = pd.Timestamp("15:43:37.687518")
end_timestamp = pd.Timestamp("15:43:40.136235")

# 対象者の名前
subject_name = "goto"

# 切り取られたビデオファイルの名前
cut_video_name = "focus"

# CSV タイムスタンプログファイルとビデオファイルを指定
csv_file = f".\\SearcTubeResultsAPP\\{subject_name}\\{subject_name}.csv"
video_path = f".\\SearcTubeResultsAPP\\{subject_name}\\{subject_name}_PCカメラ映像.avi"
output_file = f".\\SearcTubeResultsAPP\\{subject_name}\\{subject_name}_{cut_video_name}.avi"

# 切り取りを実行
cut_video_by_timestamp(csv_file, video_path, output_file, start_timestamp, end_timestamp)
