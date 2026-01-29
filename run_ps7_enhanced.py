import os
import sys
import tempfile
import cv2
import numpy as np
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageEnhance, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow not installed.")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)

def convert_to_ela_image_ps7(path: str, quality: int = 90):
    """PS-7 Compliant Error Level Analysis (ELA)"""
    image = Image.open(path).convert("RGB")
    
    # Create a unique temp JPEG file
    fd, temp_filename = tempfile.mkstemp(suffix=".jpg")
    os.close(fd)
    
    try:
        # Step 2: fixed JPEG quality
        image.save(temp_filename, "JPEG", quality=quality)
        
        # Step 3: reload compressed image
        with Image.open(temp_filename) as temp_image:
            temp_image = temp_image.convert("RGB")
            
            # Step 4: absolute difference
            ela_image = ImageChops.difference(image, temp_image)
        
        # Step 5: brightness amplification
        extrema = ela_image.getextrema()
        max_diff = max(ex[1] for ex in extrema) or 1
        scale = 255.0 / max_diff
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        
        return ela_image, temp_image
        
    finally:
        # Cleanup temp file
        try:
            os.remove(temp_filename)
        except OSError:
            pass

def find_suspicious_regions(ela_image, threshold=128):
    """Tier 1: Find and highlight suspicious regions with bounding boxes"""
    # Convert to grayscale and numpy array
    ela_gray = ela_image.convert('L')
    ela_array = np.array(ela_gray)
    
    # Threshold bright pixels
    _, binary = cv2.threshold(ela_array, threshold, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by area (remove noise)
    min_area = 100
    suspicious_regions = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            suspicious_regions.append((x, y, w, h, area))
    
    return suspicious_regions

def create_bounding_box_overlay(original_image, suspicious_regions):
    """Create overlay with bounding boxes on original image"""
    overlay = original_image.copy()
    draw = ImageDraw.Draw(overlay)
    
    for i, (x, y, w, h, area) in enumerate(suspicious_regions):
        # Draw rectangle
        draw.rectangle([x, y, x+w, y+h], outline="red", width=3)
        
        # Add label
        label = f"Region {i+1}"
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        draw.text((x, y-20), label, fill="red", font=font)
    
    return overlay

def create_side_by_side_output(original, recompressed, ela_heatmap, overlay):
    """Tier 1: Create professional side-by-side comparison"""
    # Ensure all images are same size
    width, height = original.size
    recompressed = recompressed.resize((width, height))
    ela_heatmap = ela_heatmap.resize((width, height))
    overlay = overlay.resize((width, height))
    
    # Create 4-panel output: Original | Recompressed | ELA | Overlay
    combined_width = width * 4
    combined_height = height + 60  # Extra space for labels
    
    combined = Image.new('RGB', (combined_width, combined_height), 'white')
    
    # Paste images
    combined.paste(original, (0, 30))
    combined.paste(recompressed, (width, 30))
    combined.paste(ela_heatmap, (width*2, 30))
    combined.paste(overlay, (width*3, 30))
    
    # Add labels
    draw = ImageDraw.Draw(combined)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    labels = ["Original", "Recompressed (90%)", "ELA Heatmap", "Suspicious Regions"]
    for i, label in enumerate(labels):
        draw.text((i*width + 10, 5), label, fill="black", font=font)
    
    return combined

def quality_sweep_analysis(image_path, qualities=[85, 90, 95]):
    """Tier 1: Multi-quality ELA analysis for robust detection"""
    results = {}
    
    for quality in qualities:
        ela_image, recompressed = convert_to_ela_image_ps7(image_path, quality)
        results[quality] = {
            'ela': ela_image,
            'recompressed': recompressed,
            'suspicious_regions': find_suspicious_regions(ela_image)
        }
    
    return results

def calculate_inconsistency_score(ela_image):
    """Tier 2: Calculate suspicion metric (NOT probability)"""
    ela_array = np.array(ela_image.convert('L'))
    
    # Mean of top 1% brightest pixels
    top_1_percent = np.percentile(ela_array, 99)
    top_pixels = ela_array[ela_array >= top_1_percent]
    mean_top_brightness = np.mean(top_pixels) if len(top_pixels) > 0 else 0
    
    # Percentage of pixels above threshold
    threshold = 128
    bright_pixels = np.sum(ela_array > threshold)
    total_pixels = ela_array.size
    bright_percentage = (bright_pixels / total_pixels) * 100
    
    # Combined inconsistency score (0-100)
    inconsistency_score = min(100, (mean_top_brightness / 255 * 50) + (bright_percentage * 2))
    
    return {
        'inconsistency_score': round(inconsistency_score, 2),
        'bright_percentage': round(bright_percentage, 2),
        'mean_top_brightness': round(mean_top_brightness, 2)
    }

def process_video_frames(video_path, output_dir, frame_interval=30):
    """Tier 2: Video support - extract and analyze frames"""
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    processed_frames = 0
    
    frames_dir = Path(output_dir) / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            # Save frame as temporary image
            frame_path = frames_dir / f"frame_{processed_frames:04d}.jpg"
            cv2.imwrite(str(frame_path), frame)
            
            # Process with ELA
            try:
                ela_image, recompressed = convert_to_ela_image_ps7(str(frame_path))
                suspicious_regions = find_suspicious_regions(ela_image)
                score = calculate_inconsistency_score(ela_image)
                
                # Save ELA result
                ela_output = frames_dir / f"frame_{processed_frames:04d}_ela.jpg"
                ela_image.save(str(ela_output))
                
                results.append({
                    'frame': processed_frames,
                    'timestamp': frame_count / cap.get(cv2.CAP_PROP_FPS),
                    'suspicious_regions': len(suspicious_regions),
                    'inconsistency_score': score['inconsistency_score']
                })
                
                processed_frames += 1
                
            except Exception as e:
                print(f"Error processing frame {frame_count}: {e}")
        
        frame_count += 1
    
    cap.release()
    return results

def create_block_grid_visualization(ela_image, block_size=8):
    """Tier 3: JPEG block-grid analysis (8x8 blocks)"""
    ela_array = np.array(ela_image.convert('L'))
    height, width = ela_array.shape
    
    # Calculate block dimensions
    blocks_h = height // block_size
    blocks_w = width // block_size
    
    # Create block intensity map
    block_map = np.zeros((blocks_h, blocks_w))
    
    for i in range(blocks_h):
        for j in range(blocks_w):
            y_start = i * block_size
            y_end = min((i + 1) * block_size, height)
            x_start = j * block_size
            x_end = min((j + 1) * block_size, width)
            
            block = ela_array[y_start:y_end, x_start:x_end]
            block_map[i, j] = np.mean(block)
    
    # Normalize and convert to image
    block_map_normalized = (block_map / np.max(block_map) * 255).astype(np.uint8)
    
    # Resize to original dimensions for visualization
    block_visualization = cv2.resize(block_map_normalized, (width, height), interpolation=cv2.INTER_NEAREST)
    
    return Image.fromarray(block_visualization)

def enhanced_ela_analysis(input_path, output_dir):
    """Complete enhanced ELA analysis with all tiers"""
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🔍 Enhanced ELA Analysis: {input_path.name}")
    
    # Check if input is video
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}
    if input_path.suffix.lower() in video_extensions:
        print("📹 Video detected - processing frames...")
        results = process_video_frames(str(input_path), str(output_dir))
        
        # Save video analysis report
        with open(output_dir / "video_analysis_report.txt", 'w') as f:
            f.write("Video ELA Analysis Report\n")
            f.write("=" * 30 + "\n\n")
            for result in results:
                f.write(f"Frame {result['frame']:04d} (t={result['timestamp']:.2f}s): "
                       f"Regions={result['suspicious_regions']}, "
                       f"Score={result['inconsistency_score']:.2f}\n")
        
        print(f"✅ Processed {len(results)} frames")
        return
    
    # Load original image
    original = Image.open(input_path).convert('RGB')
    
    # Tier 1: Quality sweep analysis
    print("🔄 Running quality sweep analysis...")
    quality_results = quality_sweep_analysis(str(input_path))
    
    # Process each quality level
    for quality, data in quality_results.items():
        ela_image = data['ela']
        recompressed = data['recompressed']
        suspicious_regions = data['suspicious_regions']
        
        # Calculate inconsistency score
        score_data = calculate_inconsistency_score(ela_image)
        
        # Create bounding box overlay
        overlay = create_bounding_box_overlay(original, suspicious_regions)
        
        # Create side-by-side comparison
        comparison = create_side_by_side_output(original, recompressed, ela_image, overlay)
        
        # Create block grid visualization
        block_viz = create_block_grid_visualization(ela_image)
        
        # Save all outputs
        quality_dir = output_dir / f"quality_{quality}"
        quality_dir.mkdir(exist_ok=True)
        
        ela_image.save(quality_dir / "ela_heatmap.jpg")
        overlay.save(quality_dir / "suspicious_regions.jpg")
        comparison.save(quality_dir / "side_by_side_analysis.jpg")
        block_viz.save(quality_dir / "block_grid_analysis.jpg")
        
        # Save analysis report
        with open(quality_dir / "analysis_report.txt", 'w') as f:
            f.write(f"ELA Analysis Report - Quality {quality}%\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Inconsistency Score: {score_data['inconsistency_score']}/100\n")
            f.write(f"Bright Pixel Percentage: {score_data['bright_percentage']}%\n")
            f.write(f"Mean Top Brightness: {score_data['mean_top_brightness']}/255\n")
            f.write(f"Suspicious Regions Found: {len(suspicious_regions)}\n\n")
            
            f.write("Interpretation:\n")
            f.write("- Inconsistency Score: Higher values indicate more potential tampering\n")
            f.write("- Bright regions in heatmap suggest compression inconsistencies\n")
            f.write("- Red bounding boxes highlight most suspicious areas\n")
            f.write("- Block grid shows JPEG compression patterns\n")
        
        print(f"✅ Quality {quality}%: Score={score_data['inconsistency_score']:.1f}, Regions={len(suspicious_regions)}")
    
    # Create summary comparison
    print("📊 Creating summary analysis...")
    summary_images = []
    for quality in [85, 90, 95]:
        img = Image.open(output_dir / f"quality_{quality}" / "side_by_side_analysis.jpg")
        summary_images.append(img)
    
    # Stack all quality comparisons vertically
    total_height = sum(img.height for img in summary_images)
    max_width = max(img.width for img in summary_images)
    
    summary = Image.new('RGB', (max_width, total_height), 'white')
    y_offset = 0
    for img in summary_images:
        summary.paste(img, (0, y_offset))
        y_offset += img.height
    
    summary.save(output_dir / "complete_analysis_summary.jpg")
    
    print(f"🎯 Complete analysis saved to: {output_dir}")
    print("📁 Check the following files:")
    print("   - complete_analysis_summary.jpg (overview)")
    print("   - quality_XX/ folders (detailed analysis)")
    print("   - analysis_report.txt files (metrics)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Enhanced ELA Analysis Tool")
        print("Usage: python run_ps7_enhanced.py <input_image_or_video> [output_directory]")
        print("\nExamples:")
        print("  python run_ps7_enhanced.py input/suspect.jpg output/analysis")
        print("  python run_ps7_enhanced.py video.mp4 output/video_analysis")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "enhanced_output"
    
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)
    
    try:
        enhanced_ela_analysis(input_path, output_dir)
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)