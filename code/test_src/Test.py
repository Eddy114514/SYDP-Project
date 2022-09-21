from PIL import Image, ImageOps
im = Image.open(r"test_src1.png")
flip = ImageOps.mirror(im)
flip.save('test_src_flip.png')





