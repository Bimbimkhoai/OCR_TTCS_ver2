from pdf2image import convert_from_path
import cv2
from PIL import Image
pdfs = r"e3.pdf"
pages = convert_from_path(pdfs, 350)

i = 1
for page in pages:
    image_name = "Pagetest_" + str(i) + ".jpg"
    page.save(image_name, "JPEG")
    i = i + 1
