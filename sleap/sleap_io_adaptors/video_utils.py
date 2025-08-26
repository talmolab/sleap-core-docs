"""Video utilities for sleap-io integration."""

from sleap_io import Video
from sleap_io.io.video_reading import MediaVideo, HDF5Video, ImageVideo, TiffVideo
from typing import Tuple

# Object that signals shutdown
_sentinel = object()

def can_use_ffmpeg():
    """Check if ffmpeg is available for writing videos."""
    try:
        import imageio_ffmpeg as ffmpeg
    except ImportError:
        return False

    try:
        # Try to get the version of the ffmpeg plugin
        ffmpeg_version = ffmpeg.get_ffmpeg_version()
        if ffmpeg_version:
            return True
    except Exception:
        return False

    return False

def available_video_exts() -> Tuple[str]:
    """Return tuple of supported video extensions.

    Returns:
        Tuple of supported video extensions.
    """
    return (
        MediaVideo.EXTS
        + HDF5Video.EXTS
        + ImageVideo.EXTS
        + TiffVideo.EXTS
    )

