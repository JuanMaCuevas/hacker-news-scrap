#!/usr/bin/python

#==========================================================================
# IMPORTS
#==========================================================================
import sys
from optparse import OptionParser
import urllib2
from lxml import html

#==========================================================================
# CONSTANTS
#==========================================================================
NUMBERS = ["%c"%x for x in range(0x30,0x3A)]
NUMBER_POSTS_PER_PAGE = 30
URL_BASE="https://news.ycombinator.com/news?p="

#==========================================================================
# FUNCTIONS
#==========================================================================

# Parse command line flags
def parseCommandLineFlags():
    parser = OptionParser(usage='%prog [OPTIONS] "string"',
                          version='%prog 0.1')
    
    parser.add_option('-v', '--verbose', type='int', default=0,
                      help='Increase verbosity level')

    parser.add_option('-r', '--readfile', type='str',
                      help='Read from a file')
    
    parser.add_option('-w', '--writefile', type='str',
                      help='Write to a file')
    
    parser.add_option('-d', '--dos', action="store_true",
                      help='Use DOS end of line characters (\\r\\n).  By default, \
                           this program outputs UNIX end of line characters (\\n).')
    
    if (len(sys.argv) == 1):
        parser.print_help()
        sys.exit()
    
    (options,args)=parser.parse_args()
    return options, args


# Print debug messages at the user specified verbosity level
def debug(level, message):
    if level <= options.verbose:
        sys.stderr.write(message + '\n')
    return


# Read file and return data as a LIST of stripped strings
def readFile(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            if line.strip() != '':
                lines.append(line.strip())
        ##### If you want to preserve your lines in their original state, remove
        ##### the for loop above and use the following line instead.  You'll
        ##### also need to modify the writeFile fuction not to print newlines.
        #lines = f.readlines()
    return lines


# Write LIST to a file with either DOS or *NIX line endings
def writeFile(filename, lines):
    with open(filename, 'w') as f:
        for line in lines:
            if options.dos:
                f.writelines( ''.join( [line, '\r\n'] ) )
            else:
                f.writelines( ''.join( [line, '\n'] ) )
    return

def getPageFromPostId(postid):
    pid = int(postid) - 1  # starts from 0
    page = (1 + (pid / NUMBER_POSTS_PER_PAGE))
    return page

def createPageUrls(start,end):
    pages = []
    for i in range(start,end+1):
        pages.append(URL_BASE+str(i))
    return pages

def loadPageUrl(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return html

def scrapeAllPosts(page):
    tree = html.fromstring(page)
    print tree.xpath('//span[@class="rank"]/text()')
    # permaLinks = getPermalinks(page)
    # points = getPoints(page)
    # intros = getFirst150Chars()
    # posters = getPoster(page)

    # [getPermalinks(page),getPoints(page),getFirst150Chars(),getPoster(page),)
    # tree = html.fromstring(page)
    return []



def filterPosts(posts,start,end):
    return []

#==========================================================================
# MAIN PROGRAM
#==========================================================================

# Read and parse the command line flags
(options,args) = parseCommandLineFlags()
debug(5, 'Options = %s' % options)
debug(5, 'Arguments = %s' % args)



# If a read file is provided, read it.
if options.readfile:
    inputs = readFile(options.readfile)
    debug(1, '{0} item(s) found in the file {1}.'.format(len(inputs),
                                                         options.readfile) )

# Else look to see if the user specified any line arguments
elif args != []:
    inputs = args
    debug(1, '{0} item(s) found in the arguments.'.format( len(inputs) ) )

# Otherwise read from stdin for data being piped in from another command
else:
    inputs = []
    generator = (line.strip() for line in sys.stdin)
    for line in generator:
        if line != '':
            inputs.append(line)
    debug(1, '{0} item(s) found on stdin.'.format( len(inputs) ) )


##### The majority of your code will probably replace the next line #####
startPost = inputs[0]
endPost = inputs[1]

startPage = getPageFromPostId(startPost)
endPage =  getPageFromPostId(endPost)

pagesUrls = createPageUrls(startPage,endPage)

allPosts = []
for pageUrl in pagesUrls:
    page = loadPageUrl(pageUrl)
    pagePosts = scrapeAllPosts(page)
    allPosts = allPosts + pagePosts
    
filterPosts(allPosts,startPost,endPost)    

outputs =[]# inputs



# If an output file is specified, write to it.
if options.writefile:
    writeFile(options.writefile, outputs)

# Otherwise write it to stdout
else:
    for line in outputs:
        print(line)