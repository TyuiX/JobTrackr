import getopt
import sys, os, datetime
from openpyxl import Workbook
arguments = sys.argv
filename = None

# Define the flags as powers of 2 for bitmasking 
FLAG_A = 1  
FLAG_U = 2  
FLAG_L = 4
FLAG_B = 8
FLAG_AF = 16
FLAG_G = 32
FLAG_R = 64

# Initialize the flags
flags = 0

#parse and handle the arguments
filePointer = None 
def parser(argv):
    short_options = 'm:a:u:n:p:s:d:i:l:b:af:g:r:'
    long_options = ['make=', 'add=', 'update=', 'name=', 'position=', 'status=',
                    'date=', 'id=', 'list', 'before=', 'after=', 'ghosted=', 'remove=']
    
    #initalize stored value
    argv = sys.argv
    if (argv.length == 1):
        print('No arguments was given')
        sys.exit(2)
    name = None
    position = None
    status = 'applied'
    id = None
    ghosted = 21
    current_datetime = datetime.now()
    current_year = current_datetime.strftime("%Y")  # 4-digit year
    current_month = current_datetime.strftime("%B")  # Full month name
    current_day = current_datetime.strftime("%d")
    file = sys.argv[-1]

    try:
        # Parse the command-line arguments
        opts, args = getopt.getopt(argv[1:-1], short_options, long_options)
    except getopt.GetoptError:
        # Handle invalid arguments or options
        print('Invalid arguments: usage python jobTrackr.py [options] filename')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-m', '--make'):
            make(argv[-1])
        elif opt in ('-a', '--add'):
            flags += FLAG_A
        elif opt in ('-u', '--update'):
            flags += FLAG_U
        elif opt in ('-n', '--name'):
            if not arg:
                raise ValueError
            name = arg
            pass
        elif opt in ('-p', '--position'):
            if not arg:
                raise ValueError
            position = arg
            pass
        elif opt in ('-s', '--status'):
            if not arg:
                raise ValueError
            position = arg
            pass
        elif opt in ('-d', '--date'):
            if not arg:
                raise ValueError
            #pare data return an array 
            date = parseDate(arg)
            current_year = date[0]  
            current_month =  date[1]
            current_day =  date[2]
            if not arg:
                raise ValueError
            id = arg
        elif opt in ('-l', '--list'):
            flags += FLAG_L
        elif opt in ('-b', '--before'):
            flags += FLAG_B
        elif opt in ('-af', '--after'):
            flags += FLAG_AF
        elif opt in ('-g', '--ghosted'):
            if arg:
                ghosted = arg
            flags += FLAG_G
        else:
            print('Unrecognized option', opt)
            raise SyntaxError
    
    #process

    if flags & FLAG_A:
        #see if there other flag that dosent belong with add flag
        if flags & 62:
            raise SyntaxError
        add(name, position, status,  current_year, current_month, current_day)
    elif flags & FLAG_U:
        if flags & 61:
            raise SyntaxError
        update(id, name, position, status,  current_year, current_month, current_day)
    elif flags & FLAG_L:
        if flags & 61:
            raise SyntaxError
        update(id, name, position, status,  current_year, current_month, current_day)




#create new file
def make(filename):
    if not filename.endswith('.xlsx'):
        filename += '.xlsx'

    if not os.path.exists(filename):
        try:
            # Open the file in write mode
            workbook = Workbook()

            # Save the workbook
            workbook.save(filename)
            print("File created successfully!")
            return 0

        except IOError:
            print("An error occurred while creating the file.")
            return -1
    else:
        print("File already exists. No action taken.")
        return -1

def openFile(filename):
    global filePointer
    if os.path.exists(filename):
        filePointer = open(filename, 'r')
    else:
        print("file does not exist")

    

def add(name, position, status,  current_year, current_month, current_day):
    if not (name and position):
        raise SyntaxError
    
    

def update(args):
    pass

def list(options):
    pass

#return array as year month day
def parseDate(date):
    pass