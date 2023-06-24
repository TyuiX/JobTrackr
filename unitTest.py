from jobTrackr import *
import pytest
def testMakingFile():
    make('new_file')
    #testing create new excel file
    assert os.path.exists('new_file.csv')
    #test if u can make new file again
    assert make('new_file') == -1
    os.remove('new_file.csv')