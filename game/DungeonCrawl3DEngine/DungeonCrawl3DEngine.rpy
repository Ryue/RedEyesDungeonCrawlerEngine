init -50 python:
    import string

    class ClsDungeonTileSizeConfig:
        def __init__(self, frontTileWidth, frontTileHeight, sideTileWidth, sideTileHeight):
            self.frontTileWidth  = frontTileWidth
            self.frontTileHeight = frontTileHeight
            self.sideTileWidth   = sideTileWidth
            self.sideTileHeight  = sideTileHeight

    class ClsDungeonMapTile:
        def __init__(self, backgroundNumber, tileNumber, tileMaxNumberAnimation, tileCurrentNumberAnimation, tileVisibility, tileSpecialEffects, tileBlocking, tileEventNumber, tileSeen = 0):
            self.backgroundNumber = backgroundNumber
            self.tileNumber = tileNumber
            self.tileMaxNumberAnimation = tileMaxNumberAnimation
            self.tileCurrentNumberAnimation = tileCurrentNumberAnimation
            if (str(tileVisibility).isdigit()):
                self.tileVisibility = tileVisibility
            else:
                self.tileVisibility = 0
            self.tileSpecialEffects = tileSpecialEffects
            self.tileBlocking = int(tileBlocking)
            self.tileEventNumber = str(tileEventNumber).ljust(3, '0')
            self.tileSeen = tileSeen

    class ClsDungeonMap:
        def __init__(self, fileName, mapMaxX, mapMaxY):
            self.mapName = fileName.replace("_", " ")
            self.mapTilesArray = []
            currentY = 0

            while (currentY <= mapMaxY):
                currentX = 0
                
                mapTilesColumnData = []
                while (currentX <= mapMaxX):
                    mapTilesColumnData.append(ClsDungeonMapTile(
                        backgroundNumber = "001",
                        tileNumber = 0,
                        tileMaxNumberAnimation = 0,
                        tileCurrentNumberAnimation = 0,
                        tileVisibility = 0,
                        tileSpecialEffects = 0,
                        tileBlocking = 0,
                        tileEventNumber = 0
                    ))
                    currentX = currentX + 1
                self.mapTilesArray.append(mapTilesColumnData)
                currentY = currentY + 1

    class ClsDungeonCrawl3DEngine:

        # Initializes and configures the 3D engine
        def __init__(self):
            # Engine configurations
            self.screenWidth  = 1366
            self.screenHeight =  768
            self.maxMapX      =  512
            self.maxMapY      =  512

            self.tileSizesAtDistance = []
            self.tileSizesAtDistance.append(ClsDungeonTileSizeConfig(1366, 768, 142, 768))
            self.tileSizesAtDistance.append(ClsDungeonTileSizeConfig(1081, 608, 113, 608))
            self.tileSizesAtDistance.append(ClsDungeonTileSizeConfig(855, 481, 90, 481))
            self.tileSizesAtDistance.append(ClsDungeonTileSizeConfig(675, 380, 71, 380))
            self.tileSizesAtDistance.append(ClsDungeonTileSizeConfig(533, 300, 56, 300))
            self.tileSizesAtDistance.append(ClsDungeonTileSizeConfig(421, 237, 44, 237))

            self.imageNamePrefixOverlay = "Overlay"
            self.imageNamePrefixTile    = "Tile"

            # View configurations
            self.viewX            = 1
            self.viewY            = 1
            self.viewLastX        = self.viewX
            self.viewLastY        = self.viewY
            self.viewDir          = 8
            self.viewMovementType = 1 # 1...Walking / Running, 2...Flying
            self.viewCurrentMap   = ""

            # Event handling configurations
            self.fireEventOnEnterCell = True

            # Initialize
            self.InitLoadMaps()

        # Loads all maps that are in a predefined folder
        def InitLoadMaps(self):
            self.dungeonMaps = {}

            fileList = renpy.list_files()
            for fileNameWithPath in fileList:
                fileName = (fileNameWithPath.split("/"))[fileNameWithPath.count("/")][:-4]

                if (fileNameWithPath[:9] == "Data/Maps"):
                    self.dungeonMaps[fileName] = ClsDungeonMap(fileName, self.maxMapX, self.maxMapY)

                    fileContent = renpy.file(fileNameWithPath).read().decode('utf-8')                
                    fileContentLines = fileContent.split("\n")
                    mapX = 0
                    mapY = 0
                    for fileDataLine in fileContentLines:
                        columnArray = fileDataLine.split(";")
                        mapTilesColumnData = []

                        mapX = 0
                        for cellData in columnArray:
                            # ColumnData is in the following format thus split it up accordingly for the new tile: BBB.TTT.CCC.VVV.PPP.LLL.EEE
                            #                                                                       indexposition  012345678901234567890123456
                            # Only set the celldata into the map if it is a valid celldata
                            if (len(cellData) == 27):
                                tileCurrentNumberAnimation = "0"
                                self.dungeonMaps[fileName].mapTilesArray[mapY][mapX] = (ClsDungeonMapTile(
                                    backgroundNumber = cellData[0:3],          #BBB    0,1,2
                                    tileNumber = cellData[4:7],                #TTT    4,5,6
                                    tileMaxNumberAnimation = cellData[8:11],   #CCC    8,9,10
                                    tileCurrentNumberAnimation = 0,             
                                    tileVisibility = cellData[12:15],          #VVV    12,13,14
                                    tileSpecialEffects = cellData[16:19],      #PPP    16,17,18
                                    tileBlocking = cellData[20:23],            #LLL    20,21,22
                                    tileEventNumber = cellData[24:27]          #EEE    24,25,26
                                ))
                            mapX = mapX + 1

                        mapY = mapY + 1

        # RENDER: Renders the current view
        def RenderView(self):
            if (self.viewCurrentMap <> ""):
                self.PrintMapToScreen()

                renpy.show("CrawlerGeneralBackground", zorder = 0)

                renderingDistance = 0
                maxXAdjust = 1
                renderBasePosX = self.viewX
                renderBasePosY = self.viewY

                # Render background
