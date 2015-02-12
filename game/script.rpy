# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.
define e = Character('Eileen', color="#c8ffc8")

init:
    screen crawlMove:
        
        # Sets up the numpad controls to move the player when pressed
        key "K_KP8" action Return(value='F')
        key "K_KP6" action Return(value='R')
        key "K_KP2" action Return(value='B')
        key "K_KP4" action Return(value='L')
        
        fixed:
            # Displays the arrow buttons to move the player when clicked
            textbutton "↑" action Return(value='F') xcenter .5 ycenter .34
            textbutton "→" action Return(value='R') xcenter .57 ycenter .47
            textbutton "↓" action Return(value='B') xcenter .5 ycenter .6
            textbutton "←" action Return(value='L') xcenter .43 ycenter .47
            
# The game starts here.
label start:
    python:
        
        # Instantiate the Dungeon Crawl 3D engine
        dungeonCrawl3DEngine = ClsDungeonCrawl3DEngine()
        
        # Load the specified map file from "Data/Maps/"
        dungeonCrawl3DEngine.viewCurrentMap = "mytest"
        
        # Initialize the starting coordinates and direction
        crawlMoveCommand = 0
        dungeonCrawl3DEngine.viewX = 4
        dungeonCrawl3DEngine.viewY = 2
        dungeonCrawl3DEngine.viewDir = 0
    
    # Loop forever
    while (1):
        python:
            
            # Render the scene using the Dungeon Crawl 3D Engine
            renpy.scene()
            dungeonCrawl3DEngine.RenderView()

            # Check for user input, and move accordingly
            crawlMoveCommand = renpy.call_screen("crawlMove")

            if (crawlMoveCommand == 'F'):
                dungeonCrawl3DEngine.MoveForward()
            elif (crawlMoveCommand == 'B'):
                dungeonCrawl3DEngine.MoveBackward()
            elif (crawlMoveCommand == 'L'):
                dungeonCrawl3DEngine.MoveTurnLeft()
            elif (crawlMoveCommand == 'R'):
                dungeonCrawl3DEngine.MoveTurnRight()
            
    return
