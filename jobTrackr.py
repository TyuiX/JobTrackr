import getopt
import pandas as pd
import sys, os, datetime
from openpyxl import Workbook
arguments = sys.argv


# Define the flags as powers of 2 for bitmasking 
FLAG_A = 1  
FLAG_U = 2  
FLAG_L = 4
FLAG_B = 8
FLAG_AF = 16
FLAG_G = 32

# Initialize the flags
flags = 0

def parser(argv):
    short_options = 'm:a:u:n:p:s:d:i:l:b:af:g:'
    long_options = ['make=', 'add=', 'update=', 'name=', 'position=', 'status=',
                    'date=', 'id=', 'list', 'before=', 'after=', 'ghosted=']
    
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
            argv[-1] += '.csv'
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
    dataframe=  pd.read_csv(argv[-1])
    if flags & FLAG_A:
        #see if there other flag that dosent belong with add flag
        if flags & 62:
            raise SyntaxError
        add(name, position, status,  current_year, current_month, current_day, dataframe)
        dataframe.to_csv(argv[-1], index=False)
    elif flags & FLAG_U:
        if flags & 61:
            raise SyntaxError
        update(id, name, position, status,  current_year, current_month, current_day, dataframe)
        dataframe.to_csv(argv[-1], index=False)
    elif flags & FLAG_L:
        if flags & 61:
            raise SyntaxError
        update(id, name, position, status,  current_year, current_month, current_day)




#create new file
def make(filename):
    if not filename.endswith('.csv'):
        filename += '.csv'

    if not os.path.exists(filename):
        try:
            with open(filename, 'w') as file:
                file.write('company, position, status, date\n')  # Add column headers
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

    

def add(name, position, status,  current_year, current_month, current_day, dataframe):
    if not (name and position):
        raise SyntaxError
    date = unparseDate(current_year, current_month, current_day)
    data = {'company': name, 'position': position, 'status': status , 'date': date}
    dataframe = dataframe.append(data, ignore_index=True)
    return 0
        
    

def update(id, name, position, status,  current_year, current_month, current_day, dataframe):
    if id != None:
        dataframe[id, 'status'] = status
    else:
        query = (dataframe['name'] == name) & (dataframe['position'] == position)
        dataframe.loc[query, 'status'] = status

def list(options):
    pass

#return array as year month day
def parseDate(date):
    # Extract the month, day, and year using string slicing
    month = int(date[1:3])
    day = int(date[4:6])
    year = int(date [7:])
    if  not (1 <= month <= 12):
        return None
    elif  not (1 <= date <= 31):
        return None
    return [year, month, day]   

#return an unparsed string formatted as mxxdxxyxxxx
def unparseDate(current_year, current_month, current_day):
    year_str = str(current_year)
    month_str = str(current_month)
    day_str = str(current_day)
    month_str = month_str.zfill(2)
    day_str = day_str.zfill(2)
    formatted_date = 'm{}d{}y{}'.format(month_str, day_str, year_str)

    return formatted_date