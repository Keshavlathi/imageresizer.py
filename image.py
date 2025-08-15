import os
from PIL import Image

def batch_resize_aspect_ratio(input_folder, output_folder, max_size, output_format="JPEG"):
    """
    Resizes all images in a folder to fit within a maximum size while
    maintaining aspect ratio.

    Args:
        input_folder (str): Path to the folder with original images.
        output_folder (str): Path to the folder to save resized images.
        max_size (tuple): A tuple of (max_width, max_height).
        output_format (str): The desired output format (e.g., "JPEG", "PNG").
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Counters for the final summary
    success_count = 0
    failure_count = 0

    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    print(f"Found {len(image_files)} images to process...")

    for filename in image_files:
        try:
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)

            # Preserve RGBA for PNGs, otherwise convert to RGB
            if output_format.upper() == "PNG" and img.mode == 'RGBA':
                pass # Keep RGBA
            else:
                img = img.convert('RGB') # Convert to RGB for JPEG and others

            # Calculate new size while preserving aspect ratio
            img.thumbnail(max_size, Image.LANCZOS)

            # Construct the new filename and save path
            base_name = os.path.splitext(filename)[0]
            new_filename = f"{base_name}.{output_format.lower()}"
            save_path = os.path.join(output_folder, new_filename)

            # Save the resized image
            img.save(save_path, output_format.upper())
            print(f"✅ Resized and saved: {save_path}")
            success_count += 1

        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")
            failure_count += 1

    # Print a final summary report
    print("\n--- Batch Processing Complete ---")
    print(f"Successfully processed: {success_count} images")
    print(f"Skipped (due to errors): {failure_count} files")
    print(f"Resized images are located in: '{output_folder}'")


# --- Example Usage ---

input_dir = "images"       # Folder with original images
output_dir = "resized"     # Folder to save resized images
max_dimensions = (800, 600)  # Max width and height
file_format = "JPEG"       # Can be "PNG", "JPEG", etc.

batch_resize_aspect_ratio(input_dir, output_dir, max_dimensions, file_format)