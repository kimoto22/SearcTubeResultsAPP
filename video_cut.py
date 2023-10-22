import cv2
import os
from datetime import datetime, timedelta
import pandas as pd

# 対象者の名前
subject_name = "goto"

mode_name = "集中"

# 動画ファイルのパスを構築
input_video_path = f".\\subjects\\{subject_name}\\{subject_name}_PCカメラ映像.avi"
output_video_path = f".\\subjects\\{subject_name}\\{subject_name}_{mode_name}.avi"
output_txt_path = f".\\subjects\\{subject_name}\\{subject_name}_TimeStamp.txt"
csv_file_path = f".\\subjects\\{subject_name}\\{subject_name}.csv"
csv_data = pd.read_csv(csv_file_path)

GetFrameFlg = False

start_time_str = "15:39:42.127503"
end_time_str = "15:43:31.916475"

def output_HMS(time_str):
    try:
        time = datetime.strptime(time_str, "%H:%M:%S.%f")
        HMS_time = time.strftime("%H:%M:%S.%f")
        HMS_time_without_milliseconds = HMS_time.split(".")[0]
    except:
        HMS_time = time_str.strftime("%H:%M:%S.%f")
        HMS_time_without_milliseconds = HMS_time.split(".")[0]
    return HMS_time_without_milliseconds

def count_time_list(start_time_str, end_time_str):
    start_time = datetime.strptime(start_time_str, "%H:%M:%S.%f")
    end_time = datetime.strptime(end_time_str, "%H:%M:%S.%f")
    # 1秒ごとの時間リストを作成
    time_list = []
    current_time = start_time
    while current_time <= end_time:
        time_list.append(output_HMS(current_time))
        current_time += timedelta(seconds=1)
    return time_list


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

            # フォーマットして書き込み
            file.write(f"Frame {frame_number + 1}: {frame_time}\n")

    # キャプチャを解放
    cap.release()


def extract_frames(input_video_path, output_video_path, start_frame, end_frame):
    # 動画ファイルを読み込む
    cap = cv2.VideoCapture(input_video_path)

    # 出力動画の設定
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_size = int(cap.get(3)), int(cap.get(4))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

    for frame_number in range(start_frame, end_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)  # 切り出すフレームに移動
        ret, frame = cap.read()  # フレームを読み込む
        if not ret:
            break
        out.write(frame)  # フレームを出力動画に書き込む

# 動画の情報を表示
get_video_info(input_video_path)
# 動画の各フレームの時刻をテキストファイルに出力
get_frame_times(input_video_path, output_txt_path)

