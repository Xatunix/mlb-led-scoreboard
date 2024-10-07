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

from random import random
from datetime import datetime
#import subprocess
#from pathlib import Path
#import os

x = 0
y = 0
z = 0
xx = 0
yy = 0
zz = 0
xxx = 0
yyy = 0
zzz = 0
xo = 0
yo = 0
zo = 0
w = 0
o = 0
i = 0
agif = False

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
    
    date_coords = layout.coords("offday.date")
    date_format = "%a,%b %d"
    date_text = datetime.now().strftime(date_format)
    date_text_x = center_text_position(date_text, date_coords["x"], font["size"]["width"])
    graphics.DrawText(canvas, font["font"], date_text_x, date_coords["y"], color, date_text)

    
    #global agif
    #home = os.environ['HOME']
    #home = os.path.expanduser('~')
    #home = "/home/bof"
    #liv = str(home) + "/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer"
    #gifp = "/animations/so.gif"
    #gifpp = str(home) + gifp
    #if agif==False:
    #    agif = True
    #    #gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l1", "-D600", "${HOME}/animations/so.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    #    gif = subprocess.Popen([liv, "-l1", "-D600", gifpp, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])

    if "Mon" in date_text:
        color = colors.graphics_color("offday.time")
        #animation_crown(canvas, colors, color)
    elif "Tu" in date_text:
        color = colors.graphics_color("standings.al.divider")
        #animation_chase(canvas, colors, color)
    elif "Wed" in date_text:
        color1 = colors.graphics_color("offday.time")
        color2 = colors.graphics_color("offday.time")
        #animation_stripe(canvas, colors, color1, color2)
    elif "Thu" in date_text:
        color = colors.graphics_color("offday.time")
        #color = colors.graphics_color("standings.nl.divider")
        #animation_chase3(canvas, colors, color)
    elif "Fri" in date_text:
        color = colors.graphics_color("offday.time")
        #animation_crown3(canvas, colors)
    elif "Sat" in date_text:
        color = colors.graphics_color("atbat.play_result")
        #animation_crown(canvas, colors, color)
    elif "Sun" in date_text:
        color = colors.graphics_color("atbat.play_result")
        #animation_crown(canvas, colors, color)
    else:
        color = colors.graphics_color("offday.time")
        #animation_crown(canvas, colors, color)


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



def animation_ring(canvas, colors, color):
    #color = colors.graphics_color("offday.time")
    color0 = colors.graphics_color("default.background")
    color1 = colors.graphics_color("standings.nl.divider")
    color2 = colors.graphics_color("standings.al.divider")

    xMax = canvas.width
    yMax = canvas.height
    xMin = 0
    yMin = 0
    xS = xMax-1
    xH = xMax/2
    yS = yMax-1
    graphics.DrawLine(canvas, xMin, yS, xS, yS, color)
    graphics.DrawLine(canvas, xMin, yMin, xS, yMin, color)
    graphics.DrawLine(canvas, xMin, yMin, xMin, yS, color)
    graphics.DrawLine(canvas, xS, yMin, xS, yS, color)


