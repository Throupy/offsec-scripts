# PID Enumeration Script via LFI
This script can be used to interrogate / enumerate running processes via the /proc/ directory once you have located an LFI vulnerability. I used this script during the "airplane" tryhackme box and a writeup for this can be found on my website (throupy.github.io).

## Usage
```bash
python3 pid_enum.py -t HOST -p PORT -l LFI_PARAM -r PID_RANGE
python3 pid_enum.py -t airplane.thm -p 8000 -l page -r 1000
```
The above command would use the URL `http://airplane.thm:8000/?page=../../../../../proc/<PID>/cmdline` to enumerate processes

The responses of each request will be stored in the `responses/` directory and the filename will be the respective PID e.g. 529.txt would contain the `cmdline` value for PID 529.

## Notes
This script only gets the `cmdline` value from the `/proc` directory. There are many other useful ones, e.g. map, cwd, environ, etc. Feel free to modify the script to interrogate these