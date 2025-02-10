SwissDock Processing Plugin for PyMOL
# Overview
This PyMOL plugin is designed to process, filter, and analyze SwissDock docking results. It automates the extraction of ligand binding poses, filters them based on their distance to specific binding residues, and extracts binding free energy values (∆G). The plugin also calculates statistical summaries and can process multiple docking output folders at once.

The plugin is useful for binding site analysis, ligand pose filtering, and quantifying docking interactions. It was developed for analyzing Letermovir docking results with the UL56 protein but can be applied to other docking studies as well.

# Features
- Organizes SwissDock results by splitting docking output files into separate entries.
- Filters ligand poses based on their distance to selected binding site residues.
- Extracts ∆G values (binding free energy) and dissociation constant (Kd).
- Performs statistical analysis, including mean and standard deviation of ∆G values.
- Processes multiple docking outputs in batch mode.
- Generates residue interaction data, counting how often each residue is within 5Å of a ligand.

#Installation
Step 1: Install the Plugin in PyMOL
Open PyMOL.
Go to Plugins > Plugin Manager.
Click "Install New Plugin" and select "Choose file...".
Choose the file __init__.py from the plugin folder.
Step 2: Install Pandas
The plugin requires Pandas (a Python library). Install it by typing this in the PyMOL terminal:
pip install pandas

# How to Use the Plugin
1. Open the Plugin
In PyMOL, go to Plugins > Process SwissDock Plugin.
2. Select Input and Output Folders
Input Directory: Select the folder containing SwissDock output files.
Output Name: Choose a folder name where processed results will be saved.
3. Choose Filtering Options
Binding Residues: List of amino acids that define the binding site. Only ligand poses close to these residues will be kept.
Filter Distance: The cutoff distance (in Angstroms) for filtering ligand poses. The default is 5 Å.
Do Statistics: If enabled, the plugin will calculate the average ∆G value, Kd, and other statistics.
4. Process Multiple Docking Results (Optional)
If you want to process multiple SwissDock outputs at once, select Master Directory and choose a folder that contains multiple SwissDock output folders.
5. Run the Plugin
Click "Run" to start processing.
The processed output will be saved in the output folder inside the SwissDock results directory.

# Output Files
- Filtered PDB files: Ligand poses that passed the filtering step.
- allValues.csv: A file containing extracted ∆G values for all filtered ligand poses.
- stats.txt: If statistics are enabled, this file contains the mean ∆G, standard deviation, and Kd values.
- binding_residues.csv: If binding residues are specified, this file lists residues and how often they appear within 5 Å of the ligand.

# Functions Included in the Plugin
Splitting Docking Clusters
The plugin can split SwissDock PDB files into separate entries. This helps in processing individual docking poses separately.

Extracting ∆G and FullFitness
The plugin scans SwissDock output files to extract binding energy values (∆G) and writes them to a CSV file.

Filtering Ligand Poses
The plugin removes ligand conformations that are not close to the specified binding site residues. This ensures that only relevant docking poses are analyzed.

Processing Multiple Docking Results
The plugin allows processing multiple SwissDock output folders in one go if a master directory containing multiple outputs is selected.

# Example Usage

Single Docking Analysis
- Open PyMOL.
- Load the plugin.
- Select a SwissDock output folder as input.
- Set an output name and choose filtering options.
- Click "Run" to process the results.
- Find the processed results in the output directory.

Batch Processing of Multiple Docking Results
- Open the plugin.
- Select a Master Directory that contains multiple SwissDock outputs.
- Set the output name and filtering options.
- Click "Run" to process all docking outputs automatically.