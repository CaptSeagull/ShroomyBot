import requests
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import logging

from resources import res_path


def generate_meme_from_text(text: str=None, img_url: str=None):
    try:
        if not text:
            logging.warning("No text entered")
            text = "did you do it right? format is;top;bottom|img url"
        if ';' not in text:
            top = text
            bottom = ""
        else:
            top, bottom = text.split(';', maxsplit=1)
        img = None
        if img_url:
            resp = requests.get(img_url)
            if resp.status_code == 200 and (resp.headers.get("content-type", "")
                                            in ("image/png",
                                                "image/jpeg",
                                                "image/gif",
                                                "image/webp")):
                img = Image.open(BytesIO(resp.content)).convert('RGBA')
        if not img:
            img = Image.open(res_path + "bear-10.jpg")
        if not img:
            return None

        # If image is too big, rezise
        desired_size = 480
        old_size = img.size
        ratio = float(desired_size) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        img = img.resize(new_size, Image.ANTIALIAS)

        draw = ImageDraw.Draw(img)
        logging.debug(draw_text(top, "top", img, draw))
        logging.debug(draw_text(bottom, "bottom", img, draw))
        with BytesIO() as result:
            img.save(result, format('PNG'), optimize=True)
            return result.getvalue()
    except Exception:
        logging.exception("Exception when generating a meme")
    return None


def draw_text(msg, pos, img, draw):
    log_string = ["Starting draw_text for: " + pos]

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
            font = ImageFont.truetype(res_path + "impact.ttf", font_size)
            w, h = draw.textsize(msg, font)
            line_count = int(round((w / img_width_with_padding) + 1))
            log_string.append("try again with font_size={} => {}".format(font_size, line_count))
            if line_count < 3 or font_size < 10:
                break

    log_string.append("img.width: {}, text width: {}".format(img.width, w))
    log_string.append("Text length: {}".format(len(msg)))
    log_string.append("Lines: {}".format(line_count))

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

        log_string.append("cut: {} -> {}".format(cut, next_cut))

        # make sure we don't cut words in half
        if next_cut == len(msg) or msg[next_cut] == " ":
            log_string.append("may cut")
        else:
            log_string.append("may not cut")
            try:
                while msg[next_cut] != " ":
                    next_cut += 1
                log_string.append("new cut: {}".format(next_cut))
            except IndexError:
                log_string.append("Cannot cut")
                next_cut -= 1

        line = msg[cut:next_cut].strip()

        # is line still fitting ?
        w, h = draw.textsize(line, font)
        if not is_last and w > img_width_with_padding:
            log_string.append("overshot")
            next_cut -= 1
            try:
                while msg[next_cut] != " ":
                    next_cut -= 1
                log_string.append("new cut: {}".format(next_cut))
            except IndexError:
                log_string.append("Overshot")
                next_cut += 1

        last_cut = next_cut
        lines.append(msg[cut:next_cut].strip())

    log_string.append(str(lines))

    # 3. print each line centered
    last_y = -h
    if pos == "bottom":
        last_y = img.height - h * (line_count+1) - 10

    thicc = 4
    for i in range(0, line_count):
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
    return '\n'.join(log_string)
