# JobTrackr

An scripts the manage and store job application status and give statistics to the user.

## Requirement
- Python 3.9+
- Pandas

## Getting started
Usage: `python jobTrackr.py -options filename`

Valid status inputs:
- applied
- interview
- offer
- resumeReject *(note: this status should be used for rejection where you have never got an interview)*
- interviewReject *(note: this status should be used for rejection that happen after an interview)*

Options:
- `-m`, `--make`: creating file to store new filelist with name typed in the argument.
- `-a`, `--add [other flag]`: add job application to the joblist with default status of applied. 
- `-u`, `--update [other flag]`: update an status of an job application and update to current date if it turn to interview, offered, unless specify otherwise
- `-n`, `--name`: name of the company, required to be enter after add or update flag, optional for after lookUp flag
- `-p`, `--position`: position applied for, required to be enter after add or update flag, optional for after lookup flag
- `-s`, `--status`: current status optional to be enter after add flag, optional for after lookup flag
- `-d`, `--date`: date applied optional to be enter after add and update, optional for after lookup flag. The format of input of the date must be in mxxdxxyxxxx.
- `-i`, `--id`: the job id number displayed in the list, required to be inputed after the update flag
- `-l`, `--list [optional flag]`: list the all application,  query specific parameter, if no parameter is inputted, it will default to listing all application.
- `-b`, `--before`: jobs posted before this date, must be optionally inputted after lookUp flag
- `-af`, `--after`: jobs posted after this date, must be optionally inputted after lookUp flag
- `-g`, `--ghosted [x days]`: list out companies that never responded in x certain days since last update, default is to set as 21 days.
