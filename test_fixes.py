#!/usr/bin/env python3
"""
Test script to verify all fixes are working correctly
"""

import os
import sys
from PIL import Image
import tempfile

def test_ela_algorithm():
    """Test the ELA algorithm directly"""
    print("🧪 Testing ELA Algorithm...")
    
    try:
        # Import the function
        sys.path.append('.')
        from run_ps7 import convert_to_ela_image_ps7
        
        # Create a test image
        test_img = Image.new('RGB', (100, 100), color='red')
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            test_img.save(tmp.name, 'JPEG', quality=95)
            
            # Test ELA
            result = convert_to_ela_image_ps7(tmp.name)
            
            if result and result.size == (100, 100):
                print("✅ ELA algorithm working correctly")
            else:
                print("❌ ELA algorithm failed")
                return False
                
            # Cleanup
            os.unlink(tmp.name)
            
    except Exception as e:
        print(f"❌ ELA test failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test required directories exist"""
    print("🧪 Testing File Structure...")
    
    required_dirs = [
        'static',
        'static/results',
        'static/originals',
        'static/css',
        'static/js',
        'templates',
        'uploads'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} exists")
        else:
            print(f"❌ {dir_path} missing")
            return False
    
    return True

def test_required_files():
    """Test all required files exist"""
    print("🧪 Testing Required Files...")
    
    required_files = [
        'app.py',
        'run_ps7.py',
        'requirements.txt',
        'templates/base.html',
        'templates/index.html',
        'templates/result.html',
        'templates/about.html',
        'static/css/style.css',
        'static/js/main.js'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    return True

def test_imports():
    """Test all required imports work"""
    print("🧪 Testing Python Imports...")
    
    try:
        from PIL import Image, ImageChops, ImageEnhance
        print("✅ Pillow imports working")
        
        from flask import Flask, render_template, request, send_file, flash, redirect, url_for
        print("✅ Flask imports working")
        
        from werkzeug.utils import secure_filename
        print("✅ Werkzeug imports working")
        
        import uuid, datetime, tempfile, os, sys
        print("✅ Standard library imports working")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    return True

def test_app_syntax():
    """Test Flask app syntax"""
    print("🧪 Testing Flask App Syntax...")
    
    try:
        import app
        print("✅ Flask app imports without syntax errors")
        
        # Check if key functions exist
        if hasattr(app, 'convert_to_ela_image_ps7'):
            print("✅ ELA function exists in app")
        else:
            print("❌ ELA function missing in app")
            return False
            
        if hasattr(app, 'upload_file'):
            print("✅ Upload function exists")
        else:
            print("❌ Upload function missing")
            return False
            
        if hasattr(app, 'download_file'):
            print("✅ Download function exists")
        else:
            print("❌ Download function missing")
            return False
            
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Running Comprehensive Error Check...\n")
    
    tests = [
        test_file_structure,
        test_required_files,
        test_imports,
        test_app_syntax,
        test_ela_algorithm
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Empty line between tests
    
    print("=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your application is ready to run!")
        print("\n🚀 To start the web app:")
        print("   python3 app.py")
        print("\n🌐 Then visit: http://localhost:5001")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return False
    
    return True

if __name__ == "__main__":
    main()