def animation_crown(canvas, colors, color):
        global x
        global y
        global z
        global xo
        global yo
        global zo
        global w
        global o

        #color = colors.graphics_color("offday.time")
        color2 = colors.graphics_color("default.background")
        xMax = canvas.width
        yMax = canvas.height
        xMin = 0 #must stay 0
        yMin = 0 #14
        xS = xMax-1
        xH = xMax/2 
        yS = yMax-1
        if x < xH:
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color)
            x += 1
        elif y <= yS-yMin-1:
            y += 1
            graphics.DrawLine(canvas, xMin, yS, x+xH, yS, color)
            graphics.DrawLine(canvas, xMin, yS-y, xMin, yS, color)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color)
        elif z <= yMax:
            z += 1
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color)
            graphics.DrawLine(canvas, xMin, yS-y, xMin, yS, color)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color)

            graphics.DrawLine(canvas, xMin, yMin, z, yMin, color)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color)
        elif w <= 4500:
            w += 1
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color)
            graphics.DrawLine(canvas, xMin, yS-y, xMin, yS, color)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color)

            graphics.DrawLine(canvas, xMin, yMin, z, yMin, color)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color)
        elif xo < xH:
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color)
            graphics.DrawLine(canvas, xMin, yS-y, xMin, yS, color)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color)

            graphics.DrawLine(canvas, xMin, yMin, z, yMin, color)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color)

            graphics.DrawLine(canvas, xH-xo, yS, xo+xH, yS, color2)
            xo += 1
        elif yo <= yS-yMin-1:
            yo += 1
            graphics.DrawLine(canvas, xMin, yS-y, xMin, yS, color)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color)

            graphics.DrawLine(canvas, xMin, yMin, z, yMin, color)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color)

            graphics.DrawLine(canvas, xMin, yS-yo, xMin, yS, color2)
            graphics.DrawLine(canvas, xS, yS-yo, xS, yS, color2)
        elif zo <= xH:
            zo += 1
            graphics.DrawLine(canvas, xMin, yMin, z, yMin, color)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color)

            graphics.DrawLine(canvas, xMin, yMin, zo, yMin, color2)
            graphics.DrawLine(canvas, xS, yMin, xS-zo, yMin, color2)
        elif o <= 8600: #2150
            o += 1
        else:
            x = 0
            y = 0
            z = 0
            xo = 0
            yo = 0
            zo = 0
            o = 0
            w = 0

