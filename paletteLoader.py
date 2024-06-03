
import csv
import pandas as pd

# THANKS TO https://youtube.com/watch?v=q5uM4VKywbA
class paletteOpener():
    
    def getPalette(self, paletteNum):
        with open('favoritePalettes.csv', 'r') as csv_file:

            # Open the file reader
            csv_reader = csv.reader(csv_file)

            next(csv_reader)

            rows = list(csv_reader)

            paletteData = rows[paletteNum]

            # Close the file
            csv_file.close

        return paletteData

    def getPaletteSection(self, paletteStart, paletteEnd):
        with open('favoritePalettes.csv', 'r') as csv_file:

            # Open the file reader
            csv_reader = csv.reader(csv_file)

            next(csv_reader)

            rows = list(csv_reader)

            paletteData = rows[paletteStart:paletteEnd+1]

            # Close the file
            csv_file.close

        return paletteData
    
    # CREDIT TO https://www.tutorialspoint.com/how-to-delete-only-one-row-in-csv-with-python
    def removePalette(self, paletteId):

        df = pd.read_csv('favoritePalettes.csv', index_col='id')
        df = df.drop(paletteId)
        df.to_csv('favoritePalettes.csv', index=True)

    # THANKS TO https://www.geeksforgeeks.org/how-to-append-a-new-row-to-an-existing-csv-file/
    def addPalette(self, paletteId, paletteName, paletteImgUrl):

        # THANKS TO https://stackoverflow.com/questions/16864683/empty-space-in-between-rows-after-using-writer-in-python
        # For newline assistance

        # Open the file in append mode
        with open('favoritePalettes.csv', 'a', newline="") as csv_file:

            # Create writer object
            csv_writer = csv.writer(csv_file)

            # Add row to the end
            csv_writer.writerow([paletteId, paletteName, paletteImgUrl])

            csv_file.close()
    
    def getIfPaletteIdExists(self, searchPaletteId):
        with open('favoritePalettes.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, fieldnames=['id'])

            # Skip header
            next(csv_reader)

            # Loop through every line in the csv list
            for line in csv_reader:

                # Get an id from the csv list
                curPaletteId = int(line['id'])

                # Match found, returning True
                if curPaletteId == searchPaletteId:
                    return True
                
            # No matches found, returning False
            return False

'''PO = paletteOpener()
PO.addPalette(8, "hsssi", "sssslink here")
print(PO.getIfPaletteIdExists(3))'''