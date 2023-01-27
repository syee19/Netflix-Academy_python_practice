"""
A Python library for making resized thumbnails and detect fire and 
smoke from video.

"""

from video_toolpkg.thumbnail_maker import ThumbnailMaker
from video_toolpkg.fire_smoke_detector import FireSmokeDetector

extract_thumbnail = ThumbnailMaker.extract_thumbnail
play_src = ThumbnailMaker.play_src

detect_fire_from_read = FireSmokeDetector.detect_fire_from_read
detect_fire_from_path = FireSmokeDetector.detect_fire_from_path
detect_smoke_from_read = FireSmokeDetector.detect_smoke_from_read
detect_smoke_from_path = FireSmokeDetector.detect_smoke_from_paths