def animation_crown3(canvas, colors):
        global x
        global y
        global z
        global xx
        global yy
        global zz
        global xxx
        global yyy
        global zzz
        global xo
        global yo
        global zo
        global w
        global o

        #color = colors.graphics_color("offday.time")
        color4 = colors.graphics_color("default.background")
        color3 = colors.graphics_color("standings.nl.divider")
        color2 = colors.graphics_color("atbat.play_result")
        color1 = colors.graphics_color("standings.al.divider")
        xMax = canvas.width
        yMax = canvas.height
        xMin = 0 #must stay 0
        yMin = 0 #14
        xS = xMax-1
        xH = xMax/2 
        yS = yMax-1
        if x < xH:
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color1)
            x += 1
        elif y <= yS-yMin-1:
            y += 1
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color1)
            graphics.DrawLine(canvas, 0, yS-y, 0, yS, color1)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color1)
        elif z <= yMax:
            z += 1
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color1)
            graphics.DrawLine(canvas, 0, yS-y, 0, yS, color1)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color1)

            graphics.DrawLine(canvas, 0, yMin, z, yMin, color1)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color1)
        elif xx < xH:
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color1)
            graphics.DrawLine(canvas, 0, yS-y, 0, yS, color1)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color1)
            graphics.DrawLine(canvas, 0, yMin, z, yMin, color1)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color1)

            xx += 1
            graphics.DrawLine(canvas, xH-xx, yS, xx+xH, yS, color2)
        elif yy <= yS-yMin-1:
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color1)
            graphics.DrawLine(canvas, 0, yS-y, 0, yS, color1)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color1)
            graphics.DrawLine(canvas, 0, yMin, z, yMin, color1)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color1)

            graphics.DrawLine(canvas, xH-xx, yS, xx+xH, yS, color2)

            yy += 1
            graphics.DrawLine(canvas, 0, yS-yy, 0, yS, color2)
            graphics.DrawLine(canvas, xS, yS-yy, xS, yS, color2)
        elif zz <= yMax:
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color1)
            graphics.DrawLine(canvas, 0, yS-y, 0, yS, color1)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color1)
            graphics.DrawLine(canvas, 0, yMin, z, yMin, color1)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color1)

            graphics.DrawLine(canvas, xH-xx, yS, xx+xH, yS, color2)
            graphics.DrawLine(canvas, 0, yS-yy, 0, yS, color2)
            graphics.DrawLine(canvas, xS, yS-yy, xS, yS, color2)

            zz += 1
            graphics.DrawLine(canvas, 0, yMin, zz, yMin, color2)
            graphics.DrawLine(canvas, xS, yMin, xS-zz, yMin, color2)
        elif xxx < xH:
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color2)
            graphics.DrawLine(canvas, 0, yS-y, 0, yS, color2)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color2)
            graphics.DrawLine(canvas, 0, yMin, z, yMin, color2)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color2)

            xxx += 1
            graphics.DrawLine(canvas, xH-xxx, yS, xxx+xH, yS, color3)
        elif yyy <= yS-yMin-1:
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color2)
            graphics.DrawLine(canvas, 0, yS-y, 0, yS, color2)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color2)
            graphics.DrawLine(canvas, 0, yMin, z, yMin, color2)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color2)

            graphics.DrawLine(canvas, xH-xxx, yS, xxx+xH, yS, color3)

            yyy += 1
            graphics.DrawLine(canvas, 0, yS-yyy, 0, yS, color3)
            graphics.DrawLine(canvas, xS, yS-yyy, xS, yS, color3)
        elif zzz <= yMax:
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color2)
            graphics.DrawLine(canvas, 0, yS-y, 0, yS, color2)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color2)
            graphics.DrawLine(canvas, 0, yMin, z, yMin, color2)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color2)

            graphics.DrawLine(canvas, xH-xxx, yS, xxx+xH, yS, color3)
            graphics.DrawLine(canvas, 0, yS-yyy, 0, yS, color3)
            graphics.DrawLine(canvas, xS, yS-yyy, xS, yS, color3)

            zzz += 1
            graphics.DrawLine(canvas, 0, yMin, zzz, yMin, color3)
            graphics.DrawLine(canvas, xS, yMin, xS-zzz, yMin, color3)
        elif xo < xH:
            graphics.DrawLine(canvas, xH-x, yS, x+xH, yS, color3)
            graphics.DrawLine(canvas, 0, yS-y, 0, yS, color3)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color3)

            graphics.DrawLine(canvas, 0, yMin, z, yMin, color3)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color3)

            graphics.DrawLine(canvas, xH-xo, yS, xo+xH, yS, color4)
            xo += 1
        elif yo <= yS-yMin-1:
            yo += 1
            graphics.DrawLine(canvas, 0, yS-y, 0, yS, color3)
            graphics.DrawLine(canvas, xS, yS-y, xS, yS, color3)

            graphics.DrawLine(canvas, 0, yMin, z, yMin, color3)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color3)

            graphics.DrawLine(canvas, 0, yS-yo, 0, yS, color4)
            graphics.DrawLine(canvas, xS, yS-yo, xS, yS, color4)
        elif zo <= xH:
            zo += 1
            graphics.DrawLine(canvas, 0, yMin, z, yMin, color3)
            graphics.DrawLine(canvas, xS, yMin, xS-z, yMin, color3)

            graphics.DrawLine(canvas, 0, yMin, zo, yMin, color4)
            graphics.DrawLine(canvas, xS, yMin, xS-zo, yMin, color4)
        elif o <= 8600:
            o += 1
        else:
            x = 0
            y = 0
            z = 0
            xx = 0
            yy = 0
            zz = 0
            xxx = 0
            yyy = 0
            zzz = 0
            xo = 0
            yo = 0
            zo = 0
            o = 0
            w = 0

