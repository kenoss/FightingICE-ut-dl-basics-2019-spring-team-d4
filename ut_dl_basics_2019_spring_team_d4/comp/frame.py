__all__ = [
    'FrameGeneratorBase',
    'RandomFrameGeneratorUniform',
    'FrameManager',
]


import functools
import random


class FrameManager:
    def __init__(self, frame, data=None):
        assert frame >= 0

        if data is None:
            self._end_pair = (0, frame)
        else:
            self._end_pair = (data['frame_data'].getRound(), data['frame_data'].getFramesNumber() + frame)

    def is_end(self, data):
        return self._end_pair <= (data['frame_data'].getRound(), data['frame_data'].getFramesNumber())


class FrameGeneratorBase:
    def _f(self):
        raise NotImplementedError()

    def generate(self):
        frame = self._f()
        return FrameManager(frame)


class RandomFrameGeneratorUniform(FrameGeneratorBase):
    def __init__(self, low, high):
        self._f = functools.partial(random.uniform, low, high)
