import requests
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

from resources import res_path


def generate_meme_from_text(text: str=None, img_url: str=None):
    try:
        if not text or ';' not in text:
            text = "did you do it right? format is;top;bottom|img url"
        top, bottom = text.split(';', maxsplit=1)
        img = None
        if img_url:
            resp = requests.get(img_url)
            if resp.status_code == 200 and (resp.headers.get("content-type", "")
                                            in ("image/png", "image/jpeg", "image/webp")):
                img = Image.open(BytesIO(resp.content))
        if not img:
            img = Image.open(res_path + "bear-10.jpg")
        if not img:
            return None

        draw = ImageDraw.Draw(img)
        draw_text(top, "top", img, draw)
        draw_text(bottom, "bottom", img, draw)
        with BytesIO() as result:
            img.save(result, format('PNG'))
            return result.getvalue()
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print("NOTE: " + exc)
        pass
    return None


def draw_text(msg, pos, img, draw):
    font_size = img.height // 8
    lines = []

    font = ImageFont.truetype(res_path + "impact.ttf", font_size)
    w, h = draw.textsize(msg, font)

    img_width_with_padding = img.width * 0.99

    # 1. how many lines for the msg to fit ?
    line_count = 1
    if w > img_width_with_padding:
        line_count = int(round((w / img_width_with_padding) + 1))

    if line_count > 2:
        while 1:
            font_size -= 2
            font = ImageFont.truetype("impact.ttf", font_size)
            w, h = draw.textsize(msg, font)
            line_count = int(round((w / img_width_with_padding) + 1))
            print("try again with font_size={} => {}".format(font_size, line_count))
            if line_count < 3 or font_size < 10:
                break

    print("img.width: {}, text width: {}".format(img.width, w))
    print("Text length: {}".format(len(msg)))
    print("Lines: {}".format(line_count))

    # 2. divide text in X lines
    last_cut = 0
    is_last = False
    for i in range(0, line_count):
        if last_cut == 0:
            cut = int((len(msg) / line_count) * i)
        else:
            cut = last_cut

        if i < line_count-1:
            next_cut = int((len(msg) / line_count) * (i+1))
        else:
            next_cut = len(msg)
            is_last = True

        print("cut: {} -> {}".format(cut, next_cut))

        # make sure we don't cut words in half
        if next_cut == len(msg) or msg[next_cut] == " ":
            print("may cut")
        else:
            if " " in msg:
                print("may not cut")
                while msg[next_cut] != " ":
                    next_cut += 1
                print("new cut: {}".format(next_cut))

        line = msg[cut:next_cut].strip()

        # is line still fitting ?
        w, h = draw.textsize(line, font)
        if not is_last and w > img_width_with_padding:
            print("overshot")
            next_cut -= 1
            while msg[next_cut] != " ":
                next_cut -= 1
            print("new cut: {}".format(next_cut))

        last_cut = next_cut
        lines.append(msg[cut:next_cut].strip())

    print(lines)

    # 3. print each line centered
    last_y = -h
    if pos == "bottom":
        last_y = img.height - h * (line_count+1) - 10

    thicc = 4
    for i in range(0,line_count):
        w, h = draw.textsize(lines[i], font)
        text_x = img.width/2 - w/2
        #  if pos == "top":
        #    textY = h * i
        #  else:
        #    textY = img.height - h * i
        text_y = last_y + h
        draw.text((text_x-thicc, text_y-thicc), lines[i], (0,0,0), font=font)
        draw.text((text_x+thicc, text_y-thicc), lines[i], (0,0,0), font=font)
        draw.text((text_x+thicc, text_y+thicc), lines[i], (0,0,0), font=font)
        draw.text((text_x-thicc, text_y+thicc), lines[i], (0,0,0), font=font)
        draw.text((text_x - thicc, text_y), lines[i], (0, 0, 0), font=font)
        draw.text((text_x + thicc, text_y), lines[i], (0, 0, 0), font=font)
        draw.text((text_x, text_y - thicc), lines[i], (0, 0, 0), font=font)
        draw.text((text_x, text_y + thicc), lines[i], (0, 0, 0), font=font)
        draw.text((text_x, text_y), lines[i], (255, 255, 255), font=font)
        last_y = text_y
    return
