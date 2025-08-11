"""Vercel用のシンプルなモジュールスタブ"""

class YoloxONNX:
    def __init__(self, **kwargs):
        print("Demo mode: YOLOX model stub initialized")
    
    def inference(self, _image):
        import numpy as np
        # デモ用のダミー結果を返す
        return np.array([]), np.array([]), np.array([])


class CvDrawText:
    @staticmethod
    def puttext(*args, **kwargs):
        # デモ用のスタブ
        return args[0] if args else None
