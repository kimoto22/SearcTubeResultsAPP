import cv2
import os
from datetime import datetime, timedelta
import pandas as pd

# 対象者の名前
subject_name = "goto"

# 動画ファイルのパスを構築
file_path = f".\\SearcTubeResultsAPP\\subjects\\{subject_name}\\{subject_name}_PCカメラ映像.avi"
output_txt_path = f".\\SearcTubeResultsAPP\\sbjects\\{subject_name}\\{subject_name}_FrameTime.txt"
csv_file_path = f".\\SearcTubeResultsAPP\\subjects\\{subject_name}\\{subject_name}.csv"
csv_data = pd.read_csv(csv_file_path)


def output_HMS(time_str):
    time = datetime.strptime(time_str, "%H:%M:%S.%f")
    HMS_time = time.strftime("%H:%M:%S.%f")
    HMS_time_without_milliseconds = HMS_time.split(".")[0]
    return HMS_time_without_milliseconds


def read_csv(csv_data, frame_time):
    start_time_str = "15:39:42.127503"
    end_time_str = "15:43:31.916475"

    HMS_start_time = output_HMS(start_time_str)
    HMS_start_time = output_HMS(end_time_str)
    HMS_frame_time = output_HMS(frame_time)

    # Timestamp列の各アイテムを取り出す
    for index, timestamp_item in csv_data['Timestamp'].iteritems():
        HMS_timestamp = output_HMS(timestamp_item)

        print(HMS_start_time, HMS_timestamp, HMS_frame_time)

        if HMS_start_time == HMS_timestamp and HMS_start_time == HMS_frame_time:
            print(HMS_start_time)


def get_video_info(video_path):
    # OpenCVを使用して動画の情報を取得
    cap = cv2.VideoCapture(video_path)

    # 動画の総フレーム数を取得
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 動画のFPS（フレームレート）を取得
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 動画の総時間を計算
    total_seconds = total_frames / fps

    # 動画の作成時刻と終了時刻を計算
    creation_time = datetime.fromtimestamp(os.path.getctime(video_path))
    end_time = creation_time + timedelta(seconds=total_seconds)

    # フォーマットして表示
    print(f"動画作成時刻: {creation_time}")
    print(f"動画終了時刻: {end_time}")

    # キャプチャを解放
    cap.release()


def get_frame_times(video_path, output_txt_path):
    # OpenCVを使用して動画の情報を取得
    cap = cv2.VideoCapture(video_path)

    # 動画のFPS（フレームレート）を取得
    fps = cap.get(cv2.CAP_PROP_FPS)

    # ファイルを書き込みモードで開く
    with open(output_txt_path, 'w') as file:
        # 各フレームの時刻を取得して書き込む
        for frame_number in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
            # フレーム番号から時刻を計算
            current_time = datetime.fromtimestamp(os.path.getctime(video_path))
            frame_time = current_time + timedelta(seconds=frame_number / fps)
            read_csv(csv_data, frame_time)

            # フォーマットして書き込み
            file.write(f"Frame {frame_number + 1}: {frame_time}\n")

    # キャプチャを解放
    cap.release()


# 動画の情報を表示
get_video_info(file_path)
# 動画の各フレームの時刻をテキストファイルに出力
get_frame_times(file_path, output_txt_path)
