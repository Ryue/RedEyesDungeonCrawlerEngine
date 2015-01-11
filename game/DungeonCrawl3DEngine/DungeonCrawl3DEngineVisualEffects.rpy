init -1:
    transform movingImageTransformation(start, end, t):
        subpixel True
        xpos start
        linear t xpos end
        repeat
    

    screen MovingHorizontalAnimationScreen(posX, posY, width, height, imageInternalName, tagName, fastness = 15):
        tag tagName
        modal False
        viewport:
            xpos posX
            ypos posY
            xysize(width, height)
            add im.Scale(ImageReference(imageInternalName), width, height) at movingImageTransformation(0, -width, fastness)
            add im.Scale(ImageReference(imageInternalName), width, height) at movingImageTransformation(width, 0, fastness)

    image SpecialEffect001:
        animation
        LiveComposite((2732,768),
                        (1366,0),ImageReference("OverlayFrontSideOverlayDistance0TileNameOverlay001"),
                        (0,0),ImageReference("OverlayFrontSideOverlayDistance0TileNameOverlay001"))
        xpos 1366
        linear 120.0 xpos 0
        repeat  

    transform TransformMoveLeft(start_pos=(0, 0)):
        anchor (0, 0)
        pos start_pos
        linear 60 xpos 0
        repeat

init -50 python:
    from copy import copy
    import math
    class Shaker(object):
        anchors = {
            'top' : 0.0,
            'center' : 0.5,
            'bottom' : 1.0,
            'left' : 0.0,
            'right' : 1.0,
            }
    
        def __init__(self, start, child, dist):
            if start is None:
                start = child.get_placement()
            #
            self.start = [ self.anchors.get(i, i) for i in start ]  # central position
            self.dist = dist    # maximum distance, in pixels, from the starting point
            self.child = child
            
        def __call__(self, t, sizes):
            # Float to integer... turns floating point numbers to
            # integers.                
            def fti(x, r):
                if x is None:
                    x = 0
                if isinstance(x, float):
                    return int(x * r)
                else:
                    return x

            xpos, ypos, xanchor, yanchor = [ fti(a, b) for a, b in zip(self.start, sizes) ]

            xpos = xpos - xanchor
            ypos = ypos - yanchor
            
            nx = xpos + (1.0-t) * self.dist * (renpy.random.random()*2-1)
            ny = ypos + (1.0-t) * self.dist * (renpy.random.random()*2-1)

            return (int(nx), int(ny), 0, 0)
    
    def _Shake(start, time, child=None, dist=100.0, **properties):

        move = Shaker(start, child, dist=dist)
    
        return renpy.display.layout.Motion(move,
                      time,
                      child,
                      add_sizes=True,
                      **properties)

    Shake = renpy.curry(_Shake) 