from driver import graphics
from data.config.color import Color
from data.config.layout import Layout
from data.scoreboard import Scoreboard
from data.scoreboard.atbat import AtBat
from data.scoreboard.bases import Bases
from data.scoreboard.inning import Inning
from data.scoreboard.pitches import Pitches
from data.plays import PLAY_RESULTS
from data.plays import HITS
from data.plays import WALKS
from data.plays import OUTS
from data.plays import STRIKEOUTS
from data.plays import SCORING
from data.plays import OTHERS

from renderers import scrollingtext
from renderers.games import nohitter

import subprocess
from random import random
#from renderers.games import teams

#lastplay = ""
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
b = 0
agif = False
pgif = False
cgif = False

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
        #Reset mid-play situation bgif
        global cgif
        cgif = False

        _render_inning_break(canvas, layout, colors, scoreboard.inning)

        #Hide Due Up during 7th inning stretch animation (BUG: b not get reset for multiple games between innings going into stretch (only reset when showing active game)
        global b
        if (scoreboard.inning.number==7) and (scoreboard.inning.state=="Middle") and (b < 110):
            b += 1
        else:
            _render_due_up(canvas, layout, colors, scoreboard.atbat, text_pos)

    return pos


# --------------- at-bat ---------------
def _render_at_bat(canvas, layout, colors, atbat: AtBat, text_pos, play_result, animation, pitches: Pitches):
    blength = __render_batter_text(canvas, layout, colors, atbat.batter, text_pos)

    # print(str(blength))
    # __render_pitch_text(canvas, layout, colors, pitches)
    # __render_pitch_count(canvas, layout, colors, pitches)

    results = list(PLAY_RESULTS.keys())
    #hresults = list(HITS)
    wresults = list(WALKS)
    oresults = list(OUTS)
    skresults = list(STRIKEOUTS)
    sresults = list(SCORING)
    #othresults = list(OTHERS)

    #__render_play_result(canvas, layout, colors, play_result)

    plength = __render_pitcher_text(canvas, layout, colors, atbat.pitcher, pitches, text_pos)
    #print(str(plength))

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
    global b
    global agif
    global pgif

    #global lastplay
    #lastplay = play_result
    #if (play_result != "") and (lastplay != play_result):
       #print("render_at_bat play_result: " + play_result)

    if play_result in results and __should_render_play_result(play_result, layout):
        #print("Play result in results and should render: " + play_result + ", Animation=" + str(animation) + " blength=" + str(blength))

        if agif==False: 
            animation_gif(play_result)

        if "home_run" in play_result:
            #animation_chase(canvas, colors)
            animation_crown3(canvas, colors)
        elif (play_result in wresults) and (play_result not in sresults):
            animation = 1
            animation_chase(canvas, colors)
        elif (play_result in oresults) or (play_result in skresults):
            animation = 1
        elif (play_result not in sresults) and (play_result not in oresults) and (play_result not in skresults):
            animation = 1
            #animation_chase(canvas, colors)
            animation_crown(canvas, colors)

        if animation:
            __render_play_result(canvas, layout, colors, play_result)

        #Blank space for gif (must be after play display code
        bgcolor = colors.graphics_color("default.background")
        #tcolor = colors.graphics_color("standings.al.divider")
        xMax = canvas.width
        xMin = 1
        fblank = False

        yMin = 20 #14 21-26
        yMax = yMin+6
        xS = xMax-19

        if fblank is True:
            yMin = 13
            yMax = canvas.height

        #CHANGE gif blanking time
        b += 1    
        if (b < 95 and pgif==True):
            for i in range (yMin, yMax):
                graphics.DrawLine(canvas, xMin, i, xS, i, bgcolor)

        return plength
        #return max(plength, blength)
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
        b = 0
        agif = False
        pgif = False

        #blength = __render_batter_text(canvas, layout, colors, atbat.batter, text_pos)

        __render_pitch_text(canvas, layout, colors, pitches)
        __render_pitch_count(canvas, layout, colors, pitches)
        _render_count(canvas, layout, colors, pitches)

        return max(plength, blength)


