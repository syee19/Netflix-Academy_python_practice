"""ThumbnailMaker
    A module for extracting a specific frame from a mov/mp4 video and creating a thumbnail of the desired size
"""

import cv2
import os
import re


class ThumbnailMaker:
    """Class for extracting thumbnails from source video

    Attributes:
        _width (int): Width of source video
        _height (int): Height of source video
        _fps (int): Fps of source video
        _count (int): Number of frames in the source video

    """
    _width = None
    _height = None
    _fps = None
    _count = None
    _default_des_path = 'images/thumbnail.jpg'

    def __init__(self, src_path: str):
        self._src_path = src_path
        self.set_src_info()

    @property
    def src_path(self) -> str:
        """str: Source video path to extract thumbnails"""
        return self._src_path

    @src_path.setter
    def src_path(self, value: str):
        self._src_path = value
        self.set_src_info()

    @property
    def default_des_path(self) -> str:
        """str: Default save path for extracted thumbnails"""
        return self._default_des_path

    @default_des_path.setter
    def default_des_path(self, value: str):
        self._default_des_path = value

    def extract_thumbnail(self, frame_index: int, width=0, height=0, des_path='') -> bool:
        """Method for extracting thumbnail from source video

        Args:
            frame_index (int): Index of frame to be extracted
            width (int, optional): Width of thumbnail image
                By default, the width of the source video is used
            height (int, optional): Height of thumbnail image
                By default, the height of the source video is used
            des_path (str, optional): Save path of extracted thumbnail image
                By default, ``default_des_path`` is used
                If a file with the same name already exists, concatenate an underscore and a number after the filename

        Returns:
            bool: True if successful, False otherwise

        Raises:
            ValueError: if the data type of ``frame_index`` is incorrect
            IndexError: if ``frame_index`` is out of the frame range of the source video

        """
        if type(frame_index) is not int:
            raise ValueError(f"invalid literal: '{frame_index}'")
        if frame_index <= 0 or frame_index > self._count:
            raise IndexError(f"frame index out of range: {frame_index}\n\tvalid frame range: 0 ~ {self._count} ")

        if width <= 0:
            width = self._width
        if height <= 0:
            height = self._height
        if not des_path:
            des_path = self._default_des_path

        index = 1
        while os.path.exists(des_path):
            des_path = re.sub(r'_\d+(?=[.]\w+$)', r'', des_path)
            des_path = re.sub(r'(?=[.]\w+$)', rf'_{index}', des_path)
            index += 1

        video = cv2.VideoCapture(self._src_path)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_index-1)
        ret, frame = video.read()
        output = cv2.resize(frame, (width, height))
        cv2.imwrite(f'{des_path}', output)
        video.release()
        return True

    def play_src(self):
        """Method to play source video

        Note:
            The frame index is displayed at the top left of the video.
            You can pause and resume play with the space bar and exit with the q key.

        """
        video = cv2.VideoCapture(self._src_path)
        frame_index = 0
        while True:
            ret, frame = video.read()
            if not ret:
                break
            frame_index += 1
            text = cv2.putText(frame, f"frame: {frame_index}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            cv2.imshow("PlaySrc", text)

            input_key = cv2.waitKey(10)
            if input_key & 0xFF == ord(' '):
                while cv2.waitKey(0) & 0xFF != ord(' '):
                    pass
            if input_key & 0xFF == ord("q"):
                break
        video.release()
        cv2.destroyAllWindows()

    def set_src_info(self):
        """Method to get and save width, height, fps, and count information from the source video"""
        video = cv2.VideoCapture(self._src_path)
        self._width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._fps = int(video.get(cv2.CAP_PROP_FPS))
        self._count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video.release()


def main():
    my_thumbnail = ThumbnailMaker('X2Download.app-Torch Windy 02 vfx stock footage.mp4')
    my_thumbnail.play_src()
    frame_index = int(input("frame to extract: "))
    my_thumbnail.extract_thumbnail(frame_index)


if __name__ == '__main__':
    main()
