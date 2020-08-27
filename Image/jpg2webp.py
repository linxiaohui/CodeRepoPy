from PIL import Image
def save_image(input_name, output_name):
    im = Image.open(input_name)
    if im.mode=="RGBA":
        im.load()  # required for png.split()
        background = Image.new("RGB", im.size, (255, 255, 255))
        background.paste(im, mask=im.split()[3])  # 3 is the alpha channel
        im = background
    im.save('{}.webp'.format(output_name),'WEBP')

save_image("a.jpg","x")


