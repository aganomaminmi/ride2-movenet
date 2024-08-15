import numpy as np
from pythonosc import udp_client  # OSCのインポート

previous_position = None
threshold = 10  # 閾値（小さいほど敏感に反応）
move_threshold = 20
stationary_frames = 0  # 動きが止まっていると判定されたフレーム数
move_flg = False

score_threshold = 0.2
stop_motion_threshold = 1

frame = 0
count = 0

scores = []

# OSCクライアントの設定
osc_ip = "127.0.0.1"  # OSCの送信先IPアドレス
osc_port = 8001       # OSCの送信先ポート
client = udp_client.SimpleUDPClient(osc_ip, osc_port)

def check_motion(current_position, score):
    global previous_position, stationary_frames
    global frame, move_flg, score_threshold

    scores.append(score)

    frame += 1

    if (previous_position is not None) & (score > score_threshold):

        # 座標の変化量を計算
        movement = np.linalg.norm(
            np.array(current_position) - np.array(previous_position))

        if (move_flg is False) & (movement > move_threshold):
            move_flg = True

        if movement < threshold:
            stationary_frames += 1
        else:
            stationary_frames = 0

        if move_flg:
            # 例えば、10フレーム以上動きがない場合に楽器を鳴らす
            if stationary_frames >= stop_motion_threshold:
                play_instrument()
                stationary_frames = 0  # 楽器を鳴らした後、カウンターをリセット
                move_flg = False

    if score > score_threshold:
        previous_position = current_position

def play_instrument():
    global count

    count += 1
    print("今！")
    print(count)
    
    # OSCメッセージを送信
    client.send_message("/instrument", count)  # 楽器の再生カウントを送信
