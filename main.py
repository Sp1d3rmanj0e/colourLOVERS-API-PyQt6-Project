from colourlovers.clapi import ColourLovers

import random

import json

import sys
import os
import shutil
from pathlib import Path

from imageGrabber import imageDownloader
from paletteLoader import paletteOpener as PO

from design import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QColorDialog, QFileDialog
from PyQt6 import QtCore, QtGui 
from PyQt6.QtCore import QStandardPaths

class Window(QMainWindow, Ui_MainWindow):

    paletteDataArr = []
    paletteNum = 0
    currentPaletteId = -1
    currentPaletteName = ""
    currentPaletteImgUrl = ""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Check if choose color button pressed
        self.pushButton_chooseColor.clicked.connect(self.chooseColor)

        # Check if random color button pressed
        self.pushButton_randomColor.clicked.connect(self.randomColor)

        # Check if next palette button is pressed
        self.pushButton_nextPalette.clicked.connect(self.switchNextPalette)

        # Check if download button is pressed
        self.pushButton_downloadRandomPalette.clicked.connect(self.downloadFile)

        # Check if favorite/unfavorite button is pressed
        self.pushButton_favoriteRandomPalette.clicked.connect(self.favoriteRandomPalette)
    
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
        
        self.paletteDataArr = self.getPaletteData(hex)
        self.paletteNum = 0

        self.openPalette(self.paletteNum)

    def openPalette(self, paletteNum = 0):
        
        # Get the palette object to extract
        paletteObj = self.paletteDataArr[paletteNum]

        print("Palette object", paletteObj)

        paletteId = paletteObj.id
        paletteImgUrl = paletteObj.image_url
        paletteColors = paletteObj.colors
        paletteName = paletteObj.title

        print("id", paletteId)
        print("url", paletteImgUrl)
        print("colors", paletteColors)
        print("name", paletteName)
        
        # Store these variables now so we don't have to
        # Call the API again to get the infomation
        self.currentPaletteId = paletteId
        self.currentPaletteName = paletteName
        self.currentPaletteImgUrl = paletteImgUrl

        self.updatePaletteHexLabels(paletteColors)
        self.updatePaletteName(paletteName)
        self.updatePaletteImage(paletteImgUrl)

    def updatePaletteHexLabels(self, paletteColors):

        paletteLen = len(paletteColors)
        
        # Show labels as necessary
        # (Some palettes have less than 5 colors)
        if (paletteLen == 5):
            self.label_firstPaletteHex.setText(paletteColors[0])
            self.label_secondPaletteHex.setText(paletteColors[1])
            self.label_thirdPaletteHex.setText(paletteColors[2])
            self.label_fourthPaletteHex.setText(paletteColors[3])
            self.label_fifthPaletteHex.setText(paletteColors[4])
        elif (paletteLen == 4):
            self.label_firstPaletteHex.setText(paletteColors[0])
            self.label_secondPaletteHex.setText(paletteColors[1])
            self.label_thirdPaletteHex.setText("")
            self.label_fourthPaletteHex.setText(paletteColors[2])
            self.label_fifthPaletteHex.setText(paletteColors[3])
        elif (paletteLen == 3):
            self.label_firstPaletteHex.setText(paletteColors[0])
            self.label_secondPaletteHex.setText("")
            self.label_thirdPaletteHex.setText(paletteColors[1])
            self.label_fourthPaletteHex.setText("")
            self.label_fifthPaletteHex.setText(paletteColors[2])
        elif (paletteLen == 2):
            self.label_firstPaletteHex.setText("")
            self.label_secondPaletteHex.setText(paletteColors[0])
            self.label_thirdPaletteHex.setText("")
            self.label_fourthPaletteHex.setText(paletteColors[1])
            self.label_fifthPaletteHex.setText("")
        elif (paletteLen == 1):
            self.label_firstPaletteHex.setText("")
            self.label_secondPaletteHex.setText("")
            self.label_thirdPaletteHex.setText(paletteColors[0])
            self.label_fourthPaletteHex.setText("")
            self.label_fifthPaletteHex.setText("")
        else:
            self.label_firstPaletteHex.setText("Error")
            self.label_secondPaletteHex.setText("Palette")
            self.label_thirdPaletteHex.setText("Not")
            self.label_fourthPaletteHex.setText("Found")
            self.label_fifthPaletteHex.setText("Error")

    def updatePaletteName(self, paletteName):
        self.label_paletteName.setText(paletteName)

    def updatePaletteImage(self, imgUrl):

        imageDownloader.downloadImageUrl('generedPaletteDemoImage.png', imgUrl)
        self.label_imageRandomPalette.setPixmap(QtGui.QPixmap("generedPaletteDemoImage.png"))

    def switchNextPalette(self):

        # Get the length of the palette arr
        paletteLength = len(self.paletteDataArr)

        print("Palette length", paletteLength)

        # Increment the palette number by 1 or loop back to 0 if reached the max
        self.paletteNum = (self.paletteNum+1) % paletteLength

        print("Palette num", self.paletteNum)

        self.openPalette(self.paletteNum)

    # THANKS TO https://www.freecodecamp.org/news/python-copy-file-copying-files-to-another-directory/#:~:text=To%20copy%20the%20contents%20of%20a%20file%20object%20to%20another,and%20a%20destination%20file%20object.
    # THANKS TO https://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac
    # THANKS TO https://www.youtube.com/watch?v=XgK8ZRvcE5E
    # FOR HELP
    def downloadFile(self):
        
        # Get the name of the palette
        paletteName = self.label_paletteName.text()

        file_dialog = QFileDialog()

        # Designate viable files to select
        file_filter = "Image file (*.png)"

        # Generate a random file name for the file
        file_name = paletteName + " " + str(random.randrange(0, 9999999999, 1)) + ".png"

        # Get open file name
        response = file_dialog.getSaveFileName(
            parent=self,
            caption='Select a folder',
            directory=file_name,
            filter=file_filter
        )

        # If nothing is returned, cancel extraction
        if (response[0] == ''):
            print("Download cancelled")
            return

        # Get the original image
        source_file = open('generedPaletteDemoImage.png', 'rb')

        # Get the target file location
        save_path = open(response[0], 'wb')

        # Copy the original file to the new location
        shutil.copyfileobj(source_file, save_path)

        #print(response)

    def favoriteRandomPalette(self):

        paletteExists = PO.getIfPaletteIdExists(self, self.currentPaletteId)

        # If not previously favorited, favorite it now
        if (not(paletteExists)):
            PO.addPalette(self, self.currentPaletteId, self.currentPaletteName, self.currentPaletteImgUrl)
            print("Favorited palette!")
        
        # Otherwise, unfavorite it instead
        else:
            PO.removePalette(self, self.currentPaletteId)
            print("Unfavorited palette!")


        

def main():

    app = QApplication([])
    window = Window()

    window.show()
    app.exec()

if __name__ == '__main__':
    main()
