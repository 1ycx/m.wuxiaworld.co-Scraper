import os
import requests as req
from bs4 import BeautifulSoup as bs
from ebooklib import epub

# Create The EPUB File
book = epub.EpubBook()
book.set_language('en')

# Enter The Novel URL Here
novelURL =  'http://m.wuxiaworld.co/Peerless-Martial-God/'
novelChapURL = novelURL + 'all.html'
while novelURL == '':
    print("Novel URL Not Provided Inside The Script.")
    novelURL = str(input("Please Enter Novel URL : "))
print("\r\nNovel URL Set")

# Main Novel Page -- Get, Create Instance & Select
page = req.get(novelURL)
soup = bs(page.text, "html5lib")
about = soup.select_one('.synopsisArea_detail')
synopsis = soup.select_one('.review')

# Novel Chapters Page -- Get, Create Instance & Select
pageChap = req.get(novelChapURL)
so = bs(pageChap.text, "html5lib")
chapLi = so.select_one("#chapterlist")

# Book Title
title = soup.select_one('header span').text
book.set_title(title)
book.spine = ['nav']

# Get Chapter links & titles
chapTitles = []
links = []
for a in chapLi.findAll('a'):
    link = novelURL + a.get('href')
    links.append(link)
    chapTitles.append(a.string)
# Remove the starting 3 links with href="#bottom" from list
del links[2], links[1], links[0], chapTitles[2], chapTitles[1], chapTitles[0]
print(chapTitles)

# Chapter Links
length = len(links)
start = 0
end = length
print("\r\nName = ", title)
print("\r\nTotal No. Of Chapters = ", length)
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

print("\r\n")

def html_gen(elem, soupInstance, value, tagToAppend, insert_loc=None):
    element = soupInstance.new_tag(elem)
    element.string = value
    if not insert_loc:
        tagToAppend.append(element)
    else:
        tagToAppend.insert(insert_loc, element)

counter = start - 1
err = []
i = 0

for i in range(start, end+1):
    
    try:
        
        if i == length:
            break
        
        #####################
        # Get, Pass & Select
        pageIndividual = req.get(links[i])
        s = bs(pageIndividual.text, "html5lib")    
        div = s.select_one("#chaptercontent")

        #chapterTitle = "Chapter : " + str(i)
        chapterTitle = chapTitles[i]
        tag = s.new_tag("div")
        html_gen("h3", s, chapterTitle, tag)
        html_gen("hr", s, "", tag)
        
        # Remove href
        for a in div.select("a"):
            a['href'] = '#'

        # Append to tag
        tag.append(div)
        print(tag)


        # Creates a chapter
        c2 = epub.EpubHtml(title=chapterTitle, file_name='chap_'+str(i)+'.xhtml', lang='hr')
        c2.content = tag.encode("utf-8")
        book.add_item(c2)


        # Add to table of contents
        book.toc.append(c2)    

        # Add to book ordering
        book.spine.append(c2)

        print("Parsed Chapter", i)
        counter += 1


    except KeyboardInterrupt as e:
        print("Keyboard Interrupt")
        print(e)
        break
    
    except IndexError as e:
        print(e)
        print("Possibly Incorrect Link For Chapter", i)
        print("Skipping Chapter", i)
        err.append(i)
    
    except Exception as e:
        print(e)
        err.append(i)

if counter < 0: counter = 0

# About Novel
about.find('img').decompose() # Remove IMG tags
for a in about.select("a"):   # Remove anchor tags
    a['href'] = '#'
html_gen("hr", soup, "", about)
html_gen("h3", soup, "Description", about)
syn = synopsis.text.replace("Description","")
html_gen("p", soup, syn, about)
html_gen("hr", soup, "", about)
html_gen("h3", soup, "About This Download : ", about)
html_gen("p", soup, "Total Chapters = " + str(counter), about)
html_gen("p", soup, "No. Of Chapters That Raised Exceptions = " + str(len(err)), about)
if len(err) != 0:
    html_gen("p", soup, "And They Are : ", about)
    for i in err:
        html_gen("li", soup, str(i), about)
html_gen("hr", soup, "", about)

# Create About Novel Page
c1 = epub.EpubHtml(title="About Novel", file_name='About_novel'+'.xhtml', lang='hr')
c1.content = about.encode('utf-8')
book.add_item(c1)
book.toc.insert(0, c1)
book.spine.insert(1, c1)
print("Created \"About Novel\" Page")

# Add Navigation Files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Defines CSS Style
style = 'p { text-align : left; }'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# Adds CSS File
book.add_item(nav_css)

# Location Where File Will Be Saved
# Default Location Will Be The Place Where This Script Is Located
# To Change, 
# 1 - Add The Location Inside The Empty pathToLocation
#   Example 1 - Windows : 
#       pathToLocation = 'C:\\Users\\Adam\\Documents\\'
#       Notice The Extra \ To Be Added Along With Every Original - This Is Compulsory For Every \
#   Example 2 - Unix/POSIX Based(OS X, Linux, Free BSD etc) : 
#       pathToLocation = '/home/Adam/Documents/'   
#       Notice That No Extra / Are Added Along With Original  
# OR 
# 2 - Move This Script To, And Run From The Location To Be Saved
pathToLocation = ''
downloadDetails = '"' + title + '_' + str(start) + '_' + str(counter) + '.epub"'
saveLocation = pathToLocation + downloadDetails


print("Saving . . .")

# Saves Your EPUB File
epub.write_epub(saveLocation, book, {})

# Location File Got Saved
if pathToLocation == '':
    print("Saved at", os.getcwd(), 'as', downloadDetails) 
    # Example : Saved at /home/Adam/Documents as "The Strongest System_0_3.epub"
else :
    print("Saved at", saveLocation)
