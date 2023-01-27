"""FireSmokeDetector
    A module for checking the existence of fire and smoke in an image, video file or opencv read image
    using a trained model from `fire-smoke-detect-yolov4-v5`_.

.. _fire-smoke-detect-yolov4-v5:
    https://github.com/gengyanlei/fire-smoke-detect-yolov4
"""

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
    """:class:`FireSmokeDetector` checks the existence of fire and smoke in source image

    Attributes:
        imgsz (int): Image size to be used for inference, 640 by default
            Must be set in multiples of 32, otherwise rounded up
        f_threshold (int): Percentage boundary value used to determine the presence of fire, 60 by default
        s_threshold (int): Percentage boundary value used to determine the presence of smoke, 60 by default
    """
    def __init__(self) -> None:
        """Initialize the :class:`FireSmokeDetector` object."""
        self._device = select_device('0')
        self._half = self._device.type != 'cpu'  # half precision only supported on CUDA        
        self._model = attempt_load('./best.pt', map_location=self._device)  # load FP32 model
        self.imgsz = 640

        self.f_threshold = 60
        self.s_threshold = 60

    @property
    def imgsz(self):
        """int: Image size to be used for inference, 640 by default

        Notes:
            Must be set in multiples of 32, otherwise rounded up

        Raises:
            TypeError: if the data type of the set ``imgsz`` is incorrect
            ValueError: if ``imgsz`` is set non-positive value
        """
        return self._imgsz

    @imgsz.setter
    def imgsz(self, value):
        if type(value) is not int:
            raise TypeError(f"'{value}' is not int but {type(value)}")
        if value <= 0:
            raise ValueError(f"image size must be positive")
        self._imgsz = check_img_size(value, s=self._model.stride.max())  # check img_size
        if self._half:
            self._model.half()  # to FP16
        img = torch.zeros((1, 3, self.imgsz, self.imgsz), device=self._device)  # init img
        _ = self._model(img.half() if self._half else img) if self._device.type != 'cpu' else None  # run once

    @property
    def f_threshold(self):
        """int: Percentage boundary value used to determine the presence of fire, 60 by default

        Raises:
            TypeError: if the data type of the set ``f_threshold`` is incorrect
            ValueError: if ``f_threshold`` is set not within a percentage range
        """
        return self._f_threshold

    @f_threshold.setter
    def f_threshold(self, value):
        if type(value) is not int:
            raise TypeError(f"'{value}' is not int but {type(value)}")
        if value < 0 or value > 100:
            raise ValueError(f"threshold must be a positive number within 100")
        self._f_threshold = value

    @property
    def s_threshold(self):
        """int: Percentage boundary value used to determine the presence of smoke, 60 by default

        Raises:
            TypeError: if the data type of the set ``s_threshold`` is incorrect
            ValueError: if ``s_threshold`` is set not within a percentage range
        """
        return self._s_threshold

    @s_threshold.setter
    def s_threshold(self, value):
        if type(value) is not int:
            raise TypeError(f"'{value}' is not int but {type(value)}")
        if value < 0 or value > 100:
            raise ValueError(f"threshold must be a positive number within 100")
        self._s_threshold = value

    def judge_tf(self, dict, type) -> bool:
        """Determine the true/false from a dict output through a single image

        Args:
            dict: a dictionary that has 'fire' and 'smoke' as keys and the corresponding percentage as value
            type (`'fire'` or `'smoke'`): a key in dict representing the vfx type to check

        Returns:
            bool: whether the ``dict[type]`` percentage is greater than or equal to the threshold

        Raises:
            TypeError: if ``type`` is neither 'fire' nor 'smoke'
        """
        print(dict)
        if type == 'fire':
            threshold = self.f_threshold
        elif type == 'smoke':
            threshold = self.s_threshold
        else:
            raise TypeError

        if dict[type] >= threshold:
            return True
        return False

    def detect_fire_from_read(self, src_img) -> bool:
        """Determine existence of fire from a single image in the form of np.ndarray

        Args:
            src_img (np.ndarray): an image in the form of np.ndarray to determine the existence of fire

        Returns:
            bool: whether the image contains fire

        Raises:
            TypeError: if data type of ``src_img`` is incorrect
        """
        per_dict = self.percent_from_read(src_img)
        return self.judge_tf(per_dict, 'fire')

    def detect_fire_from_path(self, src_path) -> list:
        """Determine existence of fire from multiple images in a file

        Args:
            src_path (str): path of an image file to determine the existence of fire

        Returns:
            list[int]: a list of frames in video for a given path that are determined to contain fire
            Return an empty list if there is no such frame.

        Raises:
            TypeError: if data type of ``src_path`` is incorrect
            FileNotFoundError: if ``src_path`` is not exists or is a directory path
        """
        per_list = self.percent_from_path(src_path)
        res_list = []
        for i, per_dict in enumerate(per_list):
            if self.judge_tf(per_dict, 'fire'):
                res_list.append(i)
        return res_list

    def detect_smoke_from_read(self, src_img) -> bool:
        """Determine existence of smoke from a single image in the form of np.ndarray

        Args:
            src_img (np.ndarray): an image in the form of np.ndarray to determine the existence of smoke

        Returns:
            bool: whether the image contains smoke

        Raises:
            TypeError: if data type of ``src_img`` is incorrect
        """
        per_dict = self.percent_from_read(src_img)
        return self.judge_tf(per_dict, 'smoke')

    def detect_smoke_from_path(self, src_path) -> list:
        """Determine existence of smoke from multiple images in a file

        Args:
            src_path (str): path of an image file to determine the existence of smoke

        Returns:
            list[int]: a list of frames in video for a given path that are determined to contain smoke
            Return an empty list if there is no such frame.

        Raises:
            TypeError: if data type of ``src_path`` is incorrect
            FileNotFoundError: if ``src_path`` is not exists or is a directory path
        """
        per_list = self.percent_from_path(src_path)
        res_list = []
        for i, per_dict in enumerate(per_list):
            if self.judge_tf(per_dict, 'smoke'):
                res_list.append(i)
        return res_list

    def percent_from_read(self, src_img) -> dict:
        """Return a dictionary with percentages of fire and smoke extracted from a single image
        in the form of np.ndarray

        Args:
            src_img (np.ndarray): an image in the form of np.ndarray to determine the existence of fire and smoke

        Returns:
            dict: a dictionary that has 'fire' and 'smoke' as keys and the corresponding percentage as value

        Raises:
            TypeError: if data type of ``src_img`` is incorrect
        """
        if type(src_img) != np.ndarray or src_img.dtype != np.uint8:
            raise TypeError(f"src_img is not numpy.ndarray")

        # Padded resize
        img = letterbox(src_img, new_shape=self.imgsz)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        res_dict = self.run_inference(img)
        return res_dict

    def percent_from_path(self, src_path) -> list:
        """Return a list of dictionary with percentages of fire and smoke extracted from multiple images in a file

        Args:
            src_path (str): path of an image file to determine the existence of fire and smoke

        Returns:
            list[dict]: a list of dictionary
            that has 'fire' and 'smoke' as keys and the corresponding percentage as value

        Raises:
            TypeError: if data type of ``src_path`` is incorrect
            FileNotFoundError: if ``src_path`` is not exists or is a directory path
        """
        if type(src_path) is not str:
            raise TypeError(f"'{src_path}' is not str but {type(src_path)}")
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"{os.path.abspath(src_path)} does not exist")
        if not os.path.isfile(src_path):
            raise FileNotFoundError(f'{os.path.abspath(src_path)} is not a file')

        # Set Dataloader
        dataset = LoadImages(src_path, img_size=self.imgsz)

        # Run inference
        res_list = []
        for _, img, _, _ in dataset:
            sub_res = self.run_inference(img)
            res_list.append(sub_res)
        return res_list

    def run_inference(self, img) -> dict:
        """Use the trained model to infer the percentage probability that fire and smoke exist in a given image

        Args:
            img (np.ndarray): an image in the form of np.ndarray to proceed with inference

        Returns:
            dict: a dictionary that has 'fire' and 'smoke' as keys and the corresponding percentage as value
        """
        img = torch.from_numpy(img).to(self._device)
        img = img.half() if self._half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        pred = self._model(img, augment=False)[0]

        # Apply NMS
        pred = non_max_suppression(pred, 0.4, 0.5)

        res_dict = {
            'fire': 0,
            'smoke': 0
        }

        # Process detections            
        for _, det in enumerate(pred):  # detections per image
            if det is not None and len(det):
                # Write results
                for *_, conf, cls in det:
                    res_dict[self._model.names[int(cls)]] = int(conf * 100)

        return res_dict


def main():
    if len(sys.argv) == 2:
        source = sys.argv[1]
        fd = FireSmokeDetector()
        with torch.no_grad():
            fire_frames = fd.detect_fire_from_path(source)
            smoke_frames = fd.detect_smoke_from_path(source)
            print(f'fire: {fire_frames}\n smoke: {smoke_frames}')
    else:
        print('source 경로를 입력하세요.')


if __name__ == '__main__':
    main()
