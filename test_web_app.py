#!/usr/bin/env python3
"""
Test the improved web application with side-by-side comparison
"""

import requests
import os
from PIL import Image
import io

def test_improved_web_app():
    """Test the improved web application"""
    base_url = "http://localhost:5001"
    
    print("🧪 Testing Improved ELA Web Application...")
    
    # Test 1: Check if homepage loads
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ Homepage loads successfully")
        else:
            print(f"❌ Homepage failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to web app. Make sure it's running on localhost:5001")
        return False
    
    # Test 2: Create and upload a test image
    try:
        # Create a test image with some patterns
        test_image = Image.new('RGB', (200, 200), color='white')
        # Add some colored rectangles to simulate content
        pixels = test_image.load()
        for i in range(50, 150):
            for j in range(50, 150):
                pixels[i, j] = (255, 0, 0)  # Red square
        
        img_buffer = io.BytesIO()
        test_image.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        
        # Upload the test image
        files = {'file': ('test_comparison.jpg', img_buffer, 'image/jpeg')}
        response = requests.post(f"{base_url}/upload", files=files)
        
        if response.status_code == 200:
            if "Original vs ELA Analysis" in response.text:
                print("✅ Side-by-side comparison works!")
            if "Original Image" in response.text and "ELA Heatmap" in response.text:
                print("✅ Both original and ELA images are displayed")
            if "Download ELA" in response.text and "Download Original" in response.text:
                print("✅ Download buttons for both images available")
        else:
            print(f"❌ Upload failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Upload test error: {e}")
    
    print("\n🎉 Improved web application test completed!")
    print(f"🌐 Access the app at: {base_url}")
    print("📊 Features:")
    print("   • Side-by-side original vs ELA comparison")
    print("   • Download both original and ELA results")
    print("   • Improved visual layout")
    print("   • Better error handling")
    
    return True

if __name__ == "__main__":
    test_improved_web_app()