def animation_gif(play_result):
    #agif ensures the gif playing utility and randomizer is only called once
    global agif
    #pgif tells the scoreboard a gif has been played, so do required things (blank the space)
    global pgif
    #results = list(PLAY_RESULTS.keys())
    #hresults = list(HITS)
    #wresults = list(WALKS)
    oresults = list(OUTS)
    skresults = list(STRIKEOUTS)
    #sresults = list(SCORING)
    #othresults = list(OTHERS)

    #CHANGE depending on your setup! Animations folder MUST also be copied to ".../mlb-led-scoreboard/assets/animations"
    home = "/home/bof"

    #CHANGE depending on desired amount of animations. Bonuses given to infrequent plays, so change to -1 to turn off completely!
    chance = .5

    liv = home + "/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer"

    #DISABLE TO CLEAN UP LOGS
    #print("Play Gif? " + play_result, flush=True)

    if play_result in skresults and agif==False:
        agif = True
        rdm = random()
        ch = chance/2
        if rdm < ch:
            gifp = "/mlb-led-scoreboard/assets/animations/so.gif"
            g = home + gifp
            pgif = True
            print("gif: so", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D700", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch) and (rdm < chance):
            gifp = "/mlb-led-scoreboard/assets/animations/so2.gif"
            g = home + gifp
            pgif = True
            print("gif: so2", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D700", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    elif "home_run" in play_result and agif==False:
        agif = True
        rdm = random()
        if rdm < .5:
            gifp = "/mlb-led-scoreboard/assets/animations/fireworks.gif"
            g = home + gifp
            print("gif: fireworks", flush=True)
            gif = subprocess.Popen([liv, "-l3", "-D420", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        else:
            gifp = "/mlb-led-scoreboard/assets/animations/fireworks2.gif"
            g = home + gifp
            print("gif: fireworks2", flush=True)
            gif = subprocess.Popen([liv, "-l3", "-D160", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    elif "walk" in play_result and agif==False:
        agif = True
        rdm = random()
        ch = chance/2
        if rdm < ch:
            gifp = "/mlb-led-scoreboard/assets/animations/walk.gif"
            g = home + gifp
            pgif = True
            print("gif: walk", flush=True)
            gif = subprocess.Popen([liv, "-l3", "-D1000", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch) and (rdm < chance):
            gifp = "/mlb-led-scoreboard/assets/animations/walk2.gif"
            g = home + gifp
            pgif = True
            print("gif: baseonballs", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D700", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif rdm > .95:
            gifp = "/mlb-led-scoreboard/assets/animations/walk3.gif"
            g = home + gifp
            pgif = True
            print("gif: submarine", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D400", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    elif "hit_by_pitch" in play_result and agif==False:
        agif = True
        rdm = random()
        if rdm < chance+.2:
            gifp = "/mlb-led-scoreboard/assets/animations/hbp.gif"
            g = home + gifp
            pgif = True
            print("gif: hbp", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D800", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=70", "--led-slowdown-gpio=5"])
    elif "field_out_fly" in play_result and agif==False:
        agif = True
        rdm = random()
        ch = chance/3
        if rdm < ch:
            gifp = "/mlb-led-scoreboard/assets/animations/fly.gif"
            g = home + gifp
            pgif = True
            print("gif: fly", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D700", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch) and (rdm < ch*2):
            gifp = "/mlb-led-scoreboard/assets/animations/corn.gif"
            g = home + gifp
            pgif = True
            print("gif: corn", flush=True)
            gif = subprocess.Popen([liv, "-l5", "-D500", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch*2) and (rdm < ch*3):
            gifp = "/mlb-led-scoreboard/assets/animations/lazy.gif"
            g = home + gifp
            pgif = True
            print("gif: lazy", flush=True)
            gif = subprocess.Popen([liv, "-l3", "-D1500", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    elif "field_out_pop" in play_result and agif==False:
        agif = True
        rdm = random()
        ch = chance/2
        if rdm < ch:
            gifp = "/mlb-led-scoreboard/assets/animations/pop2.gif"
            g = home + gifp
            pgif = True
            print("gif: pop2", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D900", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch) and (rdm < ch*2):
            gifp = "/mlb-led-scoreboard/assets/animations/pop.gif"
            g = home + gifp
            pgif = True
            print("gif: pop", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D500", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    elif "field_out_ground" in play_result and agif==False:
        agif = True
        rdm = random()
        ch = chance/3
        if rdm < ch:
            gifp = "/mlb-led-scoreboard/assets/animations/grounder.gif"
            g = home + gifp
            pgif = True
            print("gif: grounder", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D800", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch) and (rdm < ch*2):
            gifp = "/mlb-led-scoreboard/assets/animations/grounder2.gif"
            g = home + gifp
            pgif = True
            print("gif: grounder2", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D800", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch*2) and (rdm < ch*3):
            gifp = "/mlb-led-scoreboard/assets/animations/grounder3.gif"
            g = home + gifp
            pgif = True
            print("gif: grounder3", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D640", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    elif "field_out_line" in play_result and agif==False:
        agif = True
        rdm = random()
        ch = chance/2
        if rdm < ch:
            gifp = "/mlb-led-scoreboard/assets/animations/lineout.gif"
            g = home + gifp
            pgif = True
            print("gif: lineout", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D700", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch) and (rdm < chance):
            gifp = "/mlb-led-scoreboard/assets/animations/bullet.gif"
            g = home + gifp
            pgif = True
            print("gif: bullet", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D450", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    elif "double_play" in play_result and agif==False:
        agif = True
        rdm = random()
        if rdm < chance + .2:
            gifp = "/mlb-led-scoreboard/assets/animations/dp.gif"
            g = home + gifp
            pgif = True
            print("gif: 643", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D1000", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    elif "sac_fly" in play_result and agif==False:
        agif = True
        if random() < chance+.2:
            gifp = "/mlb-led-scoreboard/assets/animations/sacfly.gif"
            g = home + gifp
            pgif = True
            print("gif: sacfly", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D1750", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    elif "stolen_base_home" in play_result and agif==False:
        agif = True
        rdm = random()
        if rdm < .5:
            gifp = "/mlb-led-scoreboard/assets/animations/fireworks.gif"
            g = home + gifp
            gif = subprocess.Popen([liv, "-l2", "-D450", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=70", "--led-slowdown-gpio=4"])
        else:
            gifp = "/mlb-led-scoreboard/assets/animations/fireworks2.gif"
            g = home + gifp
            gif = subprocess.Popen([liv, "-l3", "-D160", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=70", "--led-slowdown-gpio=4"])
    elif "stolen_base" in play_result and agif==False:
        agif = True
        if random() < chance+.2:
            gifp = "/mlb-led-scoreboard/assets/animations/sb.gif"
            g = home + gifp
            pgif = True
            print("gif: sb", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D650", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    elif "seventh" in play_result and agif==False:
        agif = True
        rdm = random()
        if rdm < .25:
            gifp = "/mlb-led-scoreboard/assets/animations/seventh.gif"
            g = home + gifp
            print("gif: seventh1", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D600", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= .25) and (rdm < .5):
            gifp = "/mlb-led-scoreboard/assets/animations/seventh2.gif"
            g = home + gifp
            print("gif: seventh2", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D600", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= .5) and (rdm < .75):
            gifp = "/mlb-led-scoreboard/assets/animations/seventh3.gif"
            g = home + gifp
            print("gif: seventh3", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D600", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        else:
            gifp = "/mlb-led-scoreboard/assets/animations/seventh4.gif"
            g = home + gifp
            print("gif: seventh4", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D600", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    elif "ducks" in play_result and agif==False:
        agif = True
        rdm = random()
        if rdm < chance:
            gifp = "/mlb-led-scoreboard/assets/animations/ducks.gif"
            g = home + gifp
            pgif = True
            print("gif: seventh1", flush=True)
            gif = subprocess.Popen([liv, "-l4", "-D900", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
    elif play_result not in oresults and agif==False:
        agif = True
        rdm = random()
        ch = (chance+.1)/8
        if rdm < ch:
            gifp = "/mlb-led-scoreboard/assets/animations/clap.gif"
            g = home + gifp
            pgif = True
            print("gif: Hclap", flush=True)
            gif = subprocess.Popen([liv, "-l8", "-D350", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch) and (rdm < ch*2):
            gifp = "/mlb-led-scoreboard/assets/animations/super.gif"
            g = home + gifp
            pgif = True
            print("gif: Hsuper", flush=True)
            gif = subprocess.Popen([liv, "-l5", "-D360", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch*2) and (rdm < ch*3):
            gifp = "/mlb-led-scoreboard/assets/animations/ao.gif"
            g = home + gifp
            pgif = True
            print("gif: Hao", flush=True)
            gif = subprocess.Popen([liv, "-l6", "-D830", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch*3) and (rdm < ch*4):
            gifp = "/mlb-led-scoreboard/assets/animations/charge.gif"
            g = home + gifp
            pgif = True
            print("gif: Hcharge", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D1200", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch*4) and (rdm < ch*5):
            gifp = "/mlb-led-scoreboard/assets/animations/clapletsgo.gif"
            g = home + gifp
            pgif = True
            print("gif: Hclap2", flush=True)
            gif = subprocess.Popen([liv, "-l2", "-D180", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch*5) and (rdm < ch*6):
            gifp = "/mlb-led-scoreboard/assets/animations/king.gif"
            g = home + gifp
            pgif = True
            print("gif: Hking", flush=True)
            gif = subprocess.Popen([liv, "-l4", "-D1000", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch*6) and (rdm < ch*7):
            gifp = "/mlb-led-scoreboard/assets/animations/wave.gif"
            g = home + gifp
            pgif = True
            print("gif: Hwave", flush=True)
            gif = subprocess.Popen([liv, "-l1", "-D400", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])
        elif (rdm >= ch*7) and (rdm < ch*8):
            gifp = "/mlb-led-scoreboard/assets/animations/wave2.gif"
            g = home + gifp
            pgif = True
            print("gif: Hwave2", flush=True)
            gif = subprocess.Popen([liv, "-l2", "-D400", g, "--led-gpio-mapping=adafruit-hat", "--led-rows=32", "--led-cols=64", "--led-brightness=55", "--led-slowdown-gpio=4"])


def animation_ring(canvas, color):
    xMax = canvas.width
    yMax = canvas.height
    xMin = 0 #must stay 0
    yMin = 14 #14
    xS = xMax-1
    xH = xMax/2 
    yS = yMax-1

    graphics.DrawLine(canvas, xMin, yS, xS, yS, color)
    graphics.DrawLine(canvas, xMin, yMin, xS, yMin, color)
    graphics.DrawLine(canvas, xMin, yMin, xMin, yS, color)
    graphics.DrawLine(canvas, xS, yMin, xS, yS, color)


def animation_stripe(canvas, colors):
        global x
        global y

        color0 = colors.graphics_color("default.background")
        color1 = colors.graphics_color("offday.time")

        xMax = canvas.width
        yMax = canvas.height
        xMin = 0 #must stay 0
        yMin = 14 #14
        xS = xMax-1
        xH = xMax/2 
        yS = yMax-1

        for x in range (xMin, xMax):
            if (x % 4) > 0:
                graphics.DrawLine(canvas, x, yS, x, yS, color0)
                graphics.DrawLine(canvas, x, yMin, x, yMin, color0)
            else:
                graphics.DrawLine(canvas, x, yS, x, yS, color1)
                graphics.DrawLine(canvas, x, yMin, x, yMin, color1)
        for y in range (yMin, yMax):
            if (y % 4) > 0:
                graphics.DrawLine(canvas, xMin, y, xMin, y, color0)
                graphics.DrawLine(canvas, xS, y, xS, y, color0)
            else:
                graphics.DrawLine(canvas, xMin, y, xMin, y, color1)
                graphics.DrawLine(canvas, xS, y, xS, y, color1)


def animation_chase(canvas, colors):
        global x
        global y
        global z
        global xo
        global yo
        global zo
        global w
        global o

        color = colors.graphics_color("offday.time")
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

        if (xMin == 0):
            if (w >= 20):
                w += 1
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x+2, yS, x+2, yS, color0)
                        graphics.DrawLine(canvas, x-2, yMin, x-2, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x+2, yS, x+2, yS, color)
                        graphics.DrawLine(canvas, x-2, yMin, x-2, yMin, color)
                for y in range (yMin+1, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y+1, xMin, y+1, color0)
                        graphics.DrawLine(canvas, xS, y-1, xS, y-1, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y+1, xMin, y+1, color)
                        graphics.DrawLine(canvas, xS, y-1, xS, y-1, color)
                if (w > 29):
                    w = 0
            elif (w >= 10):
                w += 1
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x+1, yS, x+1, yS, color0)
                        graphics.DrawLine(canvas, x-1, yMin, x-1, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x+1, yS, x+1, yS, color)
                        graphics.DrawLine(canvas, x-1, yMin, x-1, yMin, color)
                for y in range (yMin+1, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y, xMin, y, color0)
                        graphics.DrawLine(canvas, xS, y, xS, y, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y, xMin, y, color)
                        graphics.DrawLine(canvas, xS, y, xS, y, color)
            else:
                w += 1
                for x in range (xMin, xMax):
                    if (x % i) > 0:
                        graphics.DrawLine(canvas, x, yS, x, yS, color0)
                        graphics.DrawLine(canvas, x, yMin, x, yMin, color0)
                    else:
                        graphics.DrawLine(canvas, x, yS, x, yS, color)
                        graphics.DrawLine(canvas, x, yMin, x, yMin, color)
                for y in range (yMin+1, yMax):
                    if (y % i) > 0:
                        graphics.DrawLine(canvas, xMin, y-1, xMin, y-1, color0)
                        graphics.DrawLine(canvas, xS, y+1, xS, y+1, color0)
                    else:
                        graphics.DrawLine(canvas, xMin, y-1, xMin, y-1, color)
                        graphics.DrawLine(canvas, xS, y+1, xS, y+1, color)


def animation_crown(canvas, colors):
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

        color = colors.graphics_color("offday.time")
        color2 = colors.graphics_color("default.background")
        xMax = canvas.width
        yMax = canvas.height
        xMin = 0 #must stay 0
        yMin = 14 #14
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
        elif w < 0:
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
        color1 = colors.graphics_color("standings.nl.divider")
        color2 = colors.graphics_color("atbat.play_result")
        color3 = colors.graphics_color("standings.al.divider")
        xMax = canvas.width
        yMax = canvas.height
        xMin = 0 #must stay 0
        yMin = 14 #14
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
        elif o <= 1000:
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


def __should_render_play_result(play_result, layout):
    #print("Render? " + play_result)
    if "strikeout" in play_result:
        coords = layout.coords("atbat.strikeout")
    else:
        coords = layout.coords("atbat.play_result")
    return coords["enabled"]


def __render_play_result(canvas, layout, colors, play_result):
    #results = list(PLAY_RESULTS.keys())
    #hresults = list(HITS)
    wresults = list(WALKS)
    #oresults = list(OUTS)
    skresults = list(STRIKEOUTS)
    sresults = list(SCORING)
    #othresults = list(OTHERS)
    #print("Rendering " +  play_result)

    #color = colors.graphics_color("atbat.play_result")
    #color2 = colors.graphics_color("default.background")
    #coords = layout.coords("atbat.play_result")
    #font = layout.font("atbat.play_result")

    if "home_run" in play_result:
        color = colors.graphics_color("atbat.play_result")
        color2 = colors.graphics_color("atbat.play_result")
        coords = layout.coords("atbat.play_result")
        font = layout.font("atbat.play_result")
    elif play_result in sresults:
        color = colors.graphics_color("atbat.play_result")
        color2 = colors.graphics_color("atbat.batter")
        coords = layout.coords("atbat.play_result")
        font = layout.font("atbat.play_result")
        animation_ring(canvas, color2)
    elif play_result in skresults:
        color = colors.graphics_color("atbat.strikeout")
        color2 = colors.graphics_color("atbat.strikeout")
        coords = layout.coords("atbat.strikeout")
        font = layout.font("atbat.strikeout")
        animation_ring(canvas, color2)
    else:
        color = colors.graphics_color("atbat.play_result")
        color2 = colors.graphics_color("default.background")
        coords = layout.coords("atbat.play_result")
        font = layout.font("atbat.play_result")

    try:
        text = PLAY_RESULTS[play_result][coords["desc_length"].lower()]
    except KeyError:
        return

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

    #BASES LOADED ANIMATION Ducks on the pond
    global cgif
    #if (base_runners[0]) and (cgif == False):
    if base_runners[0] and base_runners[1] and base_runners[2] and (cgif == False):
        #tcolor = colors.graphics_color("standings.nl.divider")
        #graphics.DrawLine(canvas, 0, 26, 45, 26, tcolor)
        cgif = True
        animation_gif("ducks") #WILL RUN ANIMATION INIFINITELY AND CRASH BOARD


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

    bgcolor = colors.graphics_color("default.background")
    tcolor = colors.graphics_color("standings.nl.divider")

    scolor = colors.graphics_color("standings.al.divider")
    bcolor = colors.graphics_color("standings.nl.divider")

    # Toggle between showing count at circles and numbers
    cCount = True

    xMax = canvas.width
    xMin = 1
    fblank = False

    yMin = 20 #14 21-26
    yMax = yMin+6
    xS = xMax-19

    if fblank is True:
        yMin = 13
        yMax = canvas.height

    #Fix instance where walk or strikeout happens but isn't recorded as a play result
    if pitches.balls > 3:
        #Extra blank pixel to cover bottom of pitches P
        graphics.DrawLine(canvas, 39, yMax, 43, yMax, bgcolor)
        for i in range (yMin, yMax):
            graphics.DrawLine(canvas, xMin, i, xS, i, bgcolor)
        __render_play_result(canvas, layout, colors, "walk")
        animation_chase(canvas, colors)
        #animation_gif("walk") WILL RUN ANIMATION INIFINITELY AND CRASH BOARD
    elif pitches.strikes > 2:
        #Extra blank pixel to cover bottom of pitches P
        graphics.DrawLine(canvas, 39, yMax, 43, yMax, bgcolor)
        for i in range (yMin, yMax):
            graphics.DrawLine(canvas, xMin, i, xS, i, bgcolor)
        __render_play_result(canvas, layout, colors, "strikeout")

        color2 = colors.graphics_color("atbat.strikeout")
        animation_ring(canvas, color2)
        #animation_gif("strikeout") WILL RUN ANIMATION INIFINITELY AND CRASH BOARD
    else:
        if cCount:
            _render_ccount(canvas, layout, colors, pitches)
        else:
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
        graphics.DrawLine(canvas, x, y + y_offset, x + size - 2, y + y_offset, color)


# --------------- count circles ---------------
def __cball_colors(colors):
    outlines = []
    fills = []
    for i in range(3):
        color = colors.graphics_color(f"cballs.{i+1}")
        outlines.append(color)
        try:
            color = colors.graphics_color(f"cballs.fill.{i+1}")
        except KeyError:
            pass
        fills.append(color)
    return outlines, fills

def __cstrike_colors(colors):
    outlines = []
    fills = []
    for i in range(2):
        color = colors.graphics_color(f"cstrikes.{i+1}")
        outlines.append(color)
        try:
            color = colors.graphics_color(f"cstrikes.fill.{i+1}")
        except KeyError:
            pass
        fills.append(color)
    return outlines, fills

def _render_ccount(canvas, layout, colors, pitches):
    ball_px = []
    ball_px.append(layout.coords("cballs.1"))
    ball_px.append(layout.coords("cballs.2"))
    ball_px.append(layout.coords("cballs.3"))

    strike_px = []
    strike_px.append(layout.coords("cstrikes.1"))
    strike_px.append(layout.coords("cstrikes.2"))

    ball_colors = []
    ball_colors, bfill_colors = __cball_colors(colors)

    strike_colors = []
    strike_colors, sfill_colors = __cstrike_colors(colors)

    #pitches.strikes > 2:
    for ball in range(len(ball_px)):
        __render_count_circle(canvas, ball_px[ball], ball_colors[ball])
        # Fill in the circle if that out has occurred
        if pitches.balls > ball:
            __fill_count_circle(canvas, ball_px[ball], bfill_colors[ball])

    for strike in range(len(strike_px)):
        __render_count_circle(canvas, strike_px[strike], strike_colors[strike])
        # Fill in the circle if that out has occurred
        if pitches.strikes > strike:
            __fill_count_circle(canvas, strike_px[strike], sfill_colors[strike])


def __render_count_circle(canvas, ball, color):
    x, y, size = (ball["x"], ball["y"], ball["size"])

    graphics.DrawLine(canvas, x+1, y, x + size-2, y, color)
    graphics.DrawLine(canvas, x, y+1, x, y + size-2, color)
    graphics.DrawLine(canvas, x + size-2, y + size-1, x+1, y + size-1, color)
    graphics.DrawLine(canvas, x + size-1, y + size-2, x + size-1, y+1, color)


def __fill_count_circle(canvas, ball, color):
    size = ball["size"]
    x, y = (ball["x"], ball["y"])
    x += 1
    y += 1
    size -= 1
    for y_offset in range(size-1):
        graphics.DrawLine(canvas, x, y + y_offset, x + size - 2, y + y_offset, color)


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
    
    #Fix 10th ordinal being too long for space
    if inning.number > 9:
        num = str(inning.number)
    else:
        num = inning.ordinal

    graphics.DrawText(canvas, num_font["font"], num_coords["x"], num_coords["y"], color, num)

    #Seventh inning stetch gif
    if (inning.number==7) and (text=="Mid"):
        animation_gif("seventh")

    #Render inning arrow between innings
    #print(inning.state)
    #null = inning.state is None
    #end = inning.state == "End"
    #mid = inning.state == "Middle"
    #if null:
    #    inning.state = "Top"
    #elif end:
    #    inning.state = "Top"
    #elif mid:
    #    inning.state = "Bottom"
    #__render_inning_half(canvas, layout, colors, inning)

    font = layout.font("inning.number")
    num_coords = layout.coords("inning.number")
    arrow_coords = layout.coords("inning.arrow")
    inning_size = len(str(inning.number)) * font["size"]["width"]
    size = arrow_coords["size"]
    top = inning.state == Inning.END
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



def _render_due_up(canvas, layout, colors, atbat: AtBat, text_pos):
    batter_font = layout.font("inning.break.due_up.leadoff")
    batter_color = colors.graphics_color("inning.break.due_up_names")

    leadoff = layout.coords("inning.break.due_up.leadoff")
    on_deck = layout.coords("inning.break.due_up.on_deck")
    in_hole = layout.coords("inning.break.due_up.in_hole")

    coords = layout.coords("inning.break.due_up.leadoff")
    offsetL = leadoff.get("offset", 0)
    offsetO = on_deck.get("offset", 0)
    offsetH = in_hole.get("offset", 0)

    #print("offsetL:" + str(offsetL))
    #print("offsetO:" + str(offsetO))
    #print("offsetH:" + str(offsetH))
    #print("text_pos:" + str(text_pos))

    font = layout.font("inning.break.due_up.leadoff")
    color = colors.graphics_color("inning.break.due_up_names")
    bgcolor = colors.graphics_color("default.background")

    #29, 20-26-32,35
    scroll = False
    largeSpace = True

    if scroll:
        lead = scrollingtext.render_text(
            canvas,
            leadoff["x"],
            leadoff["y"],
            leadoff["width"],
            font,
            color,
            bgcolor,
            atbat.batter,
            text_pos+offsetL,
            center=False,
        )

        deck = scrollingtext.render_text(
            canvas,
            on_deck["x"],
            on_deck["y"],
            on_deck["width"],
            font,
            color,
            bgcolor,
            atbat.onDeck,
            text_pos+offsetO,
            center=False,
        )

        hole = scrollingtext.render_text(
            canvas,
            in_hole["x"],
            in_hole["y"],
            in_hole["width"],
            font,
            color,
            bgcolor,
            atbat.inHole,
            text_pos+offsetH,
            center=False,
        )
    else:
        if largeSpace:
            graphics.DrawText(canvas, batter_font["font"], leadoff["x"]-13, leadoff["y"], batter_color, atbat.batter)
            graphics.DrawText(canvas, batter_font["font"], on_deck["x"]-13, on_deck["y"], batter_color, atbat.onDeck)
            graphics.DrawText(canvas, batter_font["font"], in_hole["x"]-13, in_hole["y"], batter_color, atbat.inHole)
        else:
            graphics.DrawText(canvas, batter_font["font"], leadoff["x"], leadoff["y"], batter_color, atbat.batter)
            graphics.DrawText(canvas, batter_font["font"], on_deck["x"], on_deck["y"], batter_color, atbat.onDeck)
            graphics.DrawText(canvas, batter_font["font"], in_hole["x"], in_hole["y"], batter_color, atbat.inHole)


    due_font = layout.font("inning.break.due_up.due")
    due_color = colors.graphics_color("inning.break.due_up")

    if not largeSpace:
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
