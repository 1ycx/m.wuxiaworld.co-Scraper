import sys, os
import random as ra
import requests as req
import asyncio
from aiostream import stream, pipe
from aiohttp import ClientSession
from ebooklib import epub
from bs4 import BeautifulSoup as bs


err, urls_titles, min_urls_titles = [], [], []
length, counter, start, end = 0, 0, 0, 0
book = epub.EpubBook()

def html_gen(elem, soupInstance, value, tagToAppend, insert_loc=None):
    element = soupInstance.new_tag(elem)
    element.string = value
    if not insert_loc:
        tagToAppend.append(element)
    else:
        tagToAppend.insert(insert_loc, element)

def intro():
    global length
    global start
    global end
    length = len(urls_titles)
    start = 0
    end = length
    print("\r\nName : ", title)
    print("\r\nTotal No. Of Chapters = ", length)
    while True:
        print("\r\n---------------------------------------------------")
        print("Enter 1 - To Download All Chapters")
        print("Enter 2 - To Download A Part, Like 1-100 Or 400-650")
        print("Enter 3 - To View Chapter Titles Before Download")
        check = int(input("\r\nEnter Your Choice : "))
        print("---------------------------------------------------")
        if check == 3:
            print("\r\nx-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x")
            print("Enter 1 - To View All Chapter Titles")
            print("          (The List Can Be Very Long When Chapters > 100)")
            print("Enter 2 - To View A Specific Title")
            temp1 = int(input("\r\nEnter Your Choice : "))
            print("x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x")
            if temp1 == 2:
                temp2 = int(input("\r\nEnter Chapter Number : ")) - 1
                print(urls_titles[temp2][0])
                continue
            if temp1 == 1:
                print(urls_titles[0:][0])
                continue
            else:
                print("\r\n### Invalid Choice ###")
                continue
        if check == 2:
            print("\r\n===================================================")
            print("**Note : \"First Chapter\" Starts From \"1\"")
            print("         \"Last Chapter\" Ends At \"{0}\"".format(length))
            start = int(input("\r\nEnter First Chapter : "))
            end   = int(input("Enter Last Chapter  : "))
            print("===================================================")
            if start > 0 and end < length + 1:
                if start < end or start == end:
                    start, end = start - 1, end - 1
                    return start, end
                else:
                    print("Please Enter start And end Chapters Properly. Swapping start and end.")
                    print("start =", end, "end =", start)
                    start, end = end, start
                    return start, end
            else:
                print("\r\n**Please Enter start And end Chapters Properly.**\r\n")
                continue
        elif check == 1:
            print("Okay, All Available Chpaters Will Be Downloaded.")
            return start, end
        else :
            print("Invalid Choice. All Available Chapters Will Be Downloaded.")
            return start, end

def get_urls_titles():
    for a in chapLi.findAll('a'):
        link = novelURL + a.get('href')
        l = (link, a.string)
        urls_titles.append(l)
    del urls_titles[2], urls_titles[1], urls_titles[0]

async def fetch(url, title):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()
            return (response, title)

def process(response, title):
    global counter
    try:
        #####################
        # Get, Pass & Select
        s = bs(response, "html5lib")    
        div = s.select_one("#chaptercontent")

        # Create new div tag to add chapter title and content
        chapter = s.new_tag("div")
        chapterTitle = title

        html_gen("h4", s, chapterTitle, chapter)
        html_gen("hr", s, "", chapter)

        # Remove href
        for a in div.select("a"):
            a['href'] = '#'

        # Append to tag
        chapter.append(div)

        # Check if name exists
        if book.get_item_with_href(title + '.xhtml'):
            title += str(ra.randint(1,5))

        # Creates a chapter
        c2 = epub.EpubHtml(title=chapterTitle, file_name=title+'.xhtml', lang='hr')
        c2.content = chapter.encode("utf-8")
        book.add_item(c2)

        # Add to table of contents & book ordering
        book.toc.append(c2)    
        book.spine.append(c2)

        # Creates a chapter
        print("Parsed Chapter :", title)
        counter += 1

    except KeyboardInterrupt as e:
        print("Keyboard Interrupt")
        print(e)
        sys.exit()

    except IndexError as e:
        print(e)
        print("Possibly Incorrect Link For Chapter", title)
        print("Skipping Chapter", title)
        
    except Exception as e:
        print(e)

def save():
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

async def main():
    get_urls_titles()
    global start 
    global end 
    global counter
    global err
    
    start, end = intro()
    
    if end == length:
        min_urls_titles = urls_titles[start:]
    else:
        min_urls_titles = urls_titles[start:end+1]
    
    counter = start - 1

    xs = stream.iterate(min_urls_titles)
    ys = stream.starmap(xs, fetch, task_limit=100)
    zs = stream.starmap(ys, process, task_limit=100)
    await zs
        
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

    save()

if __name__=="__main__":
    book.set_language('en')

    # Enter The Novel URL Here
    novelURL =  'http://m.wuxiaworld.co/King-of-Gods/'
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