def animation_stripe(canvas, colors, color1, color2):
        global x
        global y
        global z
        global xo
        global yo
        global zo
        global w
        global o

        #color = colors.graphics_color("offday.time")
        #color0 = colors.graphics_color("default.background")
        #color1 = colors.graphics_color("standings.nl.divider")
        #color2 = colors.graphics_color("standings.al.divider")
        #color3 = colors.graphics_color("atbat.play_result")

        xMax = canvas.width
        yMax = canvas.height
        xMin = 0
        yMin = 0
        xS = xMax-1
        xH = xMax/2 
        yS = yMax-1

        if (w < 2150):
            for x in range (xMin, xMax):
                if (x % 4) > 0:
                    graphics.DrawLine(canvas, x, yS, x, yS, color1)
                    graphics.DrawLine(canvas, x, yMin, x, yMin, color1)
                else:
                    graphics.DrawLine(canvas, x, yS, x, yS, color2)
                    graphics.DrawLine(canvas, x, yMin, x, yMin, color2)

            for y in range (yMin, yMax):
                if (y % 4) > 0:
                    graphics.DrawLine(canvas, xMin, y, xMin, y, color1)
                    graphics.DrawLine(canvas, xS, y, xS, y, color1)
                else:
                    graphics.DrawLine(canvas, xMin, y, xMin, y, color2)
                    graphics.DrawLine(canvas, xS, y, xS, y, color2)
            w += 1
            o = 0
        elif (w < 4300):
            for x in range (xMin, xMax):
                if (x % 4) > 0:
                    graphics.DrawLine(canvas, x, yS, x, yS, color2)
                    graphics.DrawLine(canvas, x, yMin, x, yMin, color2)
                else:
                    graphics.DrawLine(canvas, x, yS, x, yS, color1)
                    graphics.DrawLine(canvas, x, yMin, x, yMin, color1)

            for y in range (yMin, yMax):
                if (y % 4) > 0:
                    graphics.DrawLine(canvas, xMin, y, xMin, y, color2)
                    graphics.DrawLine(canvas, xS, y, xS, y, color2)
                else:
                    graphics.DrawLine(canvas, xMin, y, xMin, y, color1)
                    graphics.DrawLine(canvas, xS, y, xS, y, color1)
            w += 1
            o = 0
        else:
            o += 1
        if (w >= 4300) and (o >= 8600):
            o = 0
            w = 0 

def animation_flash(canvas, colors, color):
        global x
        global y
        global z
        global xo
        global yo
        global zo
        global w
        global o
        color1 = color
        #color1 = colors.graphics_color("offday.time")
        color0 = colors.graphics_color("default.background")
        #color1 = colors.graphics_color("standings.nl.divider")
        #color2 = colors.graphics_color("standings.al.divider")

        xMax = canvas.width
        yMax = canvas.height
        xMin = 0
        yMin = 0
        xS = xMax-1
        xH = xMax/2
        yS = yMax-1
       
        if (w < 1000):
            for x in range (xMin, xMax):
                if (x % 4) > 0:
                    graphics.DrawLine(canvas, x, yS, x, yS, color1)
                    graphics.DrawLine(canvas, x, yMin, x, yMin, color1)
                else:
                    graphics.DrawLine(canvas, x, yS, x, yS, color0)
                    graphics.DrawLine(canvas, x, yMin, x, yMin, color0)

            for y in range (yMin, yMax):
                if (y % 4) > 0:
                    graphics.DrawLine(canvas, xMin, y, xMin, y, color1)
                    graphics.DrawLine(canvas, xS, y, xS, y, color1)
                else:
                    graphics.DrawLine(canvas, xMin, y, xMin, y, color0)
                    graphics.DrawLine(canvas, xS, y, xS, y, color0)
            w += 1
            o = 0
        else:
            for x in range (xMin, xMax):
                if (x % 3) > 0:
                    graphics.DrawLine(canvas, x, yS, x, yS, color0)
                    graphics.DrawLine(canvas, x, yMin, x, yMin, color0)
                else:
                    graphics.DrawLine(canvas, x, yS, x, yS, color1)
                    graphics.DrawLine(canvas, x, yMin, x, yMin, color1)

            for y in range (yMin, yMax):
                if (y % 3) > 0:
                    graphics.DrawLine(canvas, xMin, y, xMin, y, color0)
                    graphics.DrawLine(canvas, xS, y, xS, y, color0)
                else:
                    graphics.DrawLine(canvas, xMin, y, xMin, y, color1)
                    graphics.DrawLine(canvas, xS, y, xS, y, color1)

            o += 1
            #color = color2 
            #color2 = color1
            #color1 = color
        if (w >= 1000) and (o >= 1000):
            o = 0
            w = 0


