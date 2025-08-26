import os
from rembg import remove

OUTPUT_DIR = os.path.join("src", "output", "cropped_service")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def crop_image(input_path: str, filename: str, output_dir:str = OUTPUT_DIR) -> str:
    """
    Removes background from an image and saves the cropped result.

    Args:
        input_path (str): Path to the input image
        filename (str): Original filename for naming cropped output
        output_dir (str): Path to the output directory
    Returns:
        str: Output path of the cropped image
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path = os.path.join(output_dir, filename)

    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            image = i.read()
            output = remove(image)
            o.write(output)
    return output_path
