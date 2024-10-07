#These gifs were created for a 64x32 board. I am not sure how they will display on other sizes. They were also specifically created with my layout in mind, but generally will be fine elsewhere, but there is no gurantees. They are called in renderers/game/game.py using the "home" variable in that file. THIS MUST BE CHANGED TO YOUR HOME DIRECTORY FOR THEM TO FUNCTION (excerpt below)

    #CHANGE depending on your setup! Animations folder MUST also be copied to ".../mlb-led-scoreboard/assets/animations"
    home = "/home/bof"

You also must "make" the utility for playing gifs in order for the gifs to play. I did so below with the following commands:
cd rpi-rgb-led-matrix directory
sudo apt-get update
sudo apt-get install libgraphicsmagick++-dev libwebp-dev -y
cd utils
make led-image-viewer

Once you believe things are set up, use the below example command to see if things are functioning correctly
Example command to play a gif:
sudo ~/mlb-led-scoreboard/rpi-rgb-led-matrix/utils/led-image-viewer -l4 -D420 /home/bof/mlb-led-scoreboard/assets/animations/fireworks.gif --led-gpio-mapping="adafruit-hat" --led-rows=32 --led-cols=64 --led-brightness=80 --led-slowdown-gpio=4
