#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  2 21:20:17 2025

@author: ssppa
"""

from PIL import Image

def resize_image(input_path, output_path, size=(600, 600)):
    # Open the image
    img = Image.open(input_path)
    
    # Resize the image
    resized_img = img.resize(size, Image.LANCZOS)  # High-quality downsampling
    
    # Save the resized image
    resized_img.save(output_path)
    print(f"Image saved to {output_path} with size {size}")

# Example usage
input_image = "resultJL.png"       # Replace with your image file
output_image = "reshaped_JL.png"   # Output file name

resize_image(input_image, output_image)
