import os

from PIL import Image
from moviepy import VideoFileClip

Image.MAX_IMAGE_PIXELS = None

import_dir = os.path.expanduser("~/Downloads/")
output_dir = "resized"

max_dimension = 1920
qualitaet = 85
video_bitrate = "5000k"

if not os.path.exists(output_dir):
    try:
        os.makedirs(output_dir)
    except OSError as e:
        print(f"Error creating output directory: {e}")
        exit(1)

for filename in os.listdir(import_dir):
    input_path = os.path.join(import_dir, filename)
    output_path = os.path.join(output_dir, filename)

    if os.path.exists(output_path) or os.path.isdir(input_path):
        continue

    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        try:
            with Image.open(input_path) as img:
                breite, hoehe = img.size
                img_to_save = img

                if breite > max_dimension or hoehe > max_dimension:
                    if breite > hoehe:
                        neue_breite = max_dimension
                        neue_hoehe = int((hoehe / breite) * neue_breite)
                    else:
                        neue_hoehe = max_dimension
                        neue_breite = int((breite / hoehe) * neue_hoehe)

                    img_to_save = img.resize(
                        (neue_breite, neue_hoehe), Image.Resampling.LANCZOS
                    )
                    print(f"Resizing image: {filename}")

                if img_to_save.mode in ("RGBA", "P"):
                    img_to_save = img_to_save.convert("RGB")

                img_to_save.save(output_path, "JPEG", quality=qualitaet, optimize=True)
                print(f"Saved image: {output_path}")
        except Exception as e:
            print(f"Error processing image {filename}: {e}")

    elif filename.lower().endswith(".mp4"):
        try:
            with VideoFileClip(input_path) as video:
                if video.size[0] > max_dimension or video.size[1] > max_dimension:
                    if video.size[0] > video.size[1]:
                        video_resized = video.resized(width=max_dimension)
                    else:
                        video_resized = video.resized(height=max_dimension)

                    video_resized.write_videofile(output_path, bitrate=video_bitrate)
                else:
                    video.write_videofile(output_path, bitrate=video_bitrate)

                print(f"Saved video: {output_path}")
        except Exception as e:
            print(f"Error processing video {filename}: {e}")
