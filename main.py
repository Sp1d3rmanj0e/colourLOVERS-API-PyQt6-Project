from colourlovers.clapi import ColourLovers

import random

import json

import math

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

    palettesPerPage = 5
    numFavoritePalettes = 0
    numFavoritePalettePages = 1
    currentFavoritePalettePage = 1

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Update variables

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

        # Check if tab changed to favorite palettes
        self.tabWidget.tabBarClicked.connect(self.updateTab)

        # Check if next page for favorite palettes is pressed
        self.pushButton_nextPage.clicked.connect(self.favoritePalettesNextPage)

        # Check if previous page for favorite palettes is pressed
        self.pushButton_previousPage.clicked.connect(self.favoritePalettesPrevPage)

    # Opens color picker terminal
    def chooseColor(self):
        ''' 
        Opens a color dialog that allows the player to pick a color of their choice 
        Then calls setNewColor to call all corresponding functions
        '''

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
    def getRandomHexColor(self) -> str:
        ''' 
        Generates a random hex color 

        Returns:
            String: A 6 digit hex code with a '#' appended at the start

        '''
        red   = random.randint(0, 255)
        green = random.randint(0, 255)
        blue  = random.randint(0, 255)
        hex = '#%02x%02x%02x' % (red, blue, green) # CREDIT TO: Dietrich Epp --> https://stackoverflow.com/questions/3380726/converting-an-rgb-color-tuple-to-a-hexidecimal-string
        return hex

    # Generates and updates the current color image and text
    def randomColor(self):
        '''
        Generates a random color and activates the
        setNewColor() function to activate all following functions
        '''
        hex = self.getRandomHexColor()
        self.setNewColor(hex)

    # Changes the seed color title (done)
    # Changes the seed color image (done)
    # Changes the palette collection (not done)
    def setNewColor(self, hex : str):
        '''
        Changes title, image, and palette collection corresponding
        With the current hex color

        Args:
            hex (string): The hex code of the new color
        '''
        self.label_colorHex.setText(hex)
        #self.updateSeedColorSprite(hex)
        self.updatePaletteCollection(hex)

    # Given a hex code, retrieve the sprite version of that hex
    # And change the image displayed on the PyQt6 Window
    def updateSeedColorSprite(self, hex : str):
        '''
        Given a hex, call the colourLOVERS api to get and download
        the color image.  It then sets that image to the seedColor 
        image label

        Args:
            hex (String): The color to get an image of
        '''

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
    def trimHex(self, hex : str) -> str:
        '''
        Removes the '#' from a hex String if it needs one

        Args:
            hex (String): The string hex (Only works if 7 chars long)

        Returns:
            String: The 6 digit hex (w/o the '#')
        '''
        if (len(hex) == 7):
            trimmedHex = hex[1:]

        return trimmedHex

    # Hex can have or not have #
    # Will return false if API failed
    def getColorData(self, hex : str): # TODO - when able to, add "-> dict:" (needs confirmation of data type)
        '''
        Get the API color data from a given hex.
        This color data includes:
            id
            imageUrl
            and others

        Args:
            hex (String): A hex code to get the color data from

        Returns:
            dict (see api for all values): Contains data about the 
                                           given color
        '''
        # Remove # If needed
        hex = self.trimHex(hex)

        # Call API to get color data
        cl = ColourLovers()
        newColor = cl.search_color(True, hexvalue = hex, format = 'json')
        del cl

        return self.parseData(newColor)[0]

    def getPaletteData(self, searchHex : str): # TODO: Find return data type
        '''
        Gets an array containing several palettes with a set seed color

        Args:
            searchHex (String): The seed color that the palette must contain

        Returns:
            array[object]: Contains several palette objects with variables like:
                           id
                           image_url
                           colors
                           title
        '''
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
    def parseData(self, data : json): # TODO: Find return data type
        '''
        Given data, load the json data

        Args:
            data (Json): The json-encoded data

        Returns:
            loaded Json: The json-deencoded data
        '''
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
    def updatePaletteCollection(self, hex : str):
        '''
        Given a hex, generate a new palette collection and
        Update the current randomized palette

        Args:
            hex (String): The seed hex to generate the palettes from
        '''
        
        self.paletteDataArr = self.getPaletteData(hex)
        self.paletteNum = 0

        self.openPalette(self.paletteNum)

    def openPalette(self, paletteNum : int = 0):
        '''
        Extracts data from a palette object and modified QT objects
        To reflect the palette data
        This includes the palette image and respective hex colors

        Args:
            paletteNum (int): Which palette obj in the paletteArr to use
        '''

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

    def updatePaletteHexLabels(self, paletteColors): # TODO: find data type for string arrays
        '''
        Updates the 5 labels in the bottom of the main QT winow
        To display the current palette's hex colors

        Args:
            paletteColors (0 < array[Strings] <= 5): An array containing 
                                                     hexcolors of the current
                                                     palette
        '''
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

    def updatePaletteName(self, paletteName : str):
        '''
        Updates the palette name given a palette name

        Args:
            paletteName (String): The name of the current palette
        '''
        self.label_paletteName.setText(paletteName)

    def updatePaletteImage(self, imgUrl : str):
        '''
        Downloads and updates the palette image given an image url

        Args:
            imgUrl (String): The url of the image to download and show
        '''

        imageDownloader.downloadImageUrl('generedPaletteDemoImage.png', imgUrl)
        self.label_imageRandomPalette.setPixmap(QtGui.QPixmap("generedPaletteDemoImage.png"))

    def switchNextPalette(self):
        '''
        Switches to the next generated palette
        If reached the last page, loop back to the start
        Then open the palette on that page 
        '''
        
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
        '''
        Downloads the current randomized palette using QFileDialog
        to determine a spot to place the file
        '''
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

    
    def updateFavoritePalettePageVars(self):
        '''
        Calculates the new number of pages to store favorite palettes
        '''
        self.numFavoritePalettes = PO.getNumFavoritedPalettes(self)
        print("Current number of favorited palettes", self.numFavoritePalettes)
        self.numFavoritePalettePages = max(math.ceil(self.numFavoritePalettes/self.palettesPerPage), 1)

    def favoriteRandomPalette(self):
        '''
        Favorites the current randomized palette
        And adds it to a csv file for later retrieval
        '''
        paletteExists = PO.getIfPaletteIdExists(self, self.currentPaletteId)

        # If not previously favorited, favorite it now
        if (not(paletteExists)):
            PO.addPalette(self, self.currentPaletteId, self.currentPaletteName, self.currentPaletteImgUrl)
            print("Favorited palette!")
        
        # Otherwise, unfavorite it instead
        else:
            PO.removePalette(self, self.currentPaletteId)
            print("Unfavorited palette!")

        # Update page variables
        self.updateFavoritePalettePageVars()

    def showFavoritedPalettes(self, page : int = 1):
        '''
        Updates the 5 image labels and 5 name labels of favorite palettes
        Within the favorite palettes view

        The palettes shown is determined by the favorite palette page

        Args:
            page (int): The favorite palette page to show
                        NOTE: [page 1] represents [page 0]!
        '''

        # Make page base 0, not base 1
        page-=1

        # Calculate which group of 5 palettes to get
        paletteGroupMin = self.palettesPerPage * page                # Ex. Page = 0; 5 * 0 = 0
        paletteGroupMax = paletteGroupMin + self.palettesPerPage - 1 # Ex. Page = 2; (5*2 = 10) - 1 = 9

        # Get that palette section
        paletteSelectionArr = PO.getPaletteSection(self, paletteGroupMin, paletteGroupMax)

        print(paletteSelectionArr)

        self.clearFavoritePaletteSlots()

        # Draw as many palettes as there are available on this page
        for i in range(len(paletteSelectionArr)):

            palette = paletteSelectionArr[i]

            p_name = palette[1]
            p_imgUrl = palette[2]

            self.drawFavoritePaletteSlot(p_name, p_imgUrl, i)

    def clearFavoritePaletteSlots(self):
        '''
        Clears all the palettes in the favorite palette page slots
        '''
        # Reset image
        self.label_imagePaletteSlot1.setPixmap(QtGui.QPixmap("emptyPalette.png"))
            
        # Reset name
        self.label_paletteNameSlot1.setText("\"\"")

        # Reset image
        self.label_imagePaletteSlot2.setPixmap(QtGui.QPixmap("emptyPalette.png"))
            
        # Reset name
        self.label_paletteNameSlot2.setText("\"\"")

        # Reset image
        self.label_imagePaletteSlot3.setPixmap(QtGui.QPixmap("emptyPalette.png"))
            
        # Reset name
        self.label_paletteNameSlot3.setText("\"\"")

        # Reset image
        self.label_imagePaletteSlot4.setPixmap(QtGui.QPixmap("emptyPalette.png"))
            
        # Reset name
        self.label_paletteNameSlot4.setText("\"\"")

        # Reset image
        self.label_imagePaletteSlot5.setPixmap(QtGui.QPixmap("emptyPalette.png"))
            
        # Reset name
        self.label_paletteNameSlot5.setText("\"\"")

    def drawFavoritePaletteSlot(self, name : str, imgUrl : str, spot : int):
        '''
        Fills a favorite palette slot with an image and name

        Args:
            name (String): The name of the palette
            imgUrl (String): A link to the palette image
            spot (0 <= int < 5): The spot to put the palette info
        '''
        if spot == 0:
            
            # Set image
            imageDownloader.downloadImageUrl('favoritePaletteSlot1.png', imgUrl)
            self.label_imagePaletteSlot1.setPixmap(QtGui.QPixmap("favoritePaletteSlot1.png"))
            
            # Set name
            self.label_paletteNameSlot1.setText(name)

        elif spot == 1:

            # Set image
            imageDownloader.downloadImageUrl('favoritePaletteSlot2.png', imgUrl)
            self.label_imagePaletteSlot2.setPixmap(QtGui.QPixmap("favoritePaletteSlot2.png"))
            
            # Set name
            self.label_paletteNameSlot2.setText(name)

        elif spot == 2:

            # Set image
            imageDownloader.downloadImageUrl('favoritePaletteSlot3.png', imgUrl)
            self.label_imagePaletteSlot3.setPixmap(QtGui.QPixmap("favoritePaletteSlot3.png"))
            
            # Set name
            self.label_paletteNameSlot3.setText(name)

        elif spot == 3:

            # Set image
            imageDownloader.downloadImageUrl('favoritePaletteSlot4.png', imgUrl)
            self.label_imagePaletteSlot4.setPixmap(QtGui.QPixmap("favoritePaletteSlot4.png"))
            
            # Set name
            self.label_paletteNameSlot4.setText(name)

        elif spot == 4:

            # Set image
            imageDownloader.downloadImageUrl('favoritePaletteSlot5.png', imgUrl)
            self.label_imagePaletteSlot5.setPixmap(QtGui.QPixmap("favoritePaletteSlot5.png"))
            
            # Set name
            self.label_paletteNameSlot5.setText(name)

        else:
            print("Error, spot not found")

    def favoritePalettesNextPage(self):
        '''
        Turns the page to the right by one to show other palettes
        Will not move past the last page
        '''
        if self.currentFavoritePalettePage < self.numFavoritePalettePages:
            self.currentFavoritePalettePage += 1
            self.showFavoritedPalettes(self.currentFavoritePalettePage)

    def favoritePalettesPrevPage(self):
        '''
        Turns the page to the left by one to show previous palette pages
        Will not move behind the first page
        '''
        if self.currentFavoritePalettePage > 1:
            self.currentFavoritePalettePage -= 1
            self.showFavoritedPalettes(self.currentFavoritePalettePage)

    def updateTab(self):

        # Tab 0 = Favorite palettes view
        # Tab 1 = Main view
        curTab = self.tabWidget.currentIndex()

        if curTab == 0:
            self.showFavoritedPalettes(self.currentFavoritePalettePage)

def main():

    app = QApplication([])
    window = Window()

    window.show()
    app.exec()

if __name__ == '__main__':
    main()
