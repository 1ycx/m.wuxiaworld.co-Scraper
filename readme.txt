===========================================================================================================================
## About:

Python Script To Copy m.wuxiaworld.co Chapters Into EPUB File.
Just Enter The Novel URL And You're Done!
I'll Try To Add Any Necessary Updates.
===========================================================================================================================
## Problem(s) :

None Yet(Report if any).
===========================================================================================================================
## Documentation :

    For Beginners, After Setting Up A Working Python 3 Environment(Along With Latest pip), You Need To Install Some Packages. To Install, Run These Commands In Your CMD/Terminal :
        pip3 install bs4
        pip3 install ebooklib
        pip3 install requests
        pip3 install html5lib=="0.9999999"

    Download The Python Script And Unzip It.

    Open The Script With A Text Editor And Read The Details Inside.

    In Case The Script Was Not Updated According To The Changes In Website, You Might Refer The BeautifulSoup Docs To Make Changes Accordingly.

    To Run, Open CMD/Terminal, Navigate To The Unzip Location And Type : python3 code.py or python code.py

    EPUB File Will Be Saved At The Location Of Script.
===========================================================================================================================
## Working :

    Set Novel Link in novelURL
    If Specific No. Of Chapters Are To Be Downloaded, Then Enter 2 And Provide The start And end Chapters.
    All Chapters Of Corresponding Novel Will Be Downloaded And Saved As novel-name_start-chapter_end-chapter.epub
===========================================================================================================================
## Parsing :

html5lib Is Used Because Although Being Tiny Winy Bit Slow, It Generates Valid HTML. You May Compare Others Here, Differences Between Parsers. I've Copied The Table From BS4 Website Below To Give A Faint Overview.
===========================================================================================================================
## If Any Problem Occurs With html5lib :

    In Case You Update It Accidentally, You Can Reinstall The Specific Version By Checking The Details For Beginners.
    Another Choice, Change html5lib To lxml - If Installed, Otherwise To Python's Inbuilt html.parser .
===========================================================================================================================
## License

Copyright © 2018 Kogam22. Released under the terms of the MIT license.
===========================================================================================================================
