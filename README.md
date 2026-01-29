# Image Forgery Detection Project - Enhanced Edition

![build-passing](https://img.shields.io/badge/build-passing-brightgreen) ![test-passing](https://img.shields.io/badge/test-passing-brightgreen) ![enhanced](https://img.shields.io/badge/enhanced-forensics-blue)

## 🚀 Enhanced Features Overview

This project now includes **professional-grade forensics capabilities** with advanced ELA analysis:

### ✅ **Tier 1 Features (High Impact)**
- **🎯 Automatic Suspicious Region Detection** - Red bounding boxes highlight tampered areas
- **📊 Professional Side-by-Side Output** - Original | Recompressed | ELA | Regions
- **🔄 Quality Sweep Mode** - Tests multiple JPEG qualities (85%, 90%, 95%) for robust detection

### ✅ **Tier 2 Features (Advanced Analysis)**  
- **📹 Video Support** - Frame-by-frame ELA analysis for deepfake detection
- **📈 Inconsistency Scoring** - Quantitative tampering likelihood (0-100 scale)

### ✅ **Tier 3 Features (Forensics-Grade)**
- **🎨 JPEG Block-Grid Visualization** - 8×8 compression pattern analysis

## 🎯 Quick Demo

```bash
# Install enhanced dependencies
pip install -r requirements.txt

# Run comprehensive demo
python demo_enhanced.py

# Or analyze any image with full features
python run_ps7_enhanced.py input/suspect.jpg enhanced_output
```

## 📊 Enhanced Output Examples

### Professional Analysis Output:
- **complete_analysis_summary.jpg** - Multi-quality comparison overview
- **quality_XX/** folders - Detailed analysis per JPEG quality
- **side_by_side_analysis.jpg** - 4-panel professional comparison
- **suspicious_regions.jpg** - Original with red bounding boxes
- **block_grid_analysis.jpg** - JPEG compression pattern visualization
- **analysis_report.txt** - Quantitative metrics and scores

## 🔍 Enhanced User Flow

### **Basic Analysis (Original)**
```bash
python run_ps7.py input/image.jpg output/result.jpg
```

### **Enhanced Analysis (New)**
```bash
python run_ps7_enhanced.py input/image.jpg enhanced_output/
```

**Enhanced Output Includes:**
- 🎯 **Automatic region detection** with bounding boxes
- 📊 **Professional 4-panel comparison** 
- 🔄 **Multi-quality analysis** (85%, 90%, 95%)
- 📈 **Inconsistency scores** and metrics
- 🎨 **JPEG block visualization**

### **Video Analysis (Deepfake Detection)**
```bash
python run_ps7_enhanced.py suspicious_video.mp4 video_analysis/
```

## 📈 Interpretation Guide

### **Inconsistency Score (0-100)**
- **0-20**: Likely authentic
- **21-50**: Moderate suspicion  
- **51-80**: High suspicion
- **81-100**: Very likely tampered

### **Visual Indicators**
- 🔥 **Bright regions** in ELA heatmap = Compression inconsistencies
- 📦 **Red bounding boxes** = Automatically detected suspicious areas
- 🎨 **Block patterns** = JPEG compression artifact analysis
- 📊 **Side-by-side** = Professional comparison view

## 🛠️ Technical Enhancements

### **Algorithm Improvements**
- **Multi-quality sweep** for robust detection
- **Contour-based region detection** with area filtering
- **Statistical inconsistency scoring** 
- **JPEG block-aware analysis**

### **Professional Output**
- **Automated bounding box detection**
- **4-panel comparison layouts**
- **Quantitative reporting**
- **Video frame extraction and analysis**

## 📁 Enhanced Repository Structure
```
.
├── input/                          # Test images
├── enhanced_output/                # Enhanced analysis results
│   ├── complete_analysis_summary.jpg
│   ├── quality_85/
│   │   ├── ela_heatmap.jpg
│   │   ├── suspicious_regions.jpg
│   │   ├── side_by_side_analysis.jpg
│   │   ├── block_grid_analysis.jpg
│   │   └── analysis_report.txt
│   ├── quality_90/ 
│   └── quality_95/
├── run_ps7.py                      # Original PS-7 compliant
├── run_ps7_enhanced.py             # Enhanced forensics version
├── demo_enhanced.py                # Comprehensive demo
└── requirements.txt                # Updated dependencies

```

## 🎓 Original PS-7 Compliance

### Why Error Level Analysis (ELA)?
Deepfake or forged regions are often re-compressed at a different quality than the original image. When an image is recompressed uniformly and subtracted from the original, manipulated regions exhibit higher error levels. ELA visualizes these inconsistencies without relying on metadata.

**Interpretation**: Brighter/hotter regions in the ELA heatmap indicate higher compression inconsistency and potential tampering.

## How to Run
```bash
pip install -r requirements.txt
python run_ps7.py input/suspect_frame.jpg output/ela_result.jpg
```

## PS-7 Compliance
Implements fixed JPEG recompression at quality=90, absolute difference, and brightness amplification per the PS-7 hint.

### PS-7 Implementation Details
The repository includes a PS-7 compliant ELA function (`run_ps7.py`) that strictly follows the official hint:
1. **Load original image** - Uses PIL to load and convert to RGB
2. **Save as JPEG with 90% quality** - Fixed quality parameter as required
3. **Reload compressed image** - Loads the recompressed version
4. **Compute absolute difference** - Pixel-wise subtraction using ImageChops
5. **Amplify brightness** - Normalizes and enhances visibility of differences

## Dependencies
- Python 3.x
- Pillow (PIL)
- OpenCV (enhanced version)
- NumPy (enhanced version)

## Installation
Clone the repository:
```sh
git clone https://github.com/ShivamGupta92/ImageForgeryDetection.git
```

Navigate to the project directory:
```sh
cd ImageForgeryDetection
```

Install required dependencies:
```sh
pip install -r requirements.txt
```

## Results
The enhanced version provides comprehensive forensics analysis with professional-grade visualizations and quantitative metrics for detecting image tampering and deepfake content.
