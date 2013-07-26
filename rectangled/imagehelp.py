from PIL import Image
import datehelp


def open_image(path):
    image = Image.open(path)
    # convert to grayscale for github (greenscale?)
    image = image.convert("L")
    # and resize to 52x7
    image.thumbnail((52, 7), Image.ANTIALIAS)
    return image


def convert_pixel(pixel, colors=4):
    '''Invert a pixel's color and convert the color to a value of 0 to 4
    Pixel should be a value of "L" mode from PIL (one value, not three).
    '''

    # higher value = darker for github
    inverted = 255 - pixel  # as opposed to pixels, where higher = lighter
    # reduce the 8 bit color depth to HubColor(tm) (7th grade algebra style)
    reduced = int(round(inverted * colors / 255.0))
    return reduced


def colors_for_column(week, image, start_date):
    '''week: a value from 0 to 51, relative to the origin date
    image: the image that is being converted
    start_date: date to start at

    returns a dict, where key = date and value = color
    '''

    weekdates = datehelp.dates_for_column(week, start_date)

    colors = {}
    imgcolumn = week
    imgrow = 0  # 0 is top, max is bottom
    for day in weekdates:
        pixel = (week, imgrow)
        realcolor = image.getpixel(pixel)
        hubcolor = convert_pixel(realcolor)

        colors[day] = hubcolor
        imgrow += 1

    return colors