#                RenderPosX, renderPosY = self.CalculateMoveForward(renderBasePosX, renderBasePosY, self.viewDir)
#                if (renderPosY >= 0 and renderPosY < len(self.dungeonMaps[self.viewCurrentMap].mapTilesArray)):                
#                    if (RenderPosX >= 0 and RenderPosX < len(self.dungeonMaps[self.viewCurrentMap].mapTilesArray[renderPosY])):   
#                        renpy.show("CrawlBackground" + str(self.dungeonMaps[self.viewCurrentMap].mapTilesArray[renderPosY][RenderPosX].backgroundNumber))

                # Render tiles directly to left and right of the view
                renderPosX, renderPosY = self.CalculateMoveForward(renderBasePosX, renderBasePosY, self.CalculateTurnLeft(self.viewDir))
                self.renderMapPosition(renderPosX, renderPosY, renderingDistance, -1)
                renderPosX, renderPosY = self.CalculateMoveForward(renderBasePosX, renderBasePosY, self.CalculateTurnRight(self.viewDir))
                self.renderMapPosition(renderPosX, renderPosY, renderingDistance, +1)

                # Render all other distances
                while (renderingDistance < (len(self.tileSizesAtDistance) - 1)):
                    renderBasePosX, renderBasePosY = self.CalculateMoveForward(renderBasePosX, renderBasePosY, self.viewDir)
                    renderingDistance = renderingDistance + 1
                    
                    # Center
                    renderPosX = renderBasePosX
                    renderPosY = renderBasePosY
                    self.renderMapPosition(renderPosX, renderPosY, renderingDistance, 0)

                    renderPosXLeft = renderBasePosX
                    renderPosYLeft = renderBasePosY
                    renderPosXRight = renderBasePosX
                    renderPosYRight = renderBasePosY
                    xAdjust = 1
                    if (renderingDistance >= 3):
                        maxXAdjust = 2

                    while (xAdjust <= maxXAdjust):
                        # To the left
                         renderPosXLeft, renderPosYLeft = self.CalculateMoveForward(renderPosXLeft, renderPosYLeft, self.CalculateTurnLeft(self.viewDir))
                         self.renderMapPosition(renderPosXLeft, renderPosYLeft, renderingDistance, -xAdjust)

                        # To the right
                         renderPosXRight, renderPosYRight = self.CalculateMoveForward(renderPosXRight, renderPosYRight, self.CalculateTurnRight(self.viewDir))
                         self.renderMapPosition(renderPosXRight, renderPosYRight, renderingDistance, +xAdjust)

                         xAdjust = xAdjust + 1

        # INTERN: Prints map to screen
        def PrintMapToScreen(self, screenX=10, screenY=10):
            ui.frame(xpos = screenX, ypos = screenY, xanchor = 'left', yanchor = 'top', xmaximum = 180, ymaximum = 180, yfill = True, xfill = True)
            
            ui.vbox()

            ui.hbox()
            ui.text("X: %d Y: %d Dir: %d" % (self.viewX, self.viewY, self.viewDir))
            ui.close()

            # Initialize display to start at a specific position in relation to the viewers position
            minimapSize = 10
            minimapY = -minimapSize

            while (minimapY <= minimapSize):
                minimapX = -minimapSize
                ui.hbox()

                while (minimapX <= minimapSize):
                    displayViewYOnMinimap = minimapY + self.viewY
                    displayViewXOnMinimap = minimapX + self.viewX

                    if (self.viewX == displayViewXOnMinimap and self.viewY == displayViewYOnMinimap):
                        if (self.viewDir == 8):
                            ui.image("Assets/Graphics/Minimap/MinimapUp.png")
                        elif (self.viewDir == 6):
                            ui.image("Assets/Graphics/Minimap/MinimapRight.png")
                      
                        elif(self.viewDir == 2):
                            ui.image("Assets/Graphics/Minimap/MinimapDown.png")
                      
                        else:
                            ui.image("Assets/Graphics/Minimap/MinimapLeft.png")

                    elif (displayViewYOnMinimap >= 0 and len(self.dungeonMaps[self.viewCurrentMap].mapTilesArray) > displayViewYOnMinimap
                            and displayViewXOnMinimap >= 0 and len(self.dungeonMaps[self.viewCurrentMap].mapTilesArray[displayViewYOnMinimap]) > displayViewXOnMinimap):
                        mapCellToBeDisplayedOnMinimap = self.dungeonMaps[self.viewCurrentMap].mapTilesArray[displayViewYOnMinimap][displayViewXOnMinimap]

                        if (mapCellToBeDisplayedOnMinimap.tileBlocking > 0):
                            ui.image("Assets/Graphics/Minimap/MinimapBlocked.png")
                        else:
                            ui.image("Assets/Graphics/Minimap/MinimapFree.png")
                    else:
                        ui.image("Assets/Graphics/Minimap/MinimapFree.png")

                    minimapX = minimapX + 1

                minimapY = minimapY + 1

                ui.close()

            ui.close()

        # INTERN: Displays the tile located in a specific position on the map on screen (if there is a tile at that position)
        def renderMapPosition(self, renderPosX = 1, renderPosY = 1, renderingDistance = 0, xAdjust = 0, specialEffect = 0, currentBrightness = 100.0):
            if (renderingDistance >= 0 and renderingDistance < len(self.tileSizesAtDistance)):
                if (renderPosY >= 0 and renderPosY < len(self.dungeonMaps[self.viewCurrentMap].mapTilesArray)):
                        if (renderPosX >= 0 and renderPosX < len(self.dungeonMaps[self.viewCurrentMap].mapTilesArray[renderPosY])):
                            brightnessDistance = renderingDistance - 1
                            if (brightnessDistance < 0):
                                brightnessDistance = 0
                            self.DisplayTile(self.dungeonMaps[self.viewCurrentMap].mapTilesArray[renderPosY][renderPosX], renderingDistance, xAdjust, self.dungeonMaps[self.viewCurrentMap].mapTilesArray[renderPosY][renderPosX].tileSpecialEffects, currentBrightness - (7 * brightnessDistance))


        # INTERN: Displays a specific tile scaled in a given way onto a specific position on screen and adds special effects (aka overlays) to it.
        def DisplayTile(self, dungeonMapTile, distance = 0, xAdjust = 0, overlayEffect = 0, currentBrightness = 100.0, transformations = [], transformationsLeftTile = [], transformationsRightTile = [] ):
            # Define variables
            brightness = (currentBrightness + string.atoi(str(dungeonMapTile.tileVisibility))) / 2
            zOrder = ( 2000 - ( distance * 5 ) )

            tileFrontDisplayWidth = self.tileSizesAtDistance[distance].frontTileWidth
            tileFrontDisplayHeight = self.tileSizesAtDistance[distance].frontTileHeight
            tileSideDisplayWidth = self.tileSizesAtDistance[distance].sideTileWidth
            tileSideDisplayHeight = self.tileSizesAtDistance[distance].sideTileHeight

            tileFrontName = self.imageNamePrefixTile + "FrontSidetile" + str(dungeonMapTile.tileNumber).ljust(3, '0')
            internTileFrontName = tileFrontName + str(1000 - xAdjust) + "_" + str(zOrder)

            tileLeftSideName = self.imageNamePrefixTile + "LeftSidetile" + str(dungeonMapTile.tileNumber).ljust(3, '0')
            internTileLeftSideName = tileLeftSideName + str(1000 - xAdjust) + "_" + str(zOrder)
            
            tileRightSideName = self.imageNamePrefixTile + "RightSidetile" + str(dungeonMapTile.tileNumber).ljust(3, '0')
            internTileRightSideName = tileRightSideName + str(1000 - xAdjust) + "_" + str(zOrder)

            tileLeftSideInverseName = self.imageNamePrefixTile + "LeftSideInvertedtile" + str(dungeonMapTile.tileNumber).ljust(3, '0')
            internTileLeftSideInverseName = tileLeftSideInverseName + str(1000 - xAdjust) + "_" + str(zOrder)

            tileRightSideInverseName = self.imageNamePrefixTile + "RightSideInvertedtile" + str(dungeonMapTile.tileNumber).ljust(3, '0')
            internTileRightSideInverseName = tileRightSideInverseName + str(1000 - xAdjust) + "_" + str(zOrder)

            overlayEffectNumber = str(overlayEffect).ljust(3, '0')
            overlayEffectName = self.imageNamePrefixOverlay + 'FrontSideOverlay' + overlayEffectNumber
            internOverlayEffectsName = overlayEffectName + str(1000 - xAdjust) + "_" + str(zOrder)
            overlayEffectWidth = self.tileSizesAtDistance[distance].frontTileWidth + self.tileSizesAtDistance[distance].sideTileWidth
            overlayEffectHeight = self.tileSizesAtDistance[distance].frontTileHeight

            screenCenterX = int(self.screenWidth / 2)
            screenCenterY = int(self.screenHeight / 2)

            brightness = (brightness / 100) - 1.0
            if (brightness < -0.9 ):
                brightness = -0.9

            tileBrightnessMatrix = im.matrix.brightness(brightness)

            # Display tiles themselves
            if (renpy.image_exists(tileFrontName)):
                calcedXPos = 0
                calcedYPos = 0
                calcedXPos = screenCenterX - int(tileFrontDisplayWidth * 0.5)

                if (xAdjust <> 0):
                    calcedXPos = calcedXPos + int(tileFrontDisplayWidth * xAdjust)
                
                calcedYPos = screenCenterY - int(tileFrontDisplayHeight / 2)
                transformationsFrontTile = [
                    Position(xpos=int(calcedXPos),xanchor=0,yanchor=0,ypos=int(calcedYPos)),
                    Transform(size=(tileFrontDisplayWidth, tileFrontDisplayHeight))
                ]   
                transformationsLeftSideTile = [
                    Position(xpos=int(calcedXPos - tileSideDisplayWidth),xanchor=0,yanchor=0,ypos=int(calcedYPos)),
                    Transform(size=(tileSideDisplayWidth, tileSideDisplayHeight))
                ]   
                transformationsRightSideTile = [
                    Position(xpos=int(calcedXPos + tileFrontDisplayWidth),xanchor=0,yanchor=0,ypos=int(calcedYPos)),
                    Transform(size=(tileSideDisplayWidth, tileSideDisplayHeight))
                ]   

                transformationsRightSideTileInverted = [
                    Position(xpos=int(calcedXPos + tileFrontDisplayWidth - tileSideDisplayWidth),xanchor=0,yanchor=0,ypos=int(calcedYPos)),
                    Transform(size=(tileSideDisplayWidth, tileSideDisplayHeight))
                ]   

                transformationsLeftSideTileInverted = [
                    Position(xpos=int(calcedXPos - tileFrontDisplayWidth + tileSideDisplayWidth),xanchor=0,yanchor=0,ypos=int(calcedYPos)),
                    Transform(size=(tileSideDisplayWidth, tileSideDisplayHeight))
                ]   

                # Calculate the at-list
                if (not transformations ):
                    transformations = transformationsFrontTile

                if (not transformationsLeftTile ):
                    transformationsLeftTile = transformationsLeftSideTile

                if (not transformationsRightTile ):
                    transformationsRightTile = transformationsRightSideTile

                # Show the image
                renpy.show(tileFrontName, 
                    at_list = transformations,
                    layer   = 'master',
                    zorder  = zOrder,
                    tag     = internTileFrontName,
                )

                # Display sidetiles only if the image is not directly in front of the viewport
                if (xAdjust <> 0):
                    if (renpy.image_exists(tileLeftSideName)):
                        renpy.show(tileLeftSideName, 
                            at_list = transformationsLeftTile,
                            layer   = 'master',
                            zorder  = zOrder - 1,
                            tag     = internTileLeftSideName,
                        )

                    if (renpy.image_exists(tileRightSideName)):
                        renpy.show(tileRightSideName, 
                            at_list = transformationsRightTile,
                            layer   = 'master',
                            zorder  = zOrder - 1,
                            tag     = internTileRightSideName,
                        )
                else:
                    if (renpy.image_exists(tileRightSideInverseName)):
                        renpy.show(tileRightSideInverseName, 
                            at_list = transformationsRightSideTileInverted,
                            layer   = 'master',
                            zorder  = zOrder - 1,
                            tag     = internTileRightSideInverseName,
                        )

                    if (renpy.image_exists(tileLeftSideInverseName)):
                        renpy.show(tileLeftSideInverseName, 
                            at_list = transformationsLeftSideTileInverted,
                            layer   = 'master',
                            zorder  = zOrder - 1,
                            tag     = internTileLeftSideInverseName,
                        )

            # Display overlays
            if (overlayEffectNumber <> '000'):
                if (renpy.image_exists(overlayEffectName)):
                    # Calculate the at-list
                    if (not transformations ):
                        calcedXPos = 0
                        calcedYPos = 0
                        calcedXPos = screenCenterX - int(tileFrontDisplayWidth * 0.5)

                        if (xAdjust <> 0):
                            calcedXPos = calcedXPos + int(tileFrontDisplayWidth * xAdjust)
                
                        calcedYPos = screenCenterY - int(tileFrontDisplayHeight / 2)
  
                    #Show the image
                    if (overlayEffectNumber == '001'): # Rolling fox - horizontal from right to left
                        overlayZOrder = 1 + zOrder
                        img1 = At(im.Scale(ImageReference(overlayEffectName), overlayEffectWidth, overlayEffectHeight), movingImageTransformation(0, -overlayEffectWidth, 15))
                        img2 = At(im.Scale(ImageReference(overlayEffectName), overlayEffectWidth, overlayEffectHeight), movingImageTransformation(overlayEffectWidth, 0, 15))
                        fxd = Fixed(img1, img2)
                        vp = Viewport(fxd, xysize=(overlayEffectWidth, overlayEffectHeight))
                        renpy.show(internOverlayEffectsName, what=vp, at_list=[Transform(pos=(calcedXPos, calcedYPos))], zorder=overlayZOrder)
 
        # MOVEMENT: Turn view left
        def MoveTurnLeft(self):
            self.viewDir = self.CalculateTurnLeft(self.viewDir)

        # MOVEMENT: Turn view right
        def MoveTurnRight(self):
            self.viewDir = self.CalculateTurnRight(self.viewDir)

        # MOVEMENT: Move 1 field forward (only if not blocked by the current type of movement)
        def MoveForward(self):
            newPosArray = self.CalculateMoveForward(self.viewX, self.viewY, self.viewDir)

            if (not self.CalcualteIsTileBlocked(newPosArray[0], newPosArray[1])):
                self.viewLastX = self.viewX
                self.viewLastY = self.viewY
                self.viewX = newPosArray[0]
                self.viewY = newPosArray[1]
                if (self.fireEventOnEnterCell): 
                    if (self.viewY >= 0 and self.viewY < len(self.dungeonMaps[self.viewCurrentMap].mapTilesArray)):
                            if (self.viewX >= 0 and self.viewX < len(self.dungeonMaps[self.viewCurrentMap].mapTilesArray[self.viewY])):                
                                if (self.dungeonMaps[self.viewCurrentMap].mapTilesArray[self.viewY][self.viewX].tileEventNumber <> '000' and self.fireEventOnEnterCell):
                                    if (renpy.has_label("Event" + self.dungeonMaps[self.viewCurrentMap].mapTilesArray[self.viewY][self.viewX].tileEventNumber)):
                                        renpy.call("Event" + self.dungeonMaps[self.viewCurrentMap].mapTilesArray[self.viewY][self.viewX].tileEventNumber)
            else:
                renpy.with_statement(Shake((0, 0, 0, 0), 0.5, dist=30))

                                

        # MOVEMENT: Move 1 field backwards (only if not blocked by the current type of movement)
        def MoveBackward(self):
            newPosArray = self.CalculateMoveBackward(self.viewX, self.viewY, self.viewDir)

            if (not self.CalcualteIsTileBlocked(newPosArray[0], newPosArray[1])):
                self.viewLastX = self.viewX
                self.viewLastY = self.viewY
                self.viewX = newPosArray[0]
                self.viewY = newPosArray[1]
                
                if (self.fireEventOnEnterCell): 
                    if (self.viewY >= 0 and self.viewY < len(self.dungeonMaps[self.viewCurrentMap].mapTilesArray)):
                            if (self.viewX >= 0 and self.viewX < len(self.dungeonMaps[self.viewCurrentMap].mapTilesArray[self.viewY])):                
                                if (self.dungeonMaps[self.viewCurrentMap].mapTilesArray[self.viewY][self.viewX].tileEventNumber <> '000' and self.fireEventOnEnterCell):
                                    if (renpy.has_label("Event" + self.dungeonMaps[self.viewCurrentMap].mapTilesArray[self.viewY][self.viewX].tileEventNumber)):
                                        renpy.call("Event" + self.dungeonMaps[self.viewCurrentMap].mapTilesArray[self.viewY][self.viewX].tileEventNumber)            
                else:
                    renpy.with_statement(Shake((0, 0, 0, 0), 0.5, dist=30))
       
        # INTERNAL: Checks if tile is blocked by type of movement
        def CalcualteIsTileBlocked(self, checkX, checkY):
            if (checkY >= 0 and checkY < len(self.dungeonMaps[self.viewCurrentMap].mapTilesArray)):
                    if (checkX >= 0 and checkX < len(self.dungeonMaps[self.viewCurrentMap].mapTilesArray[checkY])):
                        if ((self.dungeonMaps[self.viewCurrentMap].mapTilesArray[checkY][checkX].tileBlocking == 1 and self.viewMovementType == 1) 
                            or self.dungeonMaps[self.viewCurrentMap].mapTilesArray[checkY][checkX].tileBlocking > 1):
                            return True
            return False

        # INTERNAL: Calculates the new facing if turning left from the original facing
        def CalculateTurnLeft(self, originalFacing):
            if (originalFacing == 8):
                return 4
            elif (originalFacing == 4):
                return 2
            elif (originalFacing == 2):
                return 6
            else:
                return 8

        # INTERNAL: Calculates the new facing if turning right from the original facing
        def CalculateTurnRight(self, originalFacing):
            if (originalFacing == 8):
                return 6
            elif (originalFacing == 6):
                return 2
            elif (originalFacing == 2):
                return 4
            else:
                return 8

        # INTERNAL: Calculates the x and y position if going forward 1 step from a given original x and y
        def CalculateMoveForward(self, originalX, originalY, facing):
            newX = originalX
            newY = originalY

            if (facing == 8):
                newY = newY - 1
            elif (facing == 4):
                newX = newX - 1
            elif (facing == 2):
                newY = newY + 1
            else:
                newX = newX + 1

            if (newX < 0):
                newX = 0
            elif (newX > self.maxMapX - 1):
                newX = self.maxMapX - 1

            if (newY < 0):
                newY = 0
            elif (newY > self.maxMapY - 1):
                newY = self.maxMapY - 1

            return newX, newY

        # INTERNAL: Calculates the x and y position if going backwards 1 step from a given original x and y
        def CalculateMoveBackward(self, originalX, originalY, facing):
            return self.CalculateMoveForward(originalX, originalY, self.CalculateTurnRight(self.CalculateTurnRight(facing)))

init -49 python:
    dungeonCrawl3DEngine = ClsDungeonCrawl3DEngine()

    # Loads all tiles and creates properly scaled images out of them out of a predefined folder
    dungeonCrawl3DEngine.loadedDungeonTiles = []

    renpy.image("CrawlerGeneralBackground","Assets/Graphics/CrawlBackgrounds/background.png")

    fileList = renpy.list_files()
    for fileNameWithPath in fileList:
        fileName  = (fileNameWithPath.split("/"))[fileNameWithPath.count("/")]
        imageName = (fileNameWithPath.split("/"))[fileNameWithPath.count("/")][:-4]
        tileSize = dungeonCrawl3DEngine.tileSizesAtDistance[0]

        if (fileNameWithPath[:24] == "Assets/Graphics/Overlays"):
            tileDisplayImageName = imageName
            if (imageName[-4:] == 'side'):
                tileDisplayImageName = tileDisplayImageName[:-4]
                renpy.image(
                    dungeonCrawl3DEngine.imageNamePrefixOverlay + "RightSide" + tileDisplayImageName,
                    im.Scale(
                        fileNameWithPath,
                        tileSize.sideTileWidth,
                        tileSize.sideTileHeight,
                    )
                )

                renpy.image(
                    dungeonCrawl3DEngine.imageNamePrefixOverlay + "LeftSide" + tileDisplayImageName,
                    im.Flip(
                        im.Scale(
                            fileNameWithPath,
                            tileSize.sideTileWidth,
                            tileSize.sideTileHeight,
                        ),
                        horizontal = True
                    )
                )
            else:
                renpy.image(
                    dungeonCrawl3DEngine.imageNamePrefixOverlay + "FrontSide" + tileDisplayImageName,
                    im.Scale(
                        fileNameWithPath,
                        tileSize.frontTileWidth,
                        tileSize.frontTileHeight,
                    )
                )

            distance = 0
            for tileSize in dungeonCrawl3DEngine.tileSizesAtDistance:
                tileDisplayImageName = "OverlayDistance" + str(distance) + "TileName" + imageName

                if (imageName[-4:] == 'side'):
                    tileDisplayImageName = tileDisplayImageName[:-4]
                    renpy.image(
                        "OverlayRightSide" + tileDisplayImageName,
                        im.Scale(
                            fileNameWithPath,
                            tileSize.sideTileWidth,
                            tileSize.sideTileHeight,
                        )
                    )

                    renpy.image(
                        "OverlayLeftSide" + tileDisplayImageName,
                        im.Flip(
                            im.Scale(
                                fileNameWithPath,
                                tileSize.sideTileWidth,
                                tileSize.sideTileHeight,
                            ),
                            horizontal = True
                        )
                    )
                else:
                    renpy.image(
                        "OverlayFrontSide" + tileDisplayImageName,
                        im.Scale(
                            fileNameWithPath,
                            tileSize.frontTileWidth,
                            tileSize.frontTileHeight,
                        )
                    )

                distance = distance + 1

        if (fileNameWithPath[:32] == "Assets/Graphics/CrawlBackgrounds"):
            distance = 0
            for tileSize in dungeonCrawl3DEngine.tileSizesAtDistance:
                tileDisplayImageName = "BGDistance" + str(distance) + "TileName" + imageName

                if (imageName[-4:] == 'side'):
                    tileDisplayImageName = tileDisplayImageName[:-4]
                    renpy.image(
                        "BGRightSide" + tileDisplayImageName,
                        im.Scale(
                            fileNameWithPath,
                            tileSize.sideTileWidth,
                            tileSize.sideTileHeight,
                        )
                    )

                    renpy.image(
                        "BGLeftSide" + tileDisplayImageName,
                        im.Flip(
                            im.Scale(
                                fileNameWithPath,
                                tileSize.sideTileWidth,
                                tileSize.sideTileHeight,
                            ),
                            horizontal = True
                        )
                    )
                else:
                    renpy.image(
                        "BGFrontSide" + tileDisplayImageName,
                        im.Scale(
                            fileNameWithPath,
                            tileSize.frontTileWidth,
                            tileSize.frontTileHeight,
                        )
                    )

                distance = distance + 1
                
        if (fileNameWithPath[:21] == "Assets/Graphics/Tiles"):            
            tileDisplayImageName = imageName

            if (imageName[-4:] == 'side'):
                tileDisplayImageName = tileDisplayImageName[:-4]
                renpy.image(
                    dungeonCrawl3DEngine.imageNamePrefixTile + "RightSide" + tileDisplayImageName,
                    im.Scale(
                        fileNameWithPath,
                        tileSize.sideTileWidth,
                        tileSize.sideTileHeight,
                    )
                )

                renpy.image(
                    dungeonCrawl3DEngine.imageNamePrefixTile + "RightSideInverted" + tileDisplayImageName,
                    im.Flip(ImageReference(dungeonCrawl3DEngine.imageNamePrefixTile + "RightSide" + tileDisplayImageName), horizontal=True, xanchor=0,yanchor=0)
               )

                renpy.image(
                    dungeonCrawl3DEngine.imageNamePrefixTile + "LeftSide" + tileDisplayImageName,
                    im.Flip(
                        im.Scale(
                            fileNameWithPath,
                            tileSize.sideTileWidth,
                            tileSize.sideTileHeight,
                        ),
                        horizontal = True
                    )
                )

                renpy.image(
                    dungeonCrawl3DEngine.imageNamePrefixTile + "LeftSideInverted" + tileDisplayImageName,
                    im.Flip(ImageReference(dungeonCrawl3DEngine.imageNamePrefixTile + "LeftSide" + tileDisplayImageName), horizontal=True, xanchor=0,yanchor=0)
               )
            else:
                renpy.image(
                    dungeonCrawl3DEngine.imageNamePrefixTile + "FrontSide" + tileDisplayImageName,
                    im.Scale(
                        fileNameWithPath,
                        tileSize.frontTileWidth,
                        tileSize.frontTileHeight,
                    )
                )
                       
            dungeonCrawl3DEngine.loadedDungeonTiles.append(tileDisplayImageName)

            distance = 0
            for tileSize in dungeonCrawl3DEngine.tileSizesAtDistance:
                tileDisplayImageName = "TileDistance" + str(distance) + "TileName" + imageName

                if (imageName[-4:] == 'side'):
                    tileDisplayImageName = tileDisplayImageName[:-4]
                    renpy.image(
                        "tileRightSide" + tileDisplayImageName,
                        im.Scale(
                            fileNameWithPath,
                            tileSize.sideTileWidth,
                            tileSize.sideTileHeight,
                        )
                    )

                    renpy.image(
                        "tileLeftSide" + tileDisplayImageName,
                        im.Flip(
                            im.Scale(
                                fileNameWithPath,
                                tileSize.sideTileWidth,
                                tileSize.sideTileHeight,
                            ),
                            horizontal = True
                        )
                    )
                else:
                    renpy.image(
                        "tileFrontSide" + tileDisplayImageName,
                        im.Scale(
                            fileNameWithPath,
                            tileSize.frontTileWidth,
                            tileSize.frontTileHeight,
                        )
                    )
                       
                dungeonCrawl3DEngine.loadedDungeonTiles.append(tileDisplayImageName)
                distance = distance + 1
