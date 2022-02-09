import os
import sys

import ipywidgets as widgets
import requests

from pathlib import Path
from zipfile import ZipFile

week_number = -1

if len(sys.argv) != 2:
    sys.exit("Wrong number of parameters.")
    
else:
    week_number = int(sys.argv[1])

links = ["https://cdrdv2.intel.com/v1/dl/getContent/682344", "https://cdrdv2.intel.com/v1/dl/getContent/682347", 
         "https://cdrdv2.intel.com/v1/dl/getContent/682351", "https://cdrdv2.intel.com/v1/dl/getContent/682352", 
         "https://cdrdv2.intel.com/v1/dl/getContent/682353", "https://cdrdv2.intel.com/v1/dl/getContent/682354",
         "https://cdrdv2.intel.com/v1/dl/getContent/682355", "https://cdrdv2.intel.com/v1/dl/getContent/682356",
         "https://cdrdv2.intel.com/v1/dl/getContent/682357", "https://cdrdv2.intel.com/v1/dl/getContent/682358",
         "https://cdrdv2.intel.com/v1/dl/getContent/682359", "https://cdrdv2.intel.com/v1/dl/getContent/682360"]

dir_name = "resources"
file_name = dir_name + "/"+ "week{n}.zip".format(n=week_number)

def unzip(file_name):
    with ZipFile(file_name, "r") as zipObj:
        zipObj.extractall()
        print ("You can move to Class {n}.".format(n=week_number))

def on_button_clicked(b):
    with output:
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        
        with open(file_name, "wb") as file:
            response = requests.get(links[week_number-1], stream=True)
            total_length = response.headers.get("content-length")

            if total_length is None: # no content length header
                file.write(response.content)
            else:
                total_length = int(total_length)
                chunk_size = 4096
                
                min_value = 0
                max_value = int(total_length/chunk_size)
                description = "Downloading:"

                progressbar = widgets.IntProgress(min=min_value, max=max_value, description=description)
                display(progressbar)
                
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progressbar.value += 1
        
        unzip(file_name)
                

if Path(file_name).is_file():
    print("File exist")
    unzip(file_name)
else:
    button = widgets.Button(description="Download")
    output = widgets.Output()

    display(button, output)
    
    button.on_click(on_button_clicked)
