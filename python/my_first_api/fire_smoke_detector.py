import cv2
import torch
import numpy as np
import os

import sys
sys.path.append("/home/rapa/git/fire-smoke-detect-yolov4/yolov5")
from models.experimental import attempt_load
from utils.datasets import LoadImages, letterbox
from utils.general import (check_img_size, non_max_suppression, scale_coords)
from utils.torch_utils import select_device

class FireSmokeDetector:
    def __init__(self) -> None:        
        self._weights = './best.pt' 
        self._imgsz = 640
        
        # Initialize
        self._device = select_device('0')
        self._half = self._device.type != 'cpu'  # half precision only supported on CUDA

        self.load_model()
    
    @property
    def weights(self):
        return self._weights
    
    @weights.setter
    def weights(self, value):
        if type(value) is not str:
            raise TypeError(f"invalid literal: '{value}' is not str but {type(value)}")
        if os.path.exists(value):
            raise FileExistsError(f"{os.path.abspath(value)} does not exist")
        self._weights = value
        self.load_model()
    
    @property
    def imgsz(self):
        return self._imgsz
    
    @imgsz.setter
    def imgsz(self, value):
        if type(value) is not int:
            raise TypeError(f"invalid literal: '{value}' is not int but {type(value)}")
        if value <= 0:
            raise ValueError(f"imgsz must be positive")
        self._imgsz = value
        self.load_model()
                
    def load_model(self):
        self._model = attempt_load(self._weights, map_location=self._device)  # load FP32 model
        self._imgsz = check_img_size(self._imgsz, s=self._model.stride.max())  # check img_size
        if self._half:
            self._model.half()  # to FP16
                
        img = torch.zeros((1, 3, self._imgsz, self._imgsz), device=self._device)  # init img
        _ = self._model(img.half() if self._half else img) if self._device.type != 'cpu' else None  # run once
    
    def detect_from_image(self, src_img):
        # 경로가 아니라 cv2의 imread나 VideoCapture.read로부터 가져오기
        if type(src_img) != np.ndarray or src_img.dtype != np.uint8:
            raise TypeError(f"src_img is not numpy.ndarray")
                
        result = {
            'fire': 0, 
            'smoke': 0
        }

        # Run inference
        # Padded resize
        img = letterbox(src_img, new_shape=self._imgsz)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        
        img = torch.from_numpy(img).to(self._device)
        img = img.half() if self._half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        pred = self._model(img, augment=False)[0]

        # Apply NMS
        pred = non_max_suppression(pred, 0.4, 0.5)

        # Process detections
        det = pred[0]
        if det is not None and len(det):
            # Write results
            for *_, conf, cls in det:
                result[self._model.names[int(cls)]] = int(conf*100)
        print(result)
    
    def detect_from_path(self, src_path):
        result = {
            'fire': 0, 
            'smoke': 0
        }
        
        # Set Dataloader
        dataset = LoadImages(src_path, img_size=self._imgsz)
        
        # Run inference
        for _, img, _, _ in dataset:
            img = torch.from_numpy(img).to(self._device)
            img = img.half() if self._half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            pred = self._model(img, augment=False)[0]

            # Apply NMS
            pred = non_max_suppression(pred, 0.4, 0.5)

            # Process detections            
            for _, det in enumerate(pred):  # detections per image
                if det is not None and len(det):
                    # Write results
                    for *_, conf, cls in det:
                        result[self._model.names[int(cls)]] = int(conf*100)
            print(result)        
    

def main():
    if len(sys.argv) == 2:
        source = sys.argv[1]
        fd = FireSmokeDetector()
        with torch.no_grad():
            fd.detect_from_path(source)
    else:
        print('source 경로를 입력하세요.')

if __name__ == '__main__':
    main()