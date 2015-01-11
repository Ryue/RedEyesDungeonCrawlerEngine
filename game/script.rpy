# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.
define e = Character('Eileen', color="#c8ffc8")

init:
    screen crawlMove:
        key "K_KP8" action Return(value=8)
        key "K_KP6" action Return(value=6)
        key "K_KP2" action Return(value=2)
        key "K_KP4" action Return(value=4)

        fixed:
            #if front.map[front.y][front.x] is not 1:
            textbutton "↑" action Return(value=8)  xcenter .5 ycenter .34
            textbutton "→" action Return(value=6) xcenter .57 ycenter .47
            textbutton "↓" action Return(value=2) xcenter .5 ycenter .6
            textbutton "←" action Return(value=4) xcenter .43 ycenter .47

# The game starts here.
label start:
    python:
        dungeonCrawl3DEngine = ClsDungeonCrawl3DEngine()
        dungeonCrawl3DEngine.viewCurrentMap = "mytest"
        crawlMoveCommand = 0
        dungeonCrawl3DEngine.viewX = 3
#        dungeonCrawl3DEngine.viewY = 11
        dungeonCrawl3DEngine.viewDir = 2
    
    while (1):
        python:
            renpy.scene()
            dungeonCrawl3DEngine.RenderView()
            #renpy.call_screen("MovingHorizontalAnimationScreen", 400, 50, 800, 646,"OverlayFrontSideOverlay001")

            crawlMoveCommand = renpy.call_screen("crawlMove")

            if (crawlMoveCommand == 8):
                dungeonCrawl3DEngine.MoveForward()
            elif (crawlMoveCommand == 2):
                dungeonCrawl3DEngine.MoveBackward()
            elif (crawlMoveCommand == 4):
                dungeonCrawl3DEngine.MoveTurnLeft()
            elif (crawlMoveCommand == 6):
                dungeonCrawl3DEngine.MoveTurnRight()
            
    return
