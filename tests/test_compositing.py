# -*- coding: utf-8 -*-
"""Compositing tests for use with pytest."""
import sys
from os.path import join

import pytest

from moviepy.editor import *
from moviepy.utils import close_all_clips

from tests.test_helper import TMP_DIR, FONT


def test_clips_array():
    red = ColorClip((1024, 800), color=(255, 0, 0))
    green = ColorClip((1024, 800), color=(0, 255, 0))
    blue = ColorClip((1024, 800), color=(0, 0, 255))

    video = clips_array([[red, green, blue]])

    with pytest.raises(ValueError):  # duration not set
        video.resize(width=480).write_videofile(join(TMP_DIR, "test_clips_array.mp4"))
    close_all_clips(locals())


def test_clips_array_duration():
    # NOTE: anyone knows what behaviour this sets ? If yes please replace
    # this comment.
    red = ColorClip((256, 200), color=(255, 0, 0))
    green = ColorClip((256, 200), color=(0, 255, 0))
    blue = ColorClip((256, 200), color=(0, 0, 255))

    video = clips_array([[red, green, blue]]).set_duration(5)
    with pytest.raises(AttributeError):  # fps not set
        video.write_videofile(join(TMP_DIR, "test_clips_array.mp4"))

    # this one should work correctly
    red.fps = green.fps = blue.fps = 30
    video = clips_array([[red, green, blue]]).set_duration(5)
    video.write_videofile(join(TMP_DIR, "test_clips_array.mp4"))
    close_all_clips(locals())


def test_blended_composite_video_clip():
    bg = VideoFileClip("media/video_for_blend_modes.mp4").set_duration(1.0)
    text_kwargs = {"font": FONT, "fontsize": 96, "color": "#bbbb11"}
    t1 = (
        TextClip("SOFT BLEND", **text_kwargs)
        .set_duration(1.0)
        .set_position(("center", "top"))
    )
    t2 = (
        TextClip("HARD BLEND", **text_kwargs)
        .set_duration(1.0)
        .set_position(("center", "bottom"))
    )
    comp = BlendedCompositeVideoClip(
        [bg, t1, t2],
        clips_blending=[
            {"blend_mode": "normal"},
            {"blend_mode": "soft_light", "blend_opacity": 0.8},
            {"blend_mode": "hard_light", "blend_weight": 0.8},
        ],
    )
    comp.write_videofile(join(TMP_DIR, "test_blended_composition.mp4"))
    return
