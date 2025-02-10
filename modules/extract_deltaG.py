import os
import re
from pymol import cmd

def extract_deltaG(directory, outfile ,object_pattern="entry_[0-9]+"):
    """
    Take all objects matching "object_pattern" from current pymol session and scan the directory for matches.
    If a matching file is found, it is opened and the deltaG value extracted and written to the outfile.

    This function assumes that the directory contains .crd files (the default output in the SwissDock "clusters" 
    folder). By default, these files are named "seed.[0-9]+.crd" (regex expression).

    Parameters:
    directory: name of the directory which is searched (e.g: "swissdock_out/clusters")
    outfile: name given to output file (.csv suffix recommended)
    object_pattern: pattern of the name of objects in pymol session for which to search folder (default = "seed.*)

    Returns:
    none
    """
    # opening the output filestream
    outfile = open(outfile, 'w')

    # Finding all objects in the current PyMOL session that match the pattern
    object_set = {obj for obj in cmd.get_object_list() if re.match(object_pattern, obj)}

    #print(object_set)
    
    # Opening the directory
    with os.scandir(directory) as entries:
        for entry in entries:
            # extract the portion of current file which is to be searched for in the object set
            current_filematch = re.search(object_pattern, entry.name)
            if entry.is_file() and current_filematch: 
                # search the set of objects for the current filename
                if current_filematch.group(0) in object_set:
                    with open(entry.path, 'r') as infile:
                        # Loop over each line in the file
                        for line in infile:
                            # Check if the line is the fullFitness line
                            if re.match("^REMARK  FullFitness:", line):
                                fullFit = line[21:]
                            #check if line is the deltaG line
                            if re.match("^REMARK  deltaG:", line):
                                outfile.write(f"{current_filematch.group(0)},{line[16:].rstrip()},{fullFit}")
                    infile.close()

    outfile.close()

                            
                