from goodreads import client
import json

def singleArray(inputlist):
    outputlist = []
    for i in inputlist:
      outputlist.extend(i)
    return outputlist

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

#authetification
gc = client.GoodreadsClient('fCUHaHylHEkSW3jJcZJTQ', 'dOKwd2Kewa5sIpoAynUEVl44s5wscrwWoAiGwBuijTI')

#get all books by query
books = gc.search_books('Lesbian', search_field='genre')

#parse books to single array
#books = singleArray(books)

#to json
data = []
for book in books:
    i = {}
    i['isbn'] = book.isbn
    i['isbn13'] = book.isbn13
    i['title'] = book.title
    i['author'] = book.authors[0].name
    i['link'] = book.link
    i['popular_shelves'] = [shelve.name for shelve in book.popular_shelves]
    data.append(i)
    
writeToJSONFile('./','ff-books',data)
