
import csv
import pandas as pd

# THANKS TO https://youtube.com/watch?v=q5uM4VKywbA
class paletteOpener():
    
    def getPalette(self, paletteNum : int): # TODO: Find return data type
        '''
        Grabs a palette from the csv list based on the palette row
        In the csv list

        Args:
            paletteNum (0 <= int < max rows): The palette to get info
                                              from

        Returns:
            Array[String : id, String : name, String : imgUrl]: Palette info
        '''
        with open('favoritePalettes.csv', 'r') as csv_file:

            # Open the file reader
            csv_reader = csv.reader(csv_file)

            next(csv_reader)

            rows = list(csv_reader)

            paletteData = rows[paletteNum]

            # Close the file
            csv_file.close

        return paletteData

    def getPaletteSection(self, paletteStart : int, paletteEnd : int): # TODO: Find return data type
        '''
        Gets multiple palettes of information at the same time
        Given a start and end position to grab from

        Args:
            paletteStart(0 <= int < max rows): Start position to grab palettes
                                               from
            paletteEnd(paletteStart < int < max rows): End position to grab
                                                       palettes from
        
        Returns:
            Array[Arrays[String : id, String : name, String : imgUrl]]: An array containing
                                                                        palette info
        '''
        with open('favoritePalettes.csv', 'r') as csv_file:

            # Open the file reader
            csv_reader = csv.reader(csv_file)

            next(csv_reader)

            rows = list(csv_reader)

            # Cap the maximum palette count to the max size of the list
            # Ex. If there's only 3 items, but you requested 5, it will only grab 3 items, not 5
            paletteEnd = min(paletteEnd, len(rows))

            paletteData = rows[paletteStart:paletteEnd+1]

            # Close the file
            csv_file.close

        return paletteData
    
    # CREDIT TO https://www.tutorialspoint.com/how-to-delete-only-one-row-in-csv-with-python
    def removePalette(self, paletteId : int):
        '''
        Removes a specific palette id from the csv list

        Args:
            paletteId (int): The id to remove from the csv list
        '''
        df = pd.read_csv('favoritePalettes.csv', index_col='id')
        df = df.drop(paletteId)
        df.to_csv('favoritePalettes.csv', index=True)

    # THANKS TO https://www.geeksforgeeks.org/how-to-append-a-new-row-to-an-existing-csv-file/
    def addPalette(self, paletteId : int, paletteName : str, paletteImgUrl : str):
        '''
        Adds a palette to the csv list

        Args:
            paletteId (int): The id of the palette
            paletteName (String): The name of the palette
            paletteImgUrl (String): The url of the palette image
        '''
        # THANKS TO https://stackoverflow.com/questions/16864683/empty-space-in-between-rows-after-using-writer-in-python
        # For newline assistance

        # Open the file in append mode
        with open('favoritePalettes.csv', 'a', newline="") as csv_file:

            # Create writer object
            csv_writer = csv.writer(csv_file)

            # Add row to the end
            csv_writer.writerow([paletteId, paletteName, paletteImgUrl])

            csv_file.close()
    
    def getIfPaletteIdExists(self, searchPaletteId : int) -> bool:
        '''
        Returns if a given palette id exists in the csv list

        Args:
            searchPaletteId (int): Checks if the id matches any palettes in storage

        Returns:
            boolean: True if the palette does exist, false if not
        '''
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
    
    # CREDIT TO: https://www.tutorialspoint.com/how-to-count-the-number-of-lines-in-a-csv-file-in-python#:~:text=Using%20the%20len()%20Function,lines%20in%20the%20CSV%20file.
    def getNumFavoritedPalettes(self) -> int:
        '''
        Returns:
            int: The number of palettes favorited
        '''
        # Read the CSV file into a pandas DataFrame object
        df = pd.read_csv('favoritePalettes.csv')

        # Count the number of rows in the DataFrame object using the built-in len() function
        num_lines = len(df)

        return num_lines