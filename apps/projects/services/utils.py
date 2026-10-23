import logging
import os
import subprocess

from django.conf import settings
from django.db import close_old_connections

from apps.projects.models import Project

logger = logging.getLogger(__name__)
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm"}

def is_video(name):
    return os.path.splitext(name or "")[1].lower() in VIDEO_EXTENSIONS

def web_version_path(source_name):
    stem = os.path.splitext(os.path.basename(source_name))[0]
    return f"presentations/web/{stem}.mp4"

def make_web_version(project_id):

    try:
        close_old_connections()
        project = Project.objects.get(pk=project_id)
        if not project.presentation_file:
            return

        if not is_video(project.presentation_file.name):
            return

        relative = web_version_path(project.presentation_file.name)
        final = os.path.join(settings.MEDIA_ROOT, relative)
        temporary = final[:-4] + ".tmp.mp4"
        os.makedirs(os.path.dirname(final), exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y", "-i", project.presentation_file.path,
            "-vf", "scale=-2:'min(480,ih)'",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
            "-maxrate", "900k", "-bufsize", "1800k", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "64k",
            "-movflags", "+faststart",
            temporary,
        ], check=True, capture_output=True, timeout=3600)
        os.replace(temporary, final)
        Project.objects.filter(pk=project_id).update(presentation_web=relative)
    except Exception:
        logger.exception("Conversion vidéo impossible (projet %s)", project_id)
    finally:
        close_old_connections()
