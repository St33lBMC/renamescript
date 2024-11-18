'''
11/13/24

Renames files based on keywords appeneded to the current filename
Originally designed for some ciruit board filename stuff but could be repurposed for other things I suppose

Usage: python3 renamescript.py
while in the directory containing the files that need to be renamed

Output files will be created in a subdirectory of the selected location

example: "18BG - Top Paste.gbr" ===> "spt.gbr"

version 1.1 -- added file explorer popup for easy directory selection
version 1.2 -- added settings file for ease as shipping as an executable

for compiling the executable, 
pyinstaller renamescript.py --onefile --noconsole
'''

import os, sys, shutil, json, tkinter as tk
from tkinter import filedialog


settings_file = "settings.json"

# default settings in the event settings.json cannot be read
output_dir_name = "EasyPCBUSA"
replacements = {
    "Bottom Copper": "gtl.gbr",
    "Bottom Paste": "spb.gbr",
    "Bottom Resist": "smb.gbr",
    "Bottom Silk": "ssb.gbr",
    "NC Drill Data": "drl.drl",
    "Outline": "otl.gbr",
    "Top Copper": "gtl.gbr",
    "Top Paste": "spt.gbr",
    "Top Resist": "smt.gbr",
    "Top Silk": "sst.gbr",
    "Inner Layer 1": "in1.gbr",
    "Inner Layer 2": "in2.gbr"
}

# read settings from the settings file and store in json
# includes the set of keywords and corresponding substitutions, 
#     as well as the output directory name
def read_settings(fname):
    with open(fname, 'r') as f:
        data = json.load(f)
    return data

def __main__():
    # attempt to read settings from json
    try:
        settings = read_settings(settings_file)
        replacements = settings["replacements"]
        output_dir_name = settings["outputdir"]
    except:
        print("unable to read settings.json, using default settings")

    # get the desired directory for running the rename script
    root = tk.Tk()
    root.withdraw()

    # launch a file selector window to choose directory to work in
    run_path = filedialog.askdirectory(title="Select Folder Containing Files to Rename")
    os.chdir(run_path)
    files = os.listdir()
    # print("running in " + runpath)

    # create directory for output files if it does not currently exist
    if not os.path.exists(run_path + "/" + output_dir_name):
        os.mkdir(output_dir_name)
    os.chdir(run_path + "/" + output_dir_name)

    # for each filename in the current working directory
    # print(files)
    for file in files:
        # for each keyword in the list
        for keyword in replacements:
            # if the keyword is in the filename, ignoring upper/lowercase
            if keyword.lower() in file.lower():
                new_name = replacements.get(keyword)
                # print("creating " + newname)
                # copy the old file to the subdirectory using the new name
                shutil.copy(run_path + "/" + file, new_name)
                break

if __name__ == "__main__":
    __main__()