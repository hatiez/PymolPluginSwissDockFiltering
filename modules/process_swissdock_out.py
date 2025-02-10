#!/usr/bin/env python3
"""
PyMol toolkit to process SwissDock outputs of letermovir / ul56 dockings.

Author: Hans Tietze
Contact: hanstietze@gmail.com

usage:
    1. import the toolkit from the pymol GUI, e.g. "run scripts/process_swissdock_out.py"
    2. or; directly open the toolkit from the command line, e.g "pymol toolkit/process_swissdock_out.py"
    
"""

import os, zipfile, inspect
from pymol import cmd
import pandas as pd
import numpy as np

### IMPORTING FUNCTIONS ###

"""# get directory of the current script
scripts_directory = os.path.dirname(inspect.getfile(inspect.currentframe()))

# load functions from these scripts
cmd.run(f"{scripts_directory}/loaddir.py")
cmd.run(f"{scripts_directory}/split_clusters_pdb.py")
cmd.run(f"{scripts_directory}/filter_seedfiles.py")
cmd.run(f"{scripts_directory}/extract_deltaG.py")"""

from . import loaddir, split_clusters_pdb, filter_select, extract_deltaG

### DEFINING FUNCTIONS ###
def count_residues(object_name):
    """
    Count the number of residues in the given protein object.

    Args:
    - object_name (str): The name of the protein object in PyMOL.

    Returns:
    - int: The number of residues.
    """
    # Select all residues in the protein object
    cmd.select("all_residues", f"{object_name} and polymer.protein")

    # Get the list of unique residue identifiers (chain + residue number)
    residue_list = cmd.get_model("all_residues").get_residues()

    # Count the unique residues
    residue_count = len(set(residue_list))

    return residue_count

def update_residue_counts(dir):
    """
    Updates counts of residues within 5 Angstroms of each molecule named 'entry_*',
    specifically focusing on residues in the protein named "target".

    Arguments:
        - dir: Directory where the PDB files are located.

    Returns:
        A pandas DataFrame with residue counts.
    """
    nresidues = count_residues("target")

    # Initialize the DataFrame
    df = pd.DataFrame({
        'residue': range(nresidues+1),
        'count': np.zeros(nresidues+1, dtype=int)
    })

    # Iterate over molecules named 'entry_*'
    for obj in cmd.get_object_list('all'):
        if obj.startswith('entry_'):
            # Select residues within 5 Angstroms of the current molecule, but only in the "target" protein
            #cmd.select('nearby_residues', f'byresidue (br. {obj} within 5 of {obj} and target)')
            cmd.select("nearby_residues", f"{obj} around 5 and target")
            
            # Get residue numbers
            model = cmd.get_model("nearby_residues")

            residues = set()  # Using a set to avoid duplicates
            for atom in model.atom:
                residues.add(int(atom.resi))
            residues = sorted(list(residues))  # Convert to a sorted list

            for resi in residues:
                if resi <= nresidues+1:
                    df.loc[resi, 'count'] += 1

            # Deselect for the next iteration
            cmd.deselect()

    return df

# Helper functions #
def unzip_folder(zip_file_path, extract_folder_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder_path)

def dG_to_Kd(dG):
    # declare constants
    R = 8.314
    T = 310.15
    KcaltoJ = 4184

    return np.exp(dG * KcaltoJ / (T * R)) * 1000000

def do_stats(infile,dir,outdir):
    """
    This function takes the deltaG output csv file and computes the mean deltaG as well as Kd values.
    Arguments:
        - infile: input .csv file written in the main function
        - outdir: the out directory, to which to write the results

    """


    # Read infile
    df = pd.read_csv(infile,names=["BM","dG","fullFitness"])

    # Compute column of Kd values
    df['Kd'] = df['dG'].apply(dG_to_Kd)

    # get number of BMs
    n = df.shape[0]

    # write this to new csv file
    df.to_csv(infile, index=False)

    # Compute mean values and errors
    dG = df["dG"].mean()
    dGSD = df["dG"].std()

    fullFitness = df["fullFitness"].mean()
    fullFitnessSD = df["fullFitness"].std()

    Kd = dG_to_Kd(dG)
    # error is found using gaussian propagation of uncertainty
    Kderr = (dG_to_Kd(dG+dGSD)-dG_to_Kd(dG-dGSD))/2

    # results are written to .txt file
    with open(f"{dir}/{outdir}/stats.txt", 'w') as file:
    # Write the text to the file
        file.write(f"n = {n}\ndG = {dG}\ndG_SD = {dGSD}\nfullFitness = {fullFitness}\nfullFitness_SD = {fullFitnessSD}\nKd = {Kd}\nKd_err = {Kderr}")

# Main function #
def process_swissdock_out(dir,outdir,dostats = True, filter_distance = 5,binding_residues=""):
    """
    This function takes a Swissdock output, loads all binding modes into pymol, then filters out any binding modes which
    are not within 5 (or other) Angstroms from the binding site residues. The deltaG values of all these binding
    modes are written into a .csv file into the outdir. Statistical processing of these results will be done and written to a .txt file. 

    Arguments: 
        - dir: an unzipped output folder from swissdock. The function can be run from an empty PyMol session. All files of
        interest will be opened automatically.
        - outdir: name of output folder, to which the output files will be written
        - filter_distance (optional): distance (in Angstrom) used for filtering out binding modes (default = 5).
        - binding_residues (optional): a set of residues to be used as binding site for filtering results (using regular pymol 
        formatting for making selections). If none are given, the usual are used (240+243+247+250+325+328+329+332+336+244+245
        +246+333+337).
    
    Returns:
        - none.
        - writes a .csv file to the given directory

    example usage: process_swissdock_out("swissdock_out/WT","deltaG_out","240")

    cd Documents/Uni/project_work/C325Y/
    run scripts/process_swissdock_out.py
    process_swissdock_out("swissdock_out_LetermovirZinc_reference/November_second/C325Y","deltaG_out_C325Y")
    
    """
    cmd.delete("all")
    cmd.load(f"{dir}/target.pdb")
    
    # create output directory
    if not os.path.exists(f"{dir}/{outdir}"):
        os.makedirs(f"{dir}/{outdir}")

    # split cluster file into multiple
    split_clusters_pdb.split_clusters(f"{dir}/clusters.dock4.pdb", f"{dir}/{outdir}/split_pdb_clusters")

    # then load them all
    loaddir.load_files(f"{dir}/{outdir}/split_pdb_clusters/*.pdb")

    if len(binding_residues)!=0:
        # Select the specified residues
        cmd.select("bind_site", f"resi {binding_residues}")

        # Create a selection around the specified residues
        cmd.select("around_bind_site", "bind_site around 5")

        # Remove any target protein atoms from the selection
        cmd.select("around_bind_site", "around_bind_site and not byobject target")

        # Delete any BMs which do not have atoms within the selection
        filter_select.filter_selected_molecules("entry_*", "around_bind_site")

        residue_counts_df = update_residue_counts(dir)
        residue_counts_df.to_csv(f"{dir}/{outdir}/binding_resdues.csv", index=False)

    # extract deltaG values for the remaining BMs and write to file
    extract_deltaG.extract_deltaG(f"{dir}/{outdir}/split_pdb_clusters",f"{dir}/{outdir}/allValues.csv")

    if dostats:
        do_stats(f"{dir}/{outdir}/allValues.csv",dir,outdir)

cmd.extend('process_swissdock_out', process_swissdock_out)

