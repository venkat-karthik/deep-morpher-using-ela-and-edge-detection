from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import tempfile
import io
import base64
from werkzeug.utils import secure_filename
from PIL import Image, ImageChops, ImageEnhance
import uuid
from datetime import datetime
import shutil

app = Flask(__name__)
app.secret_key = 'ela_forgery_detection_secret_key_2024'

# Configuration
TEMP_DIR = tempfile.gettempdir()
UPLOAD_FOLDER = os.path.join(TEMP_DIR, 'uploads')
RESULTS_FOLDER = os.path.join(TEMP_DIR, 'static', 'results')
ORIGINALS_FOLDER = os.path.join(TEMP_DIR, 'static', 'originals')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size

# Create directories if they don't exist in writable TEMP_DIR
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(ORIGINALS_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_ela_statistics(ela_image):
    """
    Perform statistical analysis on the un-amplified ELA image.
    Returns mean, std_dev, tamper_score, and bounding box of the hottest region.
    """
    gray_ela = ela_image.convert("L")
    width, height = gray_ela.size
    total_pixels = width * height
    
    # Calculate global statistics using histogram
    hist = gray_ela.histogram()
    mean_diff = sum(i * hist[i] for i in range(256)) / total_pixels
    variance = sum(hist[i] * ((i - mean_diff) ** 2) for i in range(256)) / total_pixels
    std_dev = variance ** 0.5
    
    # Suspicious pixels (difference > 12)
    suspicious_count = sum(hist[12:])
    suspicious_ratio = (suspicious_count / total_pixels) * 100
    
    # Calibrate a robust tamper score (0-100)
    # Natural images typically have low mean (<3) and low std_dev (<4)
    raw_score = (mean_diff * 8.0) + (std_dev * 4.0) + (suspicious_ratio * 1.5)
    tamper_score = min(100.0, max(0.0, raw_score))
    
    # Grid-based localized anomaly detection (8x8 grid)
    cell_w = width / 8.0
    cell_h = height / 8.0
    cells_data = []
    
    for row in range(8):
        for col in range(8):
            box = (int(col * cell_w), int(row * cell_h), int((col + 1) * cell_w), int((row + 1) * cell_h))
            cell_crop = gray_ela.crop(box)
            cell_hist = cell_crop.histogram()
            cell_total = sum(cell_hist) or 1
            cell_mean = sum(i * cell_hist[i] for i in range(256)) / cell_total
            cells_data.append(((row, col), cell_mean, box))
            
    # Find the cell with the highest ELA mean
    hottest_cell = max(cells_data, key=lambda x: x[1])
    hottest_coords = hottest_cell[0]
    hottest_mean = hottest_cell[1]
    hottest_box = hottest_cell[2]
    
    # Check if this cell is an anomaly (significantly brighter than the average cell)
    avg_cell_mean = sum(x[1] for x in cells_data) / 64.0
    is_anomaly = hottest_mean > (avg_cell_mean * 1.5) and hottest_mean > 5.0
    
    normalized_box = None
    if is_anomaly:
        normalized_box = {
            "x": hottest_box[0] / width,
            "y": hottest_box[1] / height,
            "w": (hottest_box[2] - hottest_box[0]) / width,
            "h": (hottest_box[3] - hottest_box[1]) / height
        }
        
    return {
        "mean_diff": round(mean_diff, 2),
        "std_dev": round(std_dev, 2),
        "suspicious_ratio": round(suspicious_ratio, 2),
        "tamper_score": round(tamper_score, 1),
        "anomaly_box": normalized_box,
        "histogram": hist[:50]  # Only need first 50 values for chart
    }

def convert_to_ela_image_ps7(image_path):
    """PS-7 Compliant Error Level Analysis (ELA)"""
    try:
        # Load and convert image
        image = Image.open(image_path).convert("RGB")
        
        # Create temporary JPEG file
        fd, temp_filename = tempfile.mkstemp(suffix=".jpg")
        os.close(fd)
        
        try:
            # Step 2: Save with fixed 90% JPEG quality (PS-7 requirement)
            image.save(temp_filename, "JPEG", quality=90)
            
            # Step 3: Reload compressed image
            with Image.open(temp_filename) as temp_image:
                temp_image = temp_image.convert("RGB")
                
                # Step 4: Calculate absolute difference
                ela_image = ImageChops.difference(image, temp_image)
            
            # Step 5: Brightness amplification
            extrema = ela_image.getextrema()
            max_diff = max(ex[1] for ex in extrema) or 1
            scale = 255.0 / max_diff
            ela_image_amplified = ImageEnhance.Brightness(ela_image).enhance(scale)
            
            return ela_image, ela_image_amplified
            
        finally:
            # Clean up temp file
            try:
                os.remove(temp_filename)
            except OSError:
                pass
                
    except Exception as e:
        raise Exception(f"ELA processing failed: {str(e)}")

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and ELA processing"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    # Check file size
    file.seek(0, 2)  # Seek to end of file
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if file_size > MAX_FILE_SIZE:
        flash(f'File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB')
        return redirect(request.url)
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload: PNG, JPG, JPEG, GIF, BMP, TIFF, or WebP')
        return redirect(request.url)
    
    try:
        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_filename = secure_filename(file.filename)
        base_name = os.path.splitext(original_filename)[0]
        extension = os.path.splitext(original_filename)[1]
        
        filename = f"{timestamp}_{unique_id}_{base_name}{extension}"
        
        # Save uploaded file temporarily
        temp_filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_filepath)
        
        # Convert original to JPEG in memory and get base64
        with Image.open(temp_filepath) as img:
            img = img.convert('RGB')
            img_io = io.BytesIO()
            img.save(img_io, 'JPEG', quality=95)
            img_io.seek(0)
            original_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
            original_data_url = f"data:image/jpeg;base64,{original_base64}"
        
        # Process with ELA
        ela_diff, ela_amplified = convert_to_ela_image_ps7(temp_filepath)
        
        # Analyze ELA statistics
        report = analyze_ela_statistics(ela_diff)
        
        # Convert ELA result to JPEG in memory and get base64
        ela_io = io.BytesIO()
        ela_amplified.save(ela_io, 'JPEG', quality=95)
        ela_io.seek(0)
        ela_base64 = base64.b64encode(ela_io.getvalue()).decode('utf-8')
        ela_data_url = f"data:image/jpeg;base64,{ela_base64}"
        
        # Clean up uploaded file
        os.remove(temp_filepath)
        
        # Render page with base64 data URLs and report
        return render_template('result.html', 
                             original_name=original_filename,
                             original_image=original_data_url,
                             result_image=ela_data_url,
                             report=report,
                             timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
    except Exception as e:
        # Clean up uploaded file if error occurs
        try:
            if 'temp_filepath' in locals() and os.path.exists(temp_filepath):
                os.remove(temp_filepath)
        except:
            pass
            
        flash(f'Error processing image: {str(e)}')
        return redirect(url_for('index'))

@app.route('/about')
def about():
    """About page explaining ELA"""
    return render_template('about.html')

@app.route('/static/results/<filename>')
def serve_result_file(filename):
    """Serve ELA results from the temporary directory"""
    return send_file(os.path.join(RESULTS_FOLDER, filename))

@app.route('/static/originals/<filename>')
def serve_original_file(filename):
    """Serve original uploaded images from the temporary directory"""
    return send_file(os.path.join(ORIGINALS_FOLDER, filename))

@app.route('/download/<path:folder>/<filename>')
def download_file(folder, filename):
    """Download file from specified folder (results or originals)"""
    try:
        if folder == 'results':
            file_path = os.path.join(RESULTS_FOLDER, filename)
        elif folder == 'originals':
            file_path = os.path.join(ORIGINALS_FOLDER, filename)
        else:
            flash('Invalid download request')
            return redirect(url_for('index'))
        
        if not os.path.exists(file_path):
            flash('File not found')
            return redirect(url_for('index'))
            
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        flash(f'Download error: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)