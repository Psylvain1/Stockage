#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 18:26:23 2025

@author: ssppa
"""
    
#!/usr/local/bin/python3
import numpy as np
from PIL import Image, ImageDraw

# Open the input image as numpy array, convert to RGB
img=Image.open("chatJLcrop.png").convert("L")
npImage=np.array(img)
h,w=img.size


# Create same size alpha layer with circle
alpha = Image.new('L', img.size,0)
draw = ImageDraw.Draw(alpha)
draw.pieslice([0,0,min(h,w),min(h,w)],0,360,fill=255)

# Convert alpha Image to numpy array
npAlpha=np.array(alpha)

# Add alpha layer to RGB
npImage=np.dstack((npImage,npAlpha))

# Save with alpha
Image.fromarray(npImage).save('resultJL.png')