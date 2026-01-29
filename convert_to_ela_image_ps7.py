from PIL import Image, ImageChops, ImageEnhance
import os

def convert_to_ela_image_ps7(path):
    """
    PS-7 Compliant Error Level Analysis (ELA)
    
    This function implements the exact PS-7 hint logic:
    1. Load original image
    2. Save as JPEG with 90% quality (MANDATORY)
    3. Reload compressed image
    4. Compute absolute difference
    5. Amplify/normalize brightness
    
    Args:
        path: Path to the input image
        
    Returns:
        PIL Image object with ELA visualization
    """
    # Step 1: Load original image
    image = Image.open(path).convert('RGB')
    temp_filename = 'temp_ps7.jpg'
    
    # Step 2: Save with fixed 90% JPEG quality (MANDATORY)
    image.save(temp_filename, 'JPEG', quality=90)
    
    # Step 3: Reload compressed image
    temp_image = Image.open(temp_filename)
    
    # Step 4: Absolute difference
    ela_image = ImageChops.difference(image, temp_image)
    
    # Step 5: Brightness amplification
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    
    scale = 255.0 / max_diff
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    
    # Clean up temporary file
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
    
    return ela_image

# Example usage
if __name__ == "__main__":
    # Test the PS-7 compliant function
    try:
        # Replace 'test_image.jpg' with actual image path
        result = convert_to_ela_image_ps7('result/org1.jpg')
        result.save('result/ps7_ela_output.jpg')
        print("PS-7 compliant ELA processing completed successfully!")
    except Exception as e:
        print(f"Error: {e}")