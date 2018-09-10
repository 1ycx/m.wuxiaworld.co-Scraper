<img src="https://img.shields.io/badge/Status-Working-blue.svg" >

# About: 
<b>Python Script To Copy [m.wuxiaworld.co](http://m.wuxiaworld.co) Chapters Into EPUB File.</b>

Ask Me, Why This Website? Well, It Has Novels From **Webnovel(Qidan) & WuxiaWorld** With All Latest Chapters <b><u>Unlocked</u></b>. 

**No Spirit Stones, No Patreon, No Subscription Or Any Of Those Things Required To Read The Latest Chapters!**
Don't Take My Word For It ? Check It Out.

How Does The Script Work ? Just Enter The Novel URL Inside The Script And You're Done!

<h4>I'll Try To Add Any Necessary Updates.</h4>

<br/>

## Problem(s) :
* None Yet(Report if any).

## Sample :
```bash
kogam22@home:~/code$ python3 code.py

Novel URL Set

Name :  The Magus Era

Total No. Of Chapters =  1792

---------------------------------------------------
Enter 1 - To Download All Chapters
Enter 2 - To Download A Part, Like 1-100 Or 400-650
Enter 3 - To View Chapter Titles Before Download

Enter Your Choice : 2
---------------------------------------------------

===================================================
**Note : "First Chapter" Starts From "1"
         "Last Chapter" Ends At "1792"

Enter First Chapter : 1
Enter Last Chapter  : 10
===================================================
Parsed Chapter : Prologue
Parsed Chapter : Chapter 1 - Hunter
Parsed Chapter : Chapter 2 - Malice
Parsed Chapter : Chapter 3 - Challenge
Parsed Chapter : Chapter 4 - Deal
Parsed Chapter : Chapter 5 - Gain
Parsed Chapter : Chapter 6 - Parents
Parsed Chapter : Chapter 7 - Defiance
Parsed Chapter : Chapter 8 - Different Races
Parsed Chapter : Chapter 9 - Calculation
Created "About Novel" Page
Saving . . .
Saved at /home/kogam22/code as "The Magus Era_0_9.epub"
kogam22@home:~/code$
```

## Documentation :
1. For Beginners, After Setting Up A Working Python(>=3.6) Environment(Along With Latest `pip`), You Need To Install Some Packages. To Install, Run This Command In Your CMD/Terminal :
   * `pip install -r requirements.txt`
2. Download The Python Script And Unzip It.

3. Open The Script With A Text Editor And Read The Details Inside.

4. In Case The Script Was Not Updated According To The Changes In Website, You Might Refer The [**BeautifulSoup Docs**](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) To Make Changes Accordingly.

4. To Run, Open CMD/Terminal, Navigate To The Unzip Location And Type :
   * Linux - `python3 code.py` 
   * Windows - `python code.py` or `py code.py`

5. EPUB File Will Be Saved At The Location Of Script.

### Working :
* Set Novel Link in `novelURL`
  * Example : http://m.wuxiaworld.co/Martial-God-Space/ **|** http://m.wuxiaworld.co/Tales-of-Demons-and-Gods/
* If Specific Sequence Of Chapters Are To Be Downloaded, Then Enter `2` And Provide The `start` And `end` Chapters.
* EPUB File Will Be Saved In The Format `NovelName_start-chapter_end-chapter.epub`

### Parsing :
`html5lib` Is Used Because Although Being Tiny Winy Bit Slow, It Generates Valid HTML. You May Compare Others Here, [**Differences Between Parsers**](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#differences-between-parsers).
I've Copied The Table From BS4 Website Below To Give A Faint Overview.

<table border="1" class="docutils">
<colgroup><col width="18%"><col width="35%"><col width="26%"><col width="21%"></colgroup>
<tbody valign="top">
   <tr class="row-odd"><td><b>Parser</b></td>
      <td><b>Typical usage</b></td>
      <td><b>Advantages</b></td>
      <td><b>Disadvantages</b></td>
   </tr>
   <tr class="row-even"><td><b>Python’s html.parser</b></td>
      <td><code class="docutils literal"><span class="pre">BeautifulSoup(markup,</span> <span class="pre">"html.parser")</span></code></td>
      <td><ul class="first last simple">
            <li>Batteries included</li>
            <li>Decent speed</li>
            <li>Lenient (as of Python 2.7.3 and 3.2.)</li>
         </ul>
      </td>
      <td><ul class="first last simple">
            <li>Not very lenient (before Python 2.7.3 or 3.2.2)</li>
         </ul>
      </td>
   </tr>
   <tr class="row-odd"><td><b>lxml’s HTML parser</b></td>
      <td><code class="docutils literal"><span class="pre">BeautifulSoup(markup,</span> <span class="pre">"lxml")</span></code></td>
      <td><ul class="first last simple">
            <li>Very fast</li>
            <li>Lenient</li>
          </ul>
      </td>
      <td><ul class="first last simple">
            <li>External C dependency</li>
          </ul>
      </td>
   </tr>
   <tr class="row-even"><td><b>lxml’s XML parser</b></td>
      <td><code class="docutils literal"><span class="pre">BeautifulSoup(markup,</span> <span class="pre">"lxml-xml")</span></code>
   <code class="docutils literal"><span class="pre">BeautifulSoup(markup,</span> <span class="pre">"xml")</span></code></td>
      <td><ul class="first last simple">
            <li>Very fast</li>
            <li>The only currently supported XML parser</li>
          </ul>
      </td>
      <td><ul class="first last simple">
            <li>External C dependency</li>
          </ul>
      </td>
   </tr>
   <tr class="row-odd"><td><b>html5lib</b></td>
      <td><code class="docutils literal"><span class="pre">BeautifulSoup(markup,</span> <span class="pre">"html5lib")</span></code></td>
      <td><ul class="first last simple">
            <li>Extremely lenient</li>
            <li>Parses pages the same way a web browser does</li>
            <li>Creates valid HTML5</li>
          </ul>
      </td>
      <td><ul class="first last simple">
            <li>Very slow</li>
            <li>External Python dependency</li>
          </ul>
      </td>
   </tr>
</tbody>
</table>

#### If Any Problem Occurs With `html5lib` :
* In Case You Update It Accidentally, You Can Reinstall The Specific Version By Checking The Details For Beginners.
* Another Choice, Change `html5lib` To `lxml` - **If Installed**, Otherwise To Python's Inbuilt `html.parser` .

<br/>

## License

Copyright &copy; 2018 [Kogam22](https://github.com/Kogam22). Released under the terms of the [Apache 2.0 license](LICENSE).
