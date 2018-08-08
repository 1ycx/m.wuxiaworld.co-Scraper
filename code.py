import os
import requests as req
from bs4 import BeautifulSoup as bs
from ebooklib import epub

# Create The EPUB File
book = epub.EpubBook()
book.set_language('en')

# Enter The Novel URL Here
novelURL =  'http://m.wuxiaworld.co/Super-Gene/'
novelURLChap = novelURL + 'all.html'
while novelURL == '':
    print("Novel URL Not Provided Inside The Script.")
    novelURL = str(input("Please Enter Novel URL : "))
print("\r\nNovel URL Set")

# Get & Passing To Beautiful Soup Main Novel Page
page = req.get(novelURL)
soup = bs(page.text, "html5lib")

# Get & Passing To Beautiful Soup Novel Chapters Page
pageChap = req.get(novelURLChap)
so = bs(pageChap.text, "html5lib")

# Seperating Parts From Soup
chapLi = so.select_one("#chapterlist") # Using so instance of soup

about = soup.select_one('.synopsisArea_detail')
synopsis = soup.select_one('.review')

# Book Title
title = soup.select_one('header span').text
book.set_title(title)
book.spine = ['nav']


# Get All Chapter Links
links = []
for a in chapLi.findAll('a'):
    link = novelURL + a.get('href')
    links.append(link)
del links[0], links[1], links[2]


# Chapter Links
length = len(links)
start = 0
end = length
print("\r\nTotal No. Of Chapters = " + str(length))
print("\r\nPlease Note That No. Of Chapters Shown May Not Match The Actual Numbering")
print("Because Some Chapters Maybe Numbered As 187-A, 187-B, 187-C Although Being")
print("3 Different HTML Pages.")
print("\r\nEnter 1 - To Download All Chapters")
print("\r\nEnter 2 - To Download A Part, Like 0-100 Or 400-650")
check = int(input("\r\nEnter Your Choice : "))
if check == 2:
    print("\r\n**Note : To Download From First Chapter, Enter \"First Chapter\"") 
    print("         Value As \"0\", Not \"1\"")
    start = int(input("\r\nEnter First Chapter : "))
    end   = int(input("Enter Last Chapter  : "))
elif check == 1:
    print("Okay, All Available Chpaters Will Be Downloaded.")
else :
    print("Invalid Choice. All Available Chapters Will Be Downloaded.")


def html_gen(elem, val, tag, insert_loc=None):
    element = soup.new_tag(elem)
    element.string = val
    if insert_loc == None:
        tag.append(element)
    else:
        tag.insert(insert_loc, element)

counter = 0
err = []

for i in range(start, end+1):
    
    try:
    
        if i == length:
            break

        #####################
        # Sets the adress here 
        pageIndividual = req.get(links[i])

        # Modifies the HTML received
        s = bs(pageIndividual.content, "html5lib")    
        #chapterTitle = "Chapter : " + str(i)
        
        
        div = s.select_one("#chaptercontent")
        chapterTitle = div.contents[0]

        for a in div.select("a"):
            a.decompose()

        # Creates a chapter
        c2 = epub.EpubHtml(title=chapterTitle, file_name='chap_'+str(i)+'.xhtml', lang='hr')
        c2.content = div.encode("utf-8")
        book.add_item(c2)


        # Add to table of contents
        book.toc.append(c2)    

        # Add to book ordering
        book.spine.append(c2)

        print("Parsed Chapter " + str(i))
        counter = counter + 1

    except KeyboardInterrupt as e:
        print("Keyboard Interrupt")
        print(e)
        break
    
    except IndexError as e:
        print(e)
        print("Possibly Incorrect Link For Chapter " + str(i))
        print("Skipping Chapter " + str(i))
        err.append(i)
    
    except Exception as e:
        print(e)
        err.append(i)

# About Novel
about.find('img').decompose()
for a in about.select("a"):
    a.decompose()
html_gen("hr", '', about)
html_gen("h3", "Description", about)
html_gen("p", synopsis.text, about) # Some strip to be done here for proper description
html_gen("hr", '', about)
html_gen("h3", "About This Download : ", about)
html_gen("p", "Total Chapters = " + str(counter), about)
html_gen("p", "No. Of Chapters That Raised Exceptions = " + str(len(err)), about)
if len(err) != 0:
    html_gen("p", "And They Are : ", about)
    for e in err:
        html_gen("li", str(e), about)
html_gen("hr", '', about)



# Create About Novel Page
aboutNovelTitle = "About Novel"
c1 = epub.EpubHtml(title=aboutNovelTitle, file_name='About_novel'+'.xhtml', lang='hr')
c1.content = about.encode('utf-8')
book.add_item(c1)
book.toc.insert(0, c1)
book.spine.insert(1, c1)
print("Created \"About Novel\" Page")

# Add Navigation Files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Defines CSS Style
style = 'p {text-align: left;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# Adds CSS File
book.add_item(nav_css)

# Location Where File Will Be Saved
# Default Location Will Be The Place Where This Script Is Located
# To Change, 
# 1 - Add The Location Inside The Empty pathToLocation
#   Example 1.1 - Windows : 
#       pathToLocation = 'C:\\Users\\Adam\\Documents\\'
#       Notice The Extra \ To Be Added Along With Every Original - This Is Compulsory For Every \
#   Example 1.2 - Linux : 
#       pathToLocation = '/home/Adam/Documents/'   
#       Notice That No Extra / Are Added Along With Original  
# OR 
# 2 - Move This Script And To, And Run From The Location To Be Saved
pathToLocation = ''
saveLocation = pathToLocation + title + '_' + str(start) + '_' + str(i) + '.epub'

print("Saving . . .")

# Saves Your EPUB File
epub.write_epub(saveLocation, book, {})

# Location File Got Saved
if pathToLocation == '':
    print("Saved at " + str(os.getcwd()) + ' as "' + title + '_' + str(start) + '_' + str(i) + '.epub"')
else :
    print("Saved at " + saveLocation)

