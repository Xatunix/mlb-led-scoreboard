from driver import graphics

import time

from PIL import Image

from data.time_formats import TIME_FORMAT_12H
from data.config.color import Color
from data.config.layout import Layout
from data.headlines import Headlines
from data.weather import Weather
from renderers import scrollingtext
from utils import center_text_position


x = 0
y = 0
z = 0
xo = 0
yo = 0
zo = 0
w = 0
o = 0
def render_offday_screen(
    canvas, layout: Layout, colors: Color, weather: Weather, headlines: Headlines, time_format, text_pos
):

    text_len = __render_news_ticker(canvas, layout, colors, headlines, text_pos)
    __render_clock(canvas, layout, colors, time_format)
    __render_weather(canvas, layout, colors, weather)
    return text_len


def __render_clock(canvas, layout, colors, time_format):
    time_format_str = "{}:%M".format(time_format)
    if time_format == TIME_FORMAT_12H:
        time_format_str += "%p"
    time_text = time.strftime(time_format_str)
    coords = layout.coords("offday.time")
    font = layout.font("offday.time")
    color = colors.graphics_color("offday.time")
    color2 = colors.graphics_color("default.background")
    text_x = center_text_position(time_text, coords["x"], font["size"]["width"])
    graphics.DrawText(canvas, font["font"], text_x, coords["y"], color, time_text)
    
    global x
    global y
    global z
    global xo
    global yo
    global zo
    global w
    global o
    if x < 32:
        graphics.DrawLine(canvas, 32-x, 31, x+32, 31, color)
        x += 1
    elif y < 32:
        y += 1
        graphics.DrawLine(canvas, 32-x, 31, x+32, 31, color)
        graphics.DrawLine(canvas, 0, 31-y, 0, 31, color)
        graphics.DrawLine(canvas, 63, 31-y, 63, 31, color)
    elif z <= 32:
        z += 1 
        graphics.DrawLine(canvas, 32-x, 31, x+32, 31, color)
        graphics.DrawLine(canvas, 0, 31-y, 0, 31, color)
        graphics.DrawLine(canvas, 63, 31-y, 63, 31, color)

        graphics.DrawLine(canvas, 0, 0, z, 0, color)
        graphics.DrawLine(canvas, 63, 0, 63-z, 0, color)
    elif w <= 2150:
        w += 1
        graphics.DrawLine(canvas, 32-x, 31, x+32, 31, color)
        graphics.DrawLine(canvas, 0, 31-y, 0, 31, color)
        graphics.DrawLine(canvas, 63, 31-y, 63, 31, color)

        graphics.DrawLine(canvas, 0, 0, z, 0, color)
        graphics.DrawLine(canvas, 63, 0, 63-z, 0, color)
    elif xo < 32:
        graphics.DrawLine(canvas, 32-x, 31, x+32, 31, color)
        graphics.DrawLine(canvas, 0, 31-y, 0, 31, color)
        graphics.DrawLine(canvas, 63, 31-y, 63, 31, color)

        graphics.DrawLine(canvas, 0, 0, z, 0, color)
        graphics.DrawLine(canvas, 63, 0, 63-z, 0, color)

        graphics.DrawLine(canvas, 32-xo, 31, xo+32, 31, color2)
        xo += 1
    elif yo < 32:
        yo += 1
        graphics.DrawLine(canvas, 0, 31-y, 0, 31, color)
        graphics.DrawLine(canvas, 63, 31-y, 63, 31, color)
        graphics.DrawLine(canvas, 0, 0, z, 0, color)
        graphics.DrawLine(canvas, 63, 0, 63-z, 0, color)

        graphics.DrawLine(canvas, 0, 31-yo, 0, 31, color2)
        graphics.DrawLine(canvas, 63, 31-yo, 63, 31, color2)
    elif zo <= 32:
        zo += 1
        graphics.DrawLine(canvas, 0, 0, z, 0, color)
        graphics.DrawLine(canvas, 63, 0, 63-z, 0, color)

        graphics.DrawLine(canvas, 0, 0, zo, 0, color2)
        graphics.DrawLine(canvas, 63, 0, 63-zo, 0, color2)
    elif o <= 21500:
        o += 1
    else:
        x = 0
        y = 0
        z = 0
        w = 0
        o = 0
        xo = 0
        yo = 0
        zo = 0

   # graphics.DrawLine(canvas, 0, 14, 63, 14, color)
   # graphics.DrawLine(canvas, 0, 14, 0, 31, color)
   # graphics.DrawLine(canvas, 63, 14, 63, 31, color)


def __render_weather(canvas, layout, colors, weather):
    if weather.available():
        image_file = weather.icon_filename()
        weather_icon = Image.open(image_file)
        __render_weather_icon(canvas, layout, colors, weather_icon)
        __render_weather_text(canvas, layout, colors, weather.conditions, "conditions")
        __render_weather_text(canvas, layout, colors, weather.temperature_string(), "temperature")
        __render_weather_text(canvas, layout, colors, weather.wind_speed_string(), "wind_speed")
        __render_weather_text(canvas, layout, colors, weather.wind_dir_string(), "wind_dir")
        __render_weather_text(canvas, layout, colors, weather.wind_string(), "wind")


def __render_weather_text(canvas, layout, colors, text, keyname):
    coords = layout.coords("offday.{}".format(keyname))
    font = layout.font("offday.{}".format(keyname))
    color = colors.graphics_color("offday.{}".format(keyname))
    text_x = center_text_position(text, coords["x"], font["size"]["width"])
    graphics.DrawText(canvas, font["font"], text_x, coords["y"], color, text)


def __render_weather_icon(canvas, layout, colors, weather_icon):
    coords = layout.coords("offday.weather_icon")
    color = colors.color("offday.weather_icon")
    resize = coords.get("rescale_icon")

    if resize:
        weather_icon = weather_icon.resize(
            (weather_icon.width * resize, weather_icon.height * resize), Image.NEAREST
        )
    for x in range(weather_icon.width):
        for y in range(weather_icon.height):
            pixel = weather_icon.getpixel((x, y))
            if pixel[3] > 0:
                canvas.SetPixel(coords["x"] + x, coords["y"] + y, color["r"], color["g"], color["b"])


def __render_news_ticker(canvas, layout, colors, headlines, text_pos):
    coords = layout.coords("offday.scrolling_text")
    font = layout.font("offday.scrolling_text")
    color = colors.graphics_color("offday.scrolling_text")
    bgcolor = colors.graphics_color("default.background")
    ticker_text = headlines.ticker_string()
    return scrollingtext.render_text(
        canvas, coords["x"], coords["y"], coords["width"], font, color, bgcolor, ticker_text, text_pos
    )
