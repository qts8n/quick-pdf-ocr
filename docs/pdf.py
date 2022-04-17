import cv2
import numpy as np

_DTYPE = np.dtype('uint8')
_DTYPE.newbyteorder('=')


def page_to_image(page):
    page_pixmap = page.get_pixmap(dpi=144)
    c_channel_num = 4 if page_pixmap.alpha else 3
    shape = page_pixmap.height, page_pixmap.width, c_channel_num
    np_buffer = np.frombuffer(page_pixmap.samples, dtype=_DTYPE)
    image = np.reshape(np_buffer, shape)
    if c_channel_num == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    return image


def page_to_content(page, reader):
    page_image = page_to_image(page)
    content = reader.readtext(page_image, detail=0, paragraph=True)
    return ' '.join(content)
