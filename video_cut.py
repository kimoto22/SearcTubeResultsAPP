from moviepy.editor import VideoFileClip
import cv2
import datetime

# 対象者の名前
subject_name = "goto"

# 切り取られたビデオファイルの名前
cut_video_name = "NotFocus"

# CSV タイムスタンプログファイルとビデオファイルを指定
input_video_path = f".\\SearcTubeResultsAPP\\{subject_name}\\{subject_name}_PCカメラ映像.avi"
output_video_path = f".\\SearcTubeResultsAPP\\{subject_name}\\{subject_name}_{cut_video_name}.mp4"

# 手動で指定する開始時刻と終了時刻
start_time_str = '15:43:43'
end_time_str = '15:46:50'

# 時刻文字列をdatetimeオブジェクトに変換します
start_time = datetime.datetime.strptime(start_time_str, '%H:%M:%S')
end_time = datetime.datetime.strptime(end_time_str, '%H:%M:%S')

# 入力動画ファイルを開きます
cap = cv2.VideoCapture(input_video_path)

# 入力動画のフレームレートを取得します
fps = int(cap.get(cv2.CAP_PROP_FPS))

# 出力動画の設定
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 出力動画のコーデックを指定します
out = cv2.VideoWriter(output_video_path, fourcc, fps,
                      (int(cap.get(3)), int(cap.get(4))))

# 指定した時刻の前にシークします
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 現在のフレームの時刻を取得します
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

    # 指定した時刻の前に到達したら、ループを抜けます
    if current_time >= (start_time.hour * 3600 + start_time.minute * 60 + start_time.second):
        break

# 指定した時刻から指定した時刻までのフレームを書き込みます
while True:
    ret, frame = cap.read()
    if not ret or current_time >= (end_time.hour * 3600 + end_time.minute * 60 + end_time.second):
        break
    out.write(frame)
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

# クリーンアップ
cap.release()
out.release()
cv2.destroyAllWindows()