def animation_chase(canvas, colors, color):
        global x
        global y
        global z
        global w
        global o

        #color = colors.graphics_color("offday.time")
        color0 = colors.graphics_color("default.background")
        color1 = colors.graphics_color("standings.nl.divider")
        color2 = colors.graphics_color("standings.al.divider")
        color3 = colors.graphics_color("atbat.play_result")

        xMax = canvas.width
        yMax = canvas.height
        xMin = 0
        yMin = 0
        xS = xMax-1
        xH = xMax/2 
        yS = yMax-1

        i = 3

        if (o < 4300):
            if (w > 240):
                w = 0
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x+3, yS, x+3, yS, color0)
                        graphics.DrawLine(canvas, x-3, yMin, x-3, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x+3, yS, x+3, yS, color)
                        graphics.DrawLine(canvas, x-3, yMin, x-3, yMin, color)
                for y in range (yMin, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y+3, xMin, y+3, color0)
                        graphics.DrawLine(canvas, xS, y-3, xS, y-3, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y+3, xMin, y+3, color)
                        graphics.DrawLine(canvas, xS, y-3, xS, y-3, color)
            elif (w > 160):
                w += 1
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x+2, yS, x+2, yS, color0)
                        graphics.DrawLine(canvas, x-2, yMin, x-2, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x+2, yS, x+2, yS, color)
                        graphics.DrawLine(canvas, x-2, yMin, x-2, yMin, color)
                for y in range (yMin, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y+2, xMin, y+2, color0)
                        graphics.DrawLine(canvas, xS, y-2, xS, y-2, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y+2, xMin, y+2, color)
                        graphics.DrawLine(canvas, xS, y-2, xS, y-2, color)
            elif (w > 80):
                w += 1
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x+1, yS, x+1, yS, color0)
                        graphics.DrawLine(canvas, x-1, yMin, x-1, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x+1, yS, x+1, yS, color)
                        graphics.DrawLine(canvas, x-1, yMin, x-1, yMin, color)
                for y in range (yMin, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y+1, xMin, y+1, color0)
                        graphics.DrawLine(canvas, xS, y-1, xS, y-1, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y+1, xMin, y+1, color)
                        graphics.DrawLine(canvas, xS, y-1, xS, y-1, color)
            else:
                w += 1
                o += 1
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x, yS, x, yS, color0)
                        graphics.DrawLine(canvas, x, yMin, x, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x, yS, x, yS, color)
                        graphics.DrawLine(canvas, x, yMin, x, yMin, color)
                for y in range (yMin, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y, xMin, y, color0)
                        graphics.DrawLine(canvas, xS, y, xS, y, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y, xMin, y, color)
                        graphics.DrawLine(canvas, xS, y, xS, y, color)

        elif (o > 8600):
            w = 0
            o = 0
        else:
            o += 1


def animation_chase2(canvas, colors, color):
        global x
        global y
        global z
        global w
        global o

        #color = colors.graphics_color("offday.time")
        color0 = colors.graphics_color("default.background")
        color1 = colors.graphics_color("standings.nl.divider")
        color2 = colors.graphics_color("standings.al.divider")
        color3 = colors.graphics_color("atbat.play_result")

        xMax = canvas.width
        yMax = canvas.height
        xMin = 0
        yMin = 14
        xS = xMax-1
        xH = xMax/2 
        yS = yMax-1

        i = 3

        if (o < 4300):
            if (w > 240):
                w = 0
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x-3, yS, x-3, yS, color0)
                        graphics.DrawLine(canvas, x+3, yMin, x+3, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x-3, yS, x-3, yS, color)
                        graphics.DrawLine(canvas, x+3, yMin, x+3, yMin, color)
                for y in range (yMin+3, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y-3, xMin, y-3, color0)
                        graphics.DrawLine(canvas, xS, y+3, xS, y+3, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y-3, xMin, y-3, color)
                        graphics.DrawLine(canvas, xS, y+3, xS, y+3, color)
            elif (w > 160):
                w += 1
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x-2, yS, x-2, yS, color0)
                        graphics.DrawLine(canvas, x+2, yMin, x+2, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x-2, yS, x-2, yS, color)
                        graphics.DrawLine(canvas, x+2, yMin, x+2, yMin, color)
                for y in range (yMin+2, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y-2, xMin, y-2, color0)
                        graphics.DrawLine(canvas, xS, y+2, xS, y+2, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y-2, xMin, y-2, color)
                        graphics.DrawLine(canvas, xS, y+2, xS, y+2, color)
            elif (w > 80):
                w += 1
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x-1, yS, x-1, yS, color0)
                        graphics.DrawLine(canvas, x+1, yMin, x+1, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x+1, yS, x-1, yS, color)
                        graphics.DrawLine(canvas, x+1, yMin, x+1, yMin, color)
                for y in range (yMin+1, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y-1, xMin, y-1, color0)
                        graphics.DrawLine(canvas, xS, y+1, xS, y+1, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y-1, xMin, y-1, color)
                        graphics.DrawLine(canvas, xS, y+1, xS, y+1, color)
            else:
                w += 1
                o += 1
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x, yS, x, yS, color0)
                        graphics.DrawLine(canvas, x, yMin, x, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x, yS, x, yS, color)
                        graphics.DrawLine(canvas, x, yMin, x, yMin, color)
                for y in range (yMin, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y, xMin, y, color0)
                        graphics.DrawLine(canvas, xS, y, xS, y, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y, xMin, y, color)
                        graphics.DrawLine(canvas, xS, y, xS, y, color)

        elif (o > 8600):
            w = 0
            o = 0
        else:
            o += 1

