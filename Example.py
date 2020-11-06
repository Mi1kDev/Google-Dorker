from Classes import Dorker
query = "passwords" #any main search query to act as a basis for the search
num = 10 #any integer up to 100
search = Dorker(
    query,
    num, 
    as_filetype="log" #optional search parameters
    )
#dorker.paramList() this will show each optional search parameter and what it does
dorker.findResults() #finds any relevant search results
dorker.exportToTextFile() #exports links to a text file
#dorker.saveLinks() this will download the content from each url found