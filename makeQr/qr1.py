import qrcode
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

dico = {
    "blue": (0,0,238),
    "red": (238,59,59),
    "green": (102,205,0),
    "yellow":(255,215,0),
    "purple": (154,50,205),
    "black":(3,3,3),
    "white": (205,200,177),
    "brown":(139,35,35),
    "orange":(255,127,0)
}

def generateQrImg(color, action):
    input_data = color + " " + action
    qr = qrcode.QRCode(
            version=1,
            box_size=15,
            border=5)
    qr.add_data(input_data)
    qr.make(fit=True)
    img1 = qr.make_image(fill='black', back_color='white')
    img = Image.new("RGBA", img1.size)
    img.paste(img1)
    W, H = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font.ttf",30)
    message = input_data
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)/2, 20), message, font=font, fill=dico[color])
    return img

imL = [[], []]
l = len(dico.keys())
dst = None
i=0
for c in dico.keys():
    im1 = generateQrImg(c, "PICK")
    im2 = generateQrImg(c, "DROP")
    if dst == None:
        dst = Image.new('RGB', (im1.width*l, im1.height*2))
    imL[0].append(im1)
    imL[1].append(im2)
    dst.paste(im1, (i*im1.width, 0))
    dst.paste(im2, (i*im1.width, im1.height))
    i+=1

dst.save("qrcode001.png")