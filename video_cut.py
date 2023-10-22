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
output_csv_path = f".\\subjects\\{subject_name}\\{subject_name}_TimeStamp.csv"
csv_file_path = f".\\subjects\\{subject_name}\\{subject_name}.csv"
csv_data = pd.read_csv(csv_file_path)

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

def save_frame_times_to_csv(video_path, output_csv_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_times = []

    for frame_number in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        current_time = datetime.fromtimestamp(os.path.getctime(video_path))
        frame_time = current_time + timedelta(seconds=frame_number / fps)
        frame_times.append({'frame': frame_number + 1, 'time': output_HMS(frame_time)})

    df = pd.DataFrame(frame_times)
    df.to_csv(output_csv_path, index=False)

    cap.release()


def extract_frame_at_time(csv_path, target_time:str):
    df = pd.read_csv(csv_path)
    # 条件に一致する行を抽出
    filtered_df = df[df['time'] == target_time]

    # frame列を数値として扱うために文字列を整数に変換
    filtered_df['frame'] = filtered_df['frame'].astype(int)

    # frame列でソートし、最小のframe値を取得
    nearest_frame = filtered_df.sort_values(by='frame').iloc[0]['frame']

    return nearest_frame


def extract_frames(input_video_path, output_video_path, start_frame, end_frame):
    # 動画ファイルを読み込む
    cap = cv2.VideoCapture(input_video_path)

    # 出力動画の設定
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_size = int(cap.get(3)), int(cap.get(4))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)
    print("動画の切り取りが始まりました")
    for frame_number in range(start_frame, end_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)  # 切り出すフレームに移動
        ret, frame = cap.read()  # フレームを読み込む
        print("現在書き込んでいるframe:", frame_number)
        if not ret:
            break
        out.write(frame)  # フレームを出力動画に書き込む
    print("動画の切り取りが終わりました")

# 動画の情報を表示
get_video_info(input_video_path)
# 動画の各フレームの時刻をcsvファイルに出力
save_frame_times_to_csv(input_video_path, output_csv_path)

# 動画の各フレームのstarttime,　endtimeのframe_numberを抜き出し
start_frame = extract_frame_at_time(output_csv_path, output_HMS(start_time_str))
end_frame = extract_frame_at_time(output_csv_path, output_HMS(end_time_str))
print(start_frame, end_frame)

# 動画切り取り
extract_frames(input_video_path, output_video_path, start_frame, end_frame)