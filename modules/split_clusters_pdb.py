import os

def split_clusters(infile, outdir):
    """
    Splits a PDB file into separate entries whenever a "TER" line is encountered.

    Example usage: split_clusters("input.pdb", "output_directory")

    Parameters:
    infile (str): The path to the input PDB file.
    outdir (str): The directory where the split PDB entries will be saved.

    Returns:
    None
    """

    # Create the output directory if it does not exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Read all lines from the input file
    with open(infile, 'r') as file:
        lines = file.readlines()

    entry_count = 0  # Counter for naming output files
    entry_lines = []  # List to store lines of the current entry

    # Iterate through each line in the input file
    for line in lines:
        # Collect lines until a "TER" line is encountered
        if not line.startswith('TER'):
            entry_lines.append(line)
        else:
            # Define the output filename for the current entry
            entry_filename = f"{outdir}/entry_{entry_count}.pdb"

            # If there are collected lines, write them to the output file
            if len(entry_lines) != 0:
                with open(entry_filename, 'w') as entry_file:
                    entry_file.writelines(entry_lines)
            
            # Increment the entry counter and reset the list for the next entry
            entry_count += 1
            entry_lines = []
