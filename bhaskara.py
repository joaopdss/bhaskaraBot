from PIL import Image, ImageDraw
import math

def make_put_bhaskara(a, b, c, img):
    txt = f"x = -({b}) ± raiz de {b}² - 4 * {a} * {c}"
    img.text((10, 10), txt, fill=(0, 67, 98))
    txt = f"           2 * {a}"
    img.text((10, 25), txt, fill=(0, 67, 98))
    delta = (b ** 2) - 4 * a * c
    n1 = 2 * a
    n2 = -b

    txt = f"x = {n2} ± raiz de {delta}"
    img.text((10, 45), txt, fill=(0, 67, 98))
    txt = f"       {n1}"
    img.text((10, 60), txt, fill=(0, 67, 98))

    n3 = float("{0:.2f}".format(math.sqrt(delta)))
    x1 = (n2 + n3) / n1
    x2 = (n2 - n3) / n1

    if len(str(n3).split(".")[1]) == 1:
        n3 = str(n3).split(".")[0]
        print(n3)

    txt = f"x¹ = {n2} + {str(n3).replace('.', ',')} = {str('{0:.2f}'.format(x1)).replace('.', ',')}"
    img.text((10, 80), txt, fill=(0, 67, 98))
    txt = f"       {n1}\n"
    img.text((10, 95), txt, fill=(0, 67, 98))
    txt = f"x² = {n2} - {str(n3).replace('.', ',')} = {str('{0:.2f}'.format(x2)).replace('.', ',')}"
    img.text((10, 115), txt, fill=(0, 67, 98))
    txt = f"       {n1}"
    img.text((10, 130), txt, fill=(0, 67, 98))
    txt = "S = {" + f"{str('{0:.2f}'.format(x1)).replace('.', ',')} , {str('{0:.2f}'.format(x2)).replace('.', ',')}" + "}"
    img.text((10, 150), txt, fill=(0, 67, 98))