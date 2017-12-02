# -*- coding: utf-8 -*-

import sys, os
import numpy as np
import cv2
from scipy import stats


def motion_model(d, mu=0.0, sig=0.1):
    """
    状態遷移モデルの定義
    """
    M = len(d)
    pred = d + np.random.normal(mu, sig, size=M)
    pred[pred > 1.0] = 1.0
    pred[pred < 0.0] = 0.0
    return pred


def observation_model(frame_hsv, x, y, loc=0, scale=20):
    def color_hist(image_hsv, pix, loc, scale, saturation=128):
        image_h = image_hsv[int(pix[1]), int(pix[0]), 0]
        image_s = image_hsv[int(pix[1]), int(pix[0]), 1]
        if image_s < saturation:
            return 0e-12
        p1 = stats.norm.pdf(image_h, loc=loc, scale=scale)
        p2 = stats.norm.pdf(image_h - 179, loc=loc, scale=scale)
        p = max(p1, p2)
        return p

    w = np.array(
        [color_hist(frame_hsv, s, loc, scale) for s in zip(x, y)]
    )
    return w


if __name__ == "__main__":
    M = 1000  # パーティクルの数
    # 初期分布の生成
    x = np.random.rand(M)  # 0~1の一様乱数
    y = np.random.rand(M)  # 0~1の一様乱数

    cap = cv2.VideoCapture(-1)

    if cap.isOpened() is False:
        print('cannot open web-camera')
        sys.exit(1)

    while True:
        # カメラ画像のキャプチャ
        # retは画像を取得成功フラグ
        ret, frame = cap.read()
        width = frame.shape[1]
        height = frame.shape[0]

        # パーティクルの遷移
        pred_x = motion_model(x)
        pred_y = motion_model(y)

        # 観測モデル
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # frameをHSVカラーに変換
        target = np.uint8([[[0, 0, 255]]])
        hsv_target = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)
        weight = observation_model(
            frame_hsv,
            pred_x * (width - 1), pred_y * (height - 1),
            loc=hsv_target[0][0][0], scale=20.0)
        p = weight / np.sum(weight)

        # リサンプリング
        idx = np.arange(M)
        resampling_idx = np.random.choice(idx, size=M, p=p)
        pred_x = np.array([pred_x[i] for i in resampling_idx])
        pred_y = np.array([pred_y[i] for i in resampling_idx])

        # 座標変換
        map_x = pred_x * (width - 1)
        map_y = pred_y * (height - 1)

        # 状態の変更
        x = pred_x
        y = pred_y

        # 位置の推定
        x_est = int(np.median(map_x))
        y_est = int(np.median(map_y))

        # パーティクル状態を画像に描画
        for sx, sy, w in zip(map_x, map_y, weight):
            cv2.circle(frame, (int(sx), int(sy)), int(w * 10), (0, 0, 255), -1)
            # cv2.circle(frame, (int(sx), int(sy)), 4, (0, 0, 255), -1)
        cv2.circle(frame, (x_est, y_est), 10, (255, 0, 0), -1)  # 推定位置

        # フレームを表示する
        cv2.imshow('ColorTracker', frame)

        k = cv2.waitKey(1)  # 1msec待つ
        if k == 27:  # ESCキーで終了
            break

    cap.release()
    cv2.destroyAllWindows()
