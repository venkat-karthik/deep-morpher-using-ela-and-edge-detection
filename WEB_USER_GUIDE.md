# 🌐 ELA Web Application - User Guide

## 🚀 **Getting Started**

### **1. Launch the Application**
```bash
# Install dependencies (one-time setup)
pip install -r requirements.txt

# Start the web server
python app.py
```

### **2. Open Your Browser**
Navigate to: **http://localhost:5000**

---

## 📱 **Complete User Flow**

### **🏠 Homepage (Upload Interface)**

#### **Step 1: Select Your Image**
- **Method 1:** Click "Choose File" button
- **Method 2:** Drag & drop image directly onto the upload area
- **Supported formats:** PNG, JPG, JPEG, GIF, BMP, TIFF, WebP
- **File size limit:** 16MB maximum

#### **Step 2: Preview & Validate**
- Image preview appears automatically
- File validation happens in real-time
- Error messages show for invalid files

#### **Step 3: Start Analysis**
- Click "Analyze Image" button
- Processing modal appears with spinner
- ELA algorithm runs automatically (PS-7 compliant)

---

### **📊 Results Page**

#### **What You'll See:**
1. **ELA Heatmap:** The processed image showing error levels
2. **Original filename:** Name of your uploaded image
3. **Processing timestamp:** When the analysis was completed
4. **Action buttons:** Download, analyze another, or learn more

#### **How to Interpret Results:**
- 🔥 **Bright/White areas:** High error levels = Potential tampering
- 🌑 **Dark/Black areas:** Low error levels = Likely authentic
- 📊 **Uniform patterns:** Consistent throughout = Probably authentic

---

### **📚 About Page**

#### **Educational Content:**
- Complete explanation of Error Level Analysis
- Step-by-step algorithm breakdown
- PS-7 compliance details
- Interpretation guidelines
- Limitations and considerations
- Common use cases

---

## 🎯 **Real-World Usage Examples**

### **Example 1: Social Media Verification**
```
1. Save suspicious profile photo from social media
2. Upload to ELA web app
3. Look for bright regions around face/body
4. Bright areas may indicate face swapping or editing
```

### **Example 2: News Photo Authentication**
```
1. Upload news image that seems suspicious
2. Analyze with ELA
3. Check for inconsistent compression patterns
4. Bright areas might indicate photo manipulation
```

### **Example 3: Online Marketplace**
```
1. Upload product photos from listings
2. Look for editing artifacts
3. Bright regions could indicate enhanced/fake features
4. Use results to assess listing authenticity
```

---

## 🔧 **Advanced Features**

### **File Handling**
- **Automatic validation:** File type and size checking
- **Secure processing:** Temporary files are cleaned up
- **Error recovery:** Graceful handling of processing errors
- **Cross-platform:** Works on Windows, Mac, Linux

### **User Experience**
- **Responsive design:** Works on desktop, tablet, mobile
- **Real-time feedback:** Instant validation and previews
- **Progress indicators:** Loading animations during processing
- **Accessibility:** Screen reader friendly, keyboard navigation

### **Security Features**
- **File type whitelist:** Only image formats allowed
- **Size limits:** Prevents server overload
- **Secure uploads:** Protected against malicious files
- **No data retention:** Files deleted after processing

---

## 🚨 **Troubleshooting**

### **Common Issues & Solutions**

#### **"File too large" Error**
- **Problem:** Image exceeds 16MB limit
- **Solution:** Resize image or use compression tool

#### **"Invalid file type" Error**
- **Problem:** Unsupported file format
- **Solution:** Convert to JPG, PNG, or other supported format

#### **Processing Fails**
- **Problem:** Corrupted or invalid image file
- **Solution:** Try a different image or check file integrity

#### **Page Won't Load**
- **Problem:** Web server not running
- **Solution:** Run `python app.py` and check console for errors

#### **Slow Processing**
- **Problem:** Large image taking time to process
- **Solution:** Wait for completion or use smaller image

---

## 📊 **Performance Guidelines**

### **Optimal Image Sizes**
- **Small (< 1MB):** ~1-2 seconds processing
- **Medium (1-5MB):** ~2-5 seconds processing  
- **Large (5-16MB):** ~5-10 seconds processing

### **Best Practices**
- Use images under 5MB for faster results
- JPG format typically processes fastest
- Close other browser tabs during processing
- Ensure stable internet connection

---

## 🎨 **Interface Guide**

### **Navigation Bar**
- **Home:** Return to upload page
- **About ELA:** Learn about the algorithm

### **Upload Page Elements**
- **File selector:** Choose or drag files
- **Preview area:** See your image before processing
- **Analyze button:** Start ELA processing
- **How it works:** Algorithm explanation

### **Results Page Elements**
- **ELA heatmap:** Main analysis result
- **Download button:** Save result to computer
- **Analyze another:** Process new image
- **Interpretation guide:** How to read results

---

## 🔄 **Workflow Tips**

### **For Best Results**
1. **Use high-quality source images**
2. **Avoid heavily compressed images**
3. **Compare suspicious images with known authentic ones**
4. **Look for patterns, not just individual bright spots**
5. **Consider the context of the image**

### **Multiple Image Analysis**
1. Process several images from same source
2. Compare ELA patterns between them
3. Look for consistency in authentic images
4. Note differences in suspicious images

---

## 🎯 **Success Indicators**

### **You're Using It Right When:**
- ✅ Images upload without errors
- ✅ Processing completes successfully
- ✅ You can interpret bright vs dark regions
- ✅ Results help inform your analysis
- ✅ You understand the limitations

### **Expected Learning Curve**
- **Beginner:** Can upload and get results (5 minutes)
- **Intermediate:** Can interpret basic patterns (30 minutes)
- **Advanced:** Can spot subtle manipulation signs (hours of practice)

---

**🎉 The web interface makes professional-grade ELA analysis accessible to everyone - no technical expertise required!**