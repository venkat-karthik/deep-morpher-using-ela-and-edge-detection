import os
import sys
import tempfile

try:
    from PIL import Image, ImageChops, ImageEnhance
except ImportError:
    print("Error: Pillow not installed.")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)


def convert_to_ela_image_ps7(path: str):
    """PS-7 Compliant Error Level Analysis (ELA)"""
    image = Image.open(path).convert("RGB")

    # Create a unique temp JPEG file
    fd, temp_filename = tempfile.mkstemp(suffix=".jpg")
    os.close(fd)  # close file descriptor; Pillow will write to this path

    try:
        # Step 2: fixed JPEG quality 90
        image.save(temp_filename, "JPEG", quality=90)

        # Step 3: reload compressed image (ensure file is closed properly)
        with Image.open(temp_filename) as temp_image:
            temp_image = temp_image.convert("RGB")

            # Step 4: absolute difference
            ela_image = ImageChops.difference(image, temp_image)

        # Step 5: brightness amplification
        extrema = ela_image.getextrema()
        max_diff = max(ex[1] for ex in extrema) or 1
        scale = 255.0 / max_diff
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

        return ela_image

    finally:
        # Cleanup temp file always
        try:
            os.remove(temp_filename)
        except OSError:
            pass


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "input/suspect_frame.jpg"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output/ela_result.jpg"

    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        print("Usage: python run_ps7.py <input_image> <output_image>")
        sys.exit(1)

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"Created output directory: {output_dir}")

    try:
        result = convert_to_ela_image_ps7(input_path)
        result.save(output_path)
        print(f"Done. Saved: {output_path}")
    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)
