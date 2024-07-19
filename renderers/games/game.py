from driver import graphics
from data.config.color import Color
from data.config.layout import Layout
from data.scoreboard import Scoreboard
from data.scoreboard.atbat import AtBat
from data.scoreboard.bases import Bases
from data.scoreboard.inning import Inning
from data.scoreboard.pitches import Pitches
from data.plays import PLAY_RESULTS
from data.plays import OUTS
from data.plays import SCORING
from data.plays import HITS
from data.plays import STRIKEOUTS

from renderers import scrollingtext
from renderers.games import nohitter
import subprocess
from random import random
from renderers.games import teams

#lastplay = ""
x = 0
y = 0
z = 0
xo = 0
yo = 0
zo = 0
a = 0

def render_live_game(canvas, layout: Layout, colors: Color, scoreboard: Scoreboard, text_pos, animation_time):
    pos = 0
    if scoreboard.inning.state == Inning.TOP or scoreboard.inning.state == Inning.BOTTOM:
        pos = _render_at_bat(
                canvas,
                layout,
                colors,
                scoreboard.atbat,
                text_pos,
                scoreboard.play_result,
                (animation_time // 6) % 2,
                scoreboard.pitches
             )

        # Check if we're deep enough into a game and it's a no hitter or perfect game
        should_display_nohitter = layout.coords("nohitter")["innings_until_display"]
        if scoreboard.inning.number > should_display_nohitter:
            if layout.state_is_nohitter():
                nohitter.render_nohit_text(canvas, layout, colors)

        # _render_count(canvas, layout, colors, scoreboard.pitches)
        _render_outs(canvas, layout, colors, scoreboard.outs)
        _render_bases(canvas, layout, colors, scoreboard.bases, scoreboard.homerun(), (animation_time % 16) // 5)

        _render_inning_display(canvas, layout, colors, scoreboard.inning)

    else:
        _render_inning_break(canvas, layout, colors, scoreboard.inning)
        _render_due_up(canvas, layout, colors, scoreboard.atbat)

    return pos


# --------------- at-bat ---------------
def _render_at_bat(canvas, layout, colors, atbat: AtBat, text_pos, play_result, animation, pitches: Pitches):
    blength = __render_batter_text(canvas, layout, colors, atbat.batter, text_pos)
    # print(str(blength))
    # __render_pitch_text(canvas, layout, colors, pitches)
    # __render_pitch_count(canvas, layout, colors, pitches)
    results = list(PLAY_RESULTS.keys())
    oresults = list(OUTS)
    hresults = list(HITS)
    sresults = list(SCORING)
    skresults = list(STRIKEOUTS)
    #__render_play_result(canvas, layout, colors, play_result)

    #lastplay = play_result
    #print("LastPlay: " + lastplay)
    # global lastplay 
    #if (play_result != "") and (lastplay != play_result): 
    #    print("AtBat: " + play_result)

    plength = __render_pitcher_text(canvas, layout, colors, atbat.pitcher, pitches, text_pos)
    #print(str(plength))
    global a
    if play_result in results and __should_render_play_result(play_result, layout):
        if (play_result in oresults) or ("strikeout" in play_result):
            animation = 1
        #if (fl > 0) or (gr > 0) or (wa > 0):
        #    animation = 0
        # STOP DISPLAYING PLAY TEXT IF ANIMTION PLAYING
        if "strikeout" in play_result:
            color = colors.graphics_color("atbat.strikeout")
            graphics.DrawLine(canvas, 0, 31, 63, 31, color)
            graphics.DrawLine(canvas, 0, 14, 63, 14, color)
            graphics.DrawLine(canvas, 0, 14, 0, 31, color)
            graphics.DrawLine(canvas, 63, 14, 63, 31, color)
            if (a==0):
                a += 1
                if random() <= 0.3:
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l1", "-D600", "/home/bof/animations/so.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif "home_run" in play_result:
            if (a==0):
                a +=1
                gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l2", "-D450", "/home/bof/animations/firework22lowert.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=70", "--led-slowdown-gpio=4"])
        elif "walk" in play_result:
            if (a==0):
                a += 1
                rdm = random()
                if rdm <= 0.3:
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l3", "-D1000", "/home/bof/animations/walkt.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
                elif rdm > 0.95:
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l1", "-D300", "/home/bof/animations/ys.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif "hit_by_pitch" in play_result:
            if (a==0):
                a +=1
                gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l1", "-D800", "/home/bof/animations/hb.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=70", "--led-slowdown-gpio=4"])
        elif "field_out_fly" in play_result:
            if (a==0):
                a += 1
                rdm = random()
                if (rdm >= 0.1) and (rdm < 0.3):
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l1", "-D1200", "/home/bof/animations/fly3.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
                elif (rdm >= 0.3) and (rdm < 0.5):
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l8", "-D400", "/home/bof/animations/corn.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif "field_out_ground" in play_result:
            if (a==0):
                a += 1
                if random() <= 0.4:
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l1", "-D1000", "/home/bof/animations/grounder.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif "field_out_line" in play_result:
            if (a==0):
                a += 1
                if random() <= 0.4:
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l1", "-D700", "/home/bof/animations/lineoutt.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif "sac_fly" in play_result:
            if (a==0):
                a += 1
                if random() <= 0.5:
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l1", "-D1600", "/home/bof/animations/sacfly.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif "stolen_base_2b" in play_result:
            if (a==0):
                a += 1
                if random() <= 0.5:
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l1", "-D500", "/home/bof/animations/sb.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif "stolen_base_3b" in play_result:
            if (a==0):
                a += 1
                if random() <= 0.5:
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l1", "-D500", "/home/bof/animations/sb.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif "stolen_base_home" in play_result:
            if (a==0):
                a += 1
                gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l2", "-D450", "/home/bof/animations/firework22lowert.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=70", "--led-slowdown-gpio=4"])
        elif play_result not in oresults:
            if (a==0):
                a += 1
                rdm = random()
                if rdm >= 0.9:
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l4", "-D1000", "/home/bof/animations/kingt2.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
                elif rdm < 0.1:
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l8", "-D350", "/home/bof/animations/clap3t.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
                elif (rdm >= 0.1) and (rdm < 0.2):
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l12", "-D350", "/home/bof/animations/supert2.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
                elif (rdm >= 0.2) and (rdm < 0.3):
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l4", "-D300", "/home/bof/animations/ao.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
                elif (rdm >= 0.3) and (rdm < 0.4):
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l1", "-D600", "/home/bof/animations/wave.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
                elif (rdm >= 0.4) and (rdm < 0.5):
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l2", "-D600", "/home/bof/animations/wave2.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
                elif (rdm >= 0.5) and (rdm < 0.6):
                    gif = subprocess.Popen(["/home/bof/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer", "-l1", "-D1000", "/home/bof/animations/charge2.gif", "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])

        if (play_result not in sresults) and (play_result not in oresults) and (play_result not in skresults):
            global x
            global y
            global z
            global xo
            global yo
            global zo
            color = colors.graphics_color("atbat.batter")
            color2 = colors.graphics_color("default.background")
            if x < 32:
                graphics.DrawLine(canvas, 32-x, 31, x+32, 31, color)
                x += 1
            elif y < 16:
                y += 1
                graphics.DrawLine(canvas, 32-x, 31, x+32, 31, color)
                graphics.DrawLine(canvas, 0, 31-y, 0, 31, color)
                graphics.DrawLine(canvas, 63, 31-y, 63, 31, color)
            elif z <= 32:
                z += 1
                graphics.DrawLine(canvas, 32-x, 31, x+32, 31, color)
                graphics.DrawLine(canvas, 0, 31-y, 0, 31, color)
                graphics.DrawLine(canvas, 63, 31-y, 63, 31, color)

                graphics.DrawLine(canvas, 0, 14, z, 14, color)
                graphics.DrawLine(canvas, 63, 14, 63-z, 14, color)
            elif xo < 32:
                graphics.DrawLine(canvas, 32-x, 31, x+32, 31, color)
                graphics.DrawLine(canvas, 0, 31-y, 0, 31, color)
                graphics.DrawLine(canvas, 63, 31-y, 63, 31, color)

                graphics.DrawLine(canvas, 0, 14, z, 14, color)
                graphics.DrawLine(canvas, 63, 14, 63-z, 14, color)

                graphics.DrawLine(canvas, 32-xo, 31, xo+32, 31, color2)
                xo += 1
            elif yo < 16:
                yo += 1
                graphics.DrawLine(canvas, 0, 31-y, 0, 31, color)
                graphics.DrawLine(canvas, 63, 31-y, 63, 31, color)

                graphics.DrawLine(canvas, 0, 14, z, 14, color)
                graphics.DrawLine(canvas, 63, 14, 63-z, 14, color)

                graphics.DrawLine(canvas, 0, 31-yo, 0, 31, color2)
                graphics.DrawLine(canvas, 63, 31-yo, 63, 31, color2)
            elif zo <= 32:
                zo += 1
                graphics.DrawLine(canvas, 0, 14, z, 14, color)
                graphics.DrawLine(canvas, 63, 14, 63-z, 14, color)

                graphics.DrawLine(canvas, 0, 14, zo, 14, color2)
                graphics.DrawLine(canvas, 63, 14, 63-zo, 14, color2)
            else:
                x = 0
                y = 0
                z = 0
                xo = 0
                yo = 0
                zo = 0
        else:
            x = 0
            y = 0
            z = 0
            xo = 0
            yo = 0
            zo = 0

        #print("Play result in results and should render: " + play_result + ", Animation=" + str(animation) + " blength=" + str(blength)) 
        if animation:
            __render_play_result(canvas, layout, colors, play_result)
        return plength
        # return max(plength, blength)
    else:
        x = 0
        y = 0
        z = 0
        xo = 0
        yo = 0
        zo = 0

        a = 0

        # blength = __render_batter_text(canvas, layout, colors, atbat.batter, text_pos)
        __render_pitch_text(canvas, layout, colors, pitches)
        __render_pitch_count(canvas, layout, colors, pitches)
        _render_count(canvas, layout, colors, pitches)

        return max(plength, blength)


def __should_render_play_result(play_result, layout):
    #print("Render? " + play_result)
    if "strikeout" in play_result:
        coords = layout.coords("atbat.strikeout")
    else:
        coords = layout.coords("atbat.play_result")
    return coords["enabled"]


def __render_play_result(canvas, layout, colors, play_result):
    oresults = list(OUTS)
    sresults = list(SCORING)
    #print("Rendering " +  play_result)
    if "strikeout" in play_result:
        color = colors.graphics_color("atbat.strikeout")
        coords = layout.coords("atbat.strikeout")
        font = layout.font("atbat.strikeout")
    elif "home_run" in play_result:
        #color = colors.graphics_color("standings.nl.divider")
        color = colors.graphics_color("atbat.play_result")
        color2 = colors.graphics_color("atbat.batter")
        coords = layout.coords("atbat.play_result")
        font = layout.font("atbat.play_result")
        graphics.DrawLine(canvas, 0, 31, 63, 31, color2)
        graphics.DrawLine(canvas, 0, 14, 63, 14, color2)
        graphics.DrawLine(canvas, 0, 14, 0, 31, color2)
        graphics.DrawLine(canvas, 63, 14, 63, 31, color2)
    elif play_result in sresults:
        color = colors.graphics_color("atbat.play_result")
        color2 = colors.graphics_color("atbat.batter")
        coords = layout.coords("atbat.play_result")
        font = layout.font("atbat.play_result")
        graphics.DrawLine(canvas, 0, 31, 63, 31, color2)
        graphics.DrawLine(canvas, 0, 14, 63, 14, color2)
        graphics.DrawLine(canvas, 0, 14, 0, 31, color2)
        graphics.DrawLine(canvas, 63, 14, 63, 31, color2)
    else:
        color = colors.graphics_color("atbat.play_result")
        coords = layout.coords("atbat.play_result")
        font = layout.font("atbat.play_result")
    try:
        text = PLAY_RESULTS[play_result][coords["desc_length"].lower()]
    except KeyError:
        return
    #if play_result not in oresults:
    #if play_result in sresults:
    #color2 = colors.graphics_color("atbat.batter")
    graphics.DrawText(canvas, font["font"], coords["x"], coords["y"], color, text)


def __render_batter_text(canvas, layout, colors, batter, text_pos):
    coords = layout.coords("atbat.batter")
    color = colors.graphics_color("atbat.batter")
    font = layout.font("atbat.batter")
    bgcolor = colors.graphics_color("default.background")
    offset = coords.get("offset", 0)
    pos = scrollingtext.render_text(
        canvas,
        coords["x"] + font["size"]["width"] * 3,
        coords["y"],
        coords["width"],
        font,
        color,
        bgcolor,
        batter,
        text_pos + offset,
        center=False,
    )
    graphics.DrawText(canvas, font["font"], coords["x"], coords["y"], color, "AB:")
    return pos


def __render_pitcher_text(canvas, layout, colors, pitcher, pitches: Pitches, text_pos):
    coords = layout.coords("atbat.pitcher")
    color = colors.graphics_color("atbat.pitcher")
    font = layout.font("atbat.pitcher")
    bgcolor = colors.graphics_color("default.background")

    pitch_count = layout.coords("atbat.pitch_count")
    if pitch_count["enabled"] and pitch_count["append_pitcher_name"]:
        pitcher += f" ({pitches.pitch_count})"

    pos = scrollingtext.render_text(
        canvas,
        coords["x"] + font["size"]["width"] * 2,
        coords["y"],
        coords["width"],
        font,
        color,
        bgcolor,
        pitcher,
        text_pos,
        center=False,
    )
    graphics.DrawText(canvas, font["font"], coords["x"], coords["y"], color, "P:")
    return pos


def __render_pitch_text(canvas, layout, colors, pitches: Pitches):
    coords = layout.coords("atbat.pitch")
    color = colors.graphics_color("atbat.pitch")
    font = layout.font("atbat.pitch")
    if int(pitches.last_pitch_speed) and coords["enabled"]:
        mph = ""
        if coords["mph"]:
            mph = "mph "
        if coords["desc_length"].lower() == "long":
            pitch_text = str(pitches.last_pitch_speed) + mph + pitches.last_pitch_type_long
        elif coords["desc_length"].lower() == "short":
            pitch_text = str(pitches.last_pitch_speed) + mph + pitches.last_pitch_type
        else:
            pitch_text = ""
        graphics.DrawText(canvas, font["font"], coords["x"], coords["y"], color, pitch_text)


def __render_pitch_count(canvas, layout, colors, pitches: Pitches):
    coords = layout.coords("atbat.pitch_count")
    color = colors.graphics_color("atbat.pitch_count")
    font = layout.font("atbat.pitch_count")
    if coords["enabled"] and not coords["append_pitcher_name"]:
        pitch_count = f"{pitches.pitch_count}p"
        graphics.DrawText(canvas, font["font"], coords["x"], coords["y"], color, pitch_count)


# --------------- bases ---------------
def _render_bases(canvas, layout, colors, bases: Bases, home_run, animation):
    base_runners = bases.runners
    base_colors = []
    base_colors.append(colors.graphics_color("bases.1B"))
    base_colors.append(colors.graphics_color("bases.2B"))
    base_colors.append(colors.graphics_color("bases.3B"))

    base_px = []
    base_px.append(layout.coords("bases.1B"))
    base_px.append(layout.coords("bases.2B"))
    base_px.append(layout.coords("bases.3B"))

    for base in range(len(base_runners)):
        __render_base_outline(canvas, base_px[base], base_colors[base])

        # Fill in the base if there's currently a baserunner or cycle if theres a homer
        if base_runners[base] or (home_run and animation == base):
            __render_baserunner(canvas, base_px[base], base_colors[base])


def __render_base_outline(canvas, base, color):
    x, y = (base["x"], base["y"])
    size = base["size"]
    half = abs(size // 2)
    graphics.DrawLine(canvas, x + half, y, x, y + half, color)
    graphics.DrawLine(canvas, x + half, y, x + size, y + half, color)
    graphics.DrawLine(canvas, x + half, y + size, x, y + half, color)
    graphics.DrawLine(canvas, x + half, y + size, x + size, y + half, color)


def __render_baserunner(canvas, base, color):
    x, y = (base["x"], base["y"])
    size = base["size"]
    half = abs(size // 2)
    for offset in range(1, half + 1):
        graphics.DrawLine(canvas, x + half - offset, y + size - offset, x + half + offset, y + size - offset, color)
        graphics.DrawLine(canvas, x + half - offset, y + offset, x + half + offset, y + offset, color)


# --------------- count ---------------
def _render_count(canvas, layout, colors, pitches: Pitches):
    font = layout.font("batter_count")
    coords = layout.coords("batter_count")
    pitches_color = colors.graphics_color("batter_count")
    batter_count_text = "{}-{}".format(pitches.balls, pitches.strikes)
    graphics.DrawText(canvas, font["font"], coords["x"], coords["y"], pitches_color, batter_count_text)


# --------------- outs ---------------
def __out_colors(colors):
    outlines = []
    fills = []
    for i in range(3):
        color = colors.graphics_color(f"outs.{i+1}")
        outlines.append(color)
        try:
            color = colors.graphics_color(f"outs.fill.{i+1}")
        except KeyError:
            pass
        fills.append(color)
    return outlines, fills


def _render_outs(canvas, layout, colors, outs):
    out_px = []
    out_px.append(layout.coords("outs.1"))
    out_px.append(layout.coords("outs.2"))
    out_px.append(layout.coords("outs.3"))

    out_colors = []
    out_colors, fill_colors = __out_colors(colors)

    for out in range(len(out_px)):
        __render_out_circle(canvas, out_px[out], out_colors[out])
        # Fill in the circle if that out has occurred
        if outs.number > out:
            __fill_out_circle(canvas, out_px[out], fill_colors[out])


def __render_out_circle(canvas, out, color):
    x, y, size = (out["x"], out["y"], out["size"])

    #graphics.DrawLine(canvas, x, y, x + size, y, color)
    #graphics.DrawLine(canvas, x, y, x, y + size, color)
    #graphics.DrawLine(canvas, x + size, y + size, x, y + size, color)
    #graphics.DrawLine(canvas, x + size, y + size, x + size, y, color)

    graphics.DrawLine(canvas, x+1, y, x + size-2, y, color)
    graphics.DrawLine(canvas, x, y+1, x, y + size-2, color)
    graphics.DrawLine(canvas, x + size-2, y + size-1, x+1, y + size-1, color)
    graphics.DrawLine(canvas, x + size-1, y + size-2, x + size-1, y+1, color)


def __fill_out_circle(canvas, out, color):
    size = out["size"]
    x, y = (out["x"], out["y"])
    x += 1
    y += 1
    size -= 1
    for y_offset in range(size-1):
        graphics.DrawLine(canvas, x, y + y_offset, x + size - 1, y + y_offset, color)


# --------------- inning information ---------------
def _render_inning_break(canvas, layout, colors, inning: Inning):

    text_font = layout.font("inning.break.text")
    num_font = layout.font("inning.break.number")
    text_coords = layout.coords("inning.break.text")
    num_coords = layout.coords("inning.break.number")
    color = colors.graphics_color("inning.break.text")
    text = inning.state
    if text == "Middle":
        text = "Mid"
    num = inning.ordinal
    graphics.DrawText(canvas, text_font["font"], text_coords["x"], text_coords["y"], color, text)
    #graphics.DrawText(canvas, num_font["font"], num_coords["x"], num_coords["y"], color, num)
    if inning.number>9:
        num = str(inning.number)
    else:
        num = inning.ordinal
    graphics.DrawText(canvas, num_font["font"], num_coords["x"], num_coords["y"], color, num)


def _render_due_up(canvas, layout, colors, atbat: AtBat):
    due_font = layout.font("inning.break.due_up.due")
    due_color = colors.graphics_color("inning.break.due_up")

    due = layout.coords("inning.break.due_up.due")
    up = layout.coords("inning.break.due_up.up")
    graphics.DrawText(canvas, due_font["font"], due["x"], due["y"], due_color, "Due")
    graphics.DrawText(canvas, due_font["font"], up["x"], up["y"], due_color, "Up:")

    divider = layout.coords("inning.break.due_up.divider")
    if divider["draw"]:
        graphics.DrawLine(
            canvas,
            divider["x"],
            divider["y_start"],
            divider["x"],
            divider["y_end"],
            colors.graphics_color("inning.break.due_up_divider"),
        )

    batter_font = layout.font("inning.break.due_up.leadoff")
    batter_color = colors.graphics_color("inning.break.due_up_names")

    leadoff = layout.coords("inning.break.due_up.leadoff")
    on_deck = layout.coords("inning.break.due_up.on_deck")
    in_hole = layout.coords("inning.break.due_up.in_hole")
    graphics.DrawText(canvas, batter_font["font"], leadoff["x"], leadoff["y"], batter_color, atbat.batter)
    graphics.DrawText(canvas, batter_font["font"], on_deck["x"], on_deck["y"], batter_color, atbat.onDeck)
    graphics.DrawText(canvas, batter_font["font"], in_hole["x"], in_hole["y"], batter_color, atbat.inHole)


def _render_inning_display(canvas, layout, colors, inning: Inning):
    __render_number(canvas, layout, colors, inning)
    __render_inning_half(canvas, layout, colors, inning)


def __render_number(canvas, layout, colors, inning):
    number_color = colors.graphics_color("inning.number")
    coords = layout.coords("inning.number")
    font = layout.font("inning.number")
    pos_x = coords["x"] - (len(str(inning.number)) * font["size"]["width"])
    if inning.number>9:
        graphics.DrawText(canvas, font["font"], pos_x+2, coords["y"], number_color, str(inning.number))
    else:
        graphics.DrawText(canvas, font["font"], pos_x, coords["y"], number_color, str(inning.number))


def __render_inning_half(canvas, layout, colors, inning):
    font = layout.font("inning.number")
    num_coords = layout.coords("inning.number")
    arrow_coords = layout.coords("inning.arrow")
    inning_size = len(str(inning.number)) * font["size"]["width"]
    size = arrow_coords["size"]
    top = inning.state == Inning.TOP
    if top:
        x = num_coords["x"] - inning_size + arrow_coords["up"]["x_offset"]
        if inning.number>9:
            x = num_coords["x"] - inning_size + arrow_coords["up"]["x_offset"] + 4
        y = num_coords["y"] + arrow_coords["up"]["y_offset"]
        dir = 1
    else:
        x = num_coords["x"] - inning_size + arrow_coords["down"]["x_offset"]
        if inning.number>9:
            x = num_coords["x"] - inning_size + arrow_coords["up"]["x_offset"] + 4
        y = num_coords["y"] + arrow_coords["down"]["y_offset"]
        dir = -1

    keypath = "inning.arrow.up" if top else "inning.arrow.down"
    color = colors.graphics_color(keypath)
    for offset in range(size):
        graphics.DrawLine(canvas, x - offset, y + (offset * dir), x + offset, y + (offset * dir), color)
        graphics.DrawLine(canvas, x - offset + 1, y + (offset * dir) - 1, x + offset + 1, y + (offset * dir) + 1, color)
