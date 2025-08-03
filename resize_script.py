import os

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

import_dir = "originale"
output_dir = "resized"

max_dimension = 1920
qualitaet = 85

if not os.path.exists(output_dir):
    try:
        os.makedirs(output_dir)
    except Exception as e:
        print(f"Error creating output directory: {e}")
        exit(1)

for file in os.listdir(import_dir):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        input_path = os.path.join(import_dir, file)
        output_path = os.path.join(output_dir, file)

        try:
            with Image.open(input_path) as img:
                breite, hoehe = img.size

                if breite > max_dimension or hoehe > max_dimension:
                    if breite > hoehe:
                        neue_breite = max_dimension
                        neue_hoehe = int((hoehe / breite) * neue_breite)
                    else:
                        neue_hoehe = max_dimension
                        neue_breite = int((breite / hoehe) * neue_hoehe)

                    img = img.resize(
                        (neue_breite, neue_hoehe), Image.Resampling.LANCZOS
                    )

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                img.save(output_path, "JPEG", quality=qualitaet, optimize=True)

                print(f"Resized and saved: {output_path}")
        except Exception as e:
            print(f"Error processing {file}: {e}")
