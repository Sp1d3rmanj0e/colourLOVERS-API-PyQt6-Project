from colourlovers.clapi import ColourLovers

import random

import json

from imageGrabber import imageDownloader

from design import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QColorDialog
from PyQt6 import QtCore, QtGui

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Check if choose color button pressed
        self.pushButton_chooseColor.clicked.connect(self.chooseColor)

        # Check if random color button pressed
        self.pushButton_randomColor.clicked.connect(self.randomColor)
    
    # Opens color picker terminal
    def chooseColor(self):
        dialog = QColorDialog()

        clickedOk = dialog.exec()

        if clickedOk:
            # Get the color chosen from the dialog
            color = dialog.currentColor().name()

            # Set label color to the dialog's chosen color
            self.setNewColor(color)
        else:
            print("Dialog cancelled")

    # Generates and returns a random hex color (String)
    def getRandomHexColor(self):
        red   = random.randint(0, 255)
        green = random.randint(0, 255)
        blue  = random.randint(0, 255)
        hex = '#%02x%02x%02x' % (red, blue, green) # CREDIT TO: Dietrich Epp --> https://stackoverflow.com/questions/3380726/converting-an-rgb-color-tuple-to-a-hexidecimal-string
        return hex

    # Generates and updates the current color image and text
    def randomColor(self):
        hex = self.getRandomHexColor()
        self.setNewColor(hex)

    # Changes the seed color title (done)
    # Changes the seed color image (done)
    # Changes the palette collection (not done)
    def setNewColor(self, hex):
        self.label_colorHex.setText(hex)
        #self.updateSeedColorSprite(hex)
        self.updatePaletteCollection(hex)

    # Given a hex code, retrieve the sprite version of that hex
    # And change the image displayed on the PyQt6 Window
    def updateSeedColorSprite(self, hex):
        
        print(hex)

        # Retrieve color data from the color
        colorData = self.getColorData(hex)

        print("Color data")
        print(colorData)

        # Confirm the search worked
        if colorData:

            # Get the image link from the color data
            imageLink = colorData["imageUrl"]

            print(imageLink)

            imageDownloader.downloadImageUrl('seedColorDemoImage.png', imageLink)

            self.label_imageSeedColor.setPixmap(QtGui.QPixmap("seedColorDemoImage.png"))

        else:
            print("Color not valid")
            return False

    # Remove the # from the hex code if needed
    def trimHex(self, hex):

        if (len(hex) == 7):
            trimmedHex = hex[1:]

        return trimmedHex

    # Hex can have or not have #
    # Will return false if API failed
    def getColorData(self, hex):
        
        # Remove # If needed
        hex = self.trimHex(hex)

        # Call API to get color data
        cl = ColourLovers()
        newColor = cl.search_color(True, hexvalue = hex, format = 'json')
        del cl

        return self.parseData(newColor)[0]

    def getPaletteData(self, searchHex):

        # Remove # If needed
        searchHex = self.trimHex(searchHex)

        # Get the top 15 palettes for this color
        cl = ColourLovers()
        paletteArr = cl.search_palettes(request='top', hex = searchHex, numResults=15)
        print(paletteArr)
        del cl

        return paletteArr

    # Parses json data
    # Returns parsed data if all went well
    # Returns false if data does not exist or was empty
    def parseData(self, data):
        # Parse the json data
        parsedData = json.loads(data)

        # Confirm not an empty array
        if (len(parsedData) == 0):
            return False

        # Return data
        return parsedData

    def confirmColorExists(self, hex):
        pass

    # Given a hex code, returns an array containing palette objects
    # Each object contains various values.  The accessors we will use are:
    # .id          - the unique palette id
    # .image_url   - the url to the palette image
    # .colors      - an array containing all 5 hex colors for the palette
    # .title       - the name of the palette
    # Returns the compiled array
    def updatePaletteCollection(self, hex):
        
        paletteData = self.getPaletteData(hex)

        print(paletteData)
        print(">>>>")
        self.openPalette(paletteData, 0)

    def openPalette(self, paletteData, paletteNum = 0):
        
        # Get the palette object to extract
        paletteObj = paletteData[paletteNum]

        paletteId = paletteObj.id
        paletteImgUrl = paletteObj.image_url
        paletteColors = paletteObj.colors
        paletteName = paletteObj.title

        print("id", paletteId)
        print("url", paletteImgUrl)
        print("colors", paletteColors)
        print("name", paletteName)

        self.updatePaletteHexLabels(paletteColors)
        self.updatePaletteName(paletteName)
        self.updatePaletteImage(paletteImgUrl)

    def updatePaletteHexLabels(self, paletteColors):
        self.label_firstPaletteHex.setText(paletteColors[0])
        self.label_secondPaletteHex.setText(paletteColors[1])
        self.label_thirdPaletteHex.setText(paletteColors[2])
        self.label_fourthPaletteHex.setText(paletteColors[3])
        self.label_fifthPaletteHex.setText(paletteColors[4])

    def updatePaletteName(self, paletteName):
        self.label_paletteName.setText(paletteName)

    def updatePaletteImage(self, imgUrl):

        #imageDownloader.downloadImageUrl('generedPaletteDemoImage.png', imgUrl)

        #self.label_imageSeedColor.setPixmap(QtGui.QPixmap("generedPaletteDemoImage.png"))
        pass

def main():

    app = QApplication([])
    window = Window()

    window.show()
    app.exec()

if __name__ == '__main__':
    main()
