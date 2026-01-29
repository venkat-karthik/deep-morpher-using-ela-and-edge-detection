#!/usr/bin/env python3
"""
Demo script to showcase all enhanced ELA features
"""

import os
import sys
from pathlib import Path

def run_demo():
    """Run comprehensive demo of enhanced ELA features"""
    
    print("🚀 Enhanced ELA Analysis Demo")
    print("=" * 50)
    
    # Check if sample image exists
    sample_image = "input/suspect_frame.jpg"
    if not os.path.exists(sample_image):
        print(f"❌ Sample image not found: {sample_image}")
        print("Please ensure you have a test image in the input/ folder")
        return
    
    print(f"📸 Using sample image: {sample_image}")
    print("\n🔍 Running Enhanced ELA Analysis...")
    print("This will demonstrate all Tier 1, 2, and 3 features:")
    print("  ✅ Heatmap + Bounding Box detection")
    print("  ✅ Side-by-side professional output")
    print("  ✅ Quality sweep mode (85%, 90%, 95%)")
    print("  ✅ Inconsistency scoring")
    print("  ✅ JPEG block-grid visualization")
    
    # Run enhanced analysis
    os.system(f"python run_ps7_enhanced.py {sample_image} demo_output")
    
    print("\n🎯 Demo Complete!")
    print("📁 Check the 'demo_output' folder for:")
    print("   📊 complete_analysis_summary.jpg - Full overview")
    print("   📂 quality_85/ quality_90/ quality_95/ - Detailed analysis")
    print("   📈 analysis_report.txt files - Metrics and scores")
    print("   🎨 Various visualization types")
    
    print("\n💡 Key Features Demonstrated:")
    print("   🔥 Red bounding boxes = Suspicious regions")
    print("   📊 Inconsistency scores = Tampering likelihood")
    print("   🎨 Block grids = JPEG compression patterns")
    print("   🔄 Multi-quality = Robust detection")

if __name__ == "__main__":
    run_demo()