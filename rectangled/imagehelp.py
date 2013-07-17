import datehelp


def convert_pixel(pixel, colors=4):
    '''Invert a pixel's color and convert the color to a value of 0 to 4
    Pixel should be a value of "L" mode from PIL (one value, not three).
    '''

    # higher value = darker for github
    inverted = 255 - pixel  # as opposed to pixels, where higher = lighter
    # reduce the 8 bit color depth to HubColor(tm) (7th grade algebra style)
    reduced = int(round(inverted * colors / 255.0))
    return reduced

def colors_for_column(week, image):
    '''week: a value from 0 to 51, relative to the origin date
    image: the image that is being converted
    
    returns a dict, where key = date and value = color
    '''

    weekdates = datehelp.dates_for_column(week)
    
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