def animation_chase3(canvas, colors, color):
        global x
        global y
        global z
        global w
        global o

        #color = colors.graphics_color("offday.time")
        color0 = colors.graphics_color("default.background")
        color1 = colors.graphics_color("standings.nl.divider")
        color2 = colors.graphics_color("standings.al.divider")
        color3 = colors.graphics_color("atbat.play_result")

        xMax = canvas.width
        yMax = canvas.height
        xMin = 0
        yMin = 14
        xS = xMax-1
        xH = xMax/2 
        yS = yMax-1

        i = 3

        if (o < 4300):
            if (w > 240):
                w = 0
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x, yS, x, yS, color0)
                        graphics.DrawLine(canvas, x, yMin, x, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x, yS, x, yS, color)
                        graphics.DrawLine(canvas, x, yMin, x, yMin, color)
                for y in range (yMin, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y, xMin, y, color0)
                        graphics.DrawLine(canvas, xS, y, xS, y, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y, xMin, y, color)
                        graphics.DrawLine(canvas, xS, y, xS, y, color)
            elif (w > 160):
                w += 1
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x-2, yS, x-2, yS, color0)
                        graphics.DrawLine(canvas, x+2, yMin, x+2, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x-2, yS, x-2, yS, color)
                        graphics.DrawLine(canvas, x+2, yMin, x+2, yMin, color)
                for y in range (yMin+2, yMax+2):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y-2, xMin, y-2, color0)
                        graphics.DrawLine(canvas, xS, y+2, xS, y+2, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y-2, xMin, y-2, color)
                        graphics.DrawLine(canvas, xS, y+2, xS, y+2, color)
            elif (w > 80):
                w += 1
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x-1, yS, x-1, yS, color0)
                        graphics.DrawLine(canvas, x+1, yMin, x+1, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x+1, yS, x-1, yS, color)
                        graphics.DrawLine(canvas, x+1, yMin, x+1, yMin, color)
                for y in range (yMin, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y-1, xMin, y-1, color0)
                        graphics.DrawLine(canvas, xS, y+1, xS, y+1, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y-1, xMin, y-1, color)
                        graphics.DrawLine(canvas, xS, y+1, xS, y+1, color)
            else:
                w += 1
                o += 1
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x, yS, x, yS, color0)
                        graphics.DrawLine(canvas, x, yMin, x, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x, yS, x, yS, color)
                        graphics.DrawLine(canvas, x, yMin, x, yMin, color)
                for y in range (yMin-1, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y, xMin, y, color0)
                        graphics.DrawLine(canvas, xS, y, xS, y, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y, xMin, y, color)
                        graphics.DrawLine(canvas, xS, y, xS, y, color)

        elif (o > 8600):
            w = 0
            o = 0
        else:
            o += 1

