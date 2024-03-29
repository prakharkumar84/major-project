from PIL import Image, ImageEnhance
from PIL import Image
import numpy as np
import numpy
import os
import pywt
from Utils.createFolder import  create_image_folder
def max_ndarray(mat):
    return np.amax(mat) if type(mat).__name__ == 'ndarray' else 0


def extract_rgb_coeff(img):
    #Returns RGB dwt applied coefficients tuple Parameters
    (width, height) = img.size
    img = img.copy()
    mat_r = numpy.empty((width, height))
    mat_g = numpy.empty((width, height))
    mat_b = numpy.empty((width, height))
    for i in range(width):
        for j in range(height):
            (r, g, b) = img.getpixel((i, j))
            mat_r[i, j] = r
            mat_g[i, j] = g
            mat_b[i, j] = b
    coeffs_r = pywt.dwt2(mat_r, 'haar')
    coeffs_g = pywt.dwt2(mat_g, 'haar')
    coeffs_b = pywt.dwt2(mat_b, 'haar')
    return (coeffs_r, coeffs_g, coeffs_b)


def img_from_dwt_coeff(coeff_dwt):
    #Returns Image recreated from dwt coefficients Parameters
    (coeffs_r, coeffs_g, coeffs_b) = coeff_dwt
    cc = numpy.array((coeffs_r, coeffs_g, coeffs_b), dtype=object)
    (width, height) = (len(coeffs_r[0]), len(coeffs_r[0][0]))
    cARed = numpy.array(coeffs_r[0])
    # Channel Green
    cAGreen = numpy.array(coeffs_g[0])
    # Channel Blue
    cABlue = numpy.array(coeffs_b[0])
 # maxValue per channel par matrix
    cAMaxRed = max_ndarray(cARed)
    cAMaxGreen = max_ndarray(cAGreen)
    cAMaxBlue = max_ndarray(cABlue)
    # Image object init
    dwt_img = Image.new('RGB', (width, height), (0, 0, 20))
    # cA reconstruction
    for i in range(width):
        for j in range(height):
            R = cARed[i][j]
            R = (R/cAMaxRed)*100.0
            G = cAGreen[i][j]
            G = (G/cAMaxGreen)*100.0
            B = cABlue[i][j]
            B = (B/cAMaxBlue)*100.0
            new_value = (int(R), int(G), int(B))
            dwt_img.putpixel((i, j), new_value)
    return dwt_img

#loads image
def load_img(path):
    try:
        return Image.open(path)
    except IOError:
        return None
    

def running(file, ext):
    img = load_img(file)                                              #read image using PIL
    coef = extract_rgb_coeff(img)                                     #extract rbg coeff
    image = img_from_dwt_coeff(coef)                                  #rebuild image using rgb coeff
    return image                                                      #return image


def enhancer_(st,image, ext,hybrid):
    enhancer = ImageEnhance.Brightness(image)                         #creating a image brightness object
    image = enhancer.enhance(2)                                       # increase brightness
    file_enh = "final_dwt"+ext
    x = create_image_folder()                                         #creating image folder
    path = os.path.join(x, file_enh)                                  #creating image path
    image.save(path)
    if hybrid==False:                                                 #in case hybrid compression
        st.image(image, caption="DWT Image", width=500)
    elif hybrid:
        st.image(image, caption="HYBRID DCT-DWT Image", width=500)
    return path

#main function to call above functions
def custom_dwt(st, image, ext,hybrid=False):
    a = running(image, ext)
    b = enhancer_(st, a, ext,hybrid)  
    return b



