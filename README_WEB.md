# 🌐 ELA Image Forgery Detection - Web Application

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Web Application
```bash
python app.py
```

### 3. Open Your Browser
Navigate to: **http://localhost:5000**

## 📱 How to Use the Web Interface

### **Step 1: Upload Image**
1. Click "Choose File" or drag & drop an image
2. Supported formats: PNG, JPG, JPEG, GIF, BMP, TIFF, WebP
3. Maximum file size: 16MB
4. Preview will appear automatically

### **Step 2: Analyze**
1. Click "Analyze Image" button
2. Processing modal will appear
3. ELA algorithm runs automatically (PS-7 compliant)

### **Step 3: View Results**
1. ELA heatmap is displayed
2. Bright areas = Potential tampering
3. Dark areas = Likely authentic
4. Download results or analyze another image

## 🎯 Features

### **User-Friendly Interface**
- ✅ Drag & drop file upload
- ✅ Real-time image preview
- ✅ Progress indicators
- ✅ Responsive design (mobile-friendly)
- ✅ Bootstrap 5 UI components

### **Advanced Functionality**
- ✅ PS-7 compliant ELA algorithm
- ✅ Automatic file validation
- ✅ Secure file handling
- ✅ Result download capability
- ✅ Comprehensive interpretation guide

### **Error Handling**
- ✅ File size validation (16MB max)
- ✅ File type validation
- ✅ Processing error recovery
- ✅ User-friendly error messages

## 🔧 Technical Details

### **Backend (Flask)**
- **Framework:** Flask 2.3+
- **Image Processing:** Pillow (PIL)
- **File Handling:** Werkzeug secure uploads
- **Security:** CSRF protection, file validation

### **Frontend**
- **UI Framework:** Bootstrap 5
- **Icons:** Font Awesome 6
- **JavaScript:** Vanilla JS with modern features
- **Responsive:** Mobile-first design

### **File Structure**
```
ImageForgeryDetection/
├── app.py                 # Flask application
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Upload page
│   ├── result.html       # Results page
│   └── about.html        # About ELA page
├── static/               # Static assets
│   ├── css/style.css     # Custom styles
│   ├── js/main.js        # JavaScript functionality
│   └── results/          # Generated ELA images
├── uploads/              # Temporary upload folder
└── requirements.txt      # Python dependencies
```

## 🛡️ Security Features

### **File Upload Security**
- File type validation (whitelist approach)
- File size limits (16MB maximum)
- Secure filename handling
- Temporary file cleanup
- No executable file uploads

### **Processing Security**
- Input sanitization
- Error handling and recovery
- Memory management
- Temporary file isolation

## 🌍 Deployment Options

### **Local Development**
```bash
python app.py
# Access: http://localhost:5000
```

### **Production Deployment**
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker (create Dockerfile)
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

### **Cloud Deployment**
- **Heroku:** Ready for deployment
- **AWS/GCP:** Compatible with cloud platforms
- **Docker:** Containerization ready

## 📊 Performance

### **Processing Speed**
- Small images (< 1MB): ~1-2 seconds
- Medium images (1-5MB): ~2-5 seconds
- Large images (5-16MB): ~5-10 seconds

### **Scalability**
- Single-threaded processing
- Memory efficient
- Suitable for moderate traffic
- Can be scaled with load balancers

## 🎨 Customization

### **UI Customization**
- Modify `static/css/style.css` for styling
- Edit templates for layout changes
- Add new pages by creating templates
- Customize colors, fonts, and branding

### **Algorithm Customization**
- Modify `convert_to_ela_image_ps7()` function
- Add new analysis methods
- Implement batch processing
- Add result comparison features

## 🐛 Troubleshooting

### **Common Issues**

**Port Already in Use:**
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

**File Upload Fails:**
- Check file size (< 16MB)
- Verify file format is supported
- Ensure sufficient disk space

**Processing Errors:**
- Check image file integrity
- Verify Pillow installation
- Review error logs in console

### **Debug Mode**
```bash
# Enable debug mode for development
export FLASK_DEBUG=1
python app.py
```

## 📈 Future Enhancements

### **Planned Features**
- [ ] Batch image processing
- [ ] User accounts and history
- [ ] API endpoints for integration
- [ ] Advanced analysis options
- [ ] Result comparison tools
- [ ] Export to PDF reports

### **Technical Improvements**
- [ ] Async processing with Celery
- [ ] Database integration
- [ ] Caching for faster results
- [ ] WebSocket for real-time updates
- [ ] Progressive web app (PWA)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**🎯 The web interface makes ELA analysis accessible to everyone - no command line required!**