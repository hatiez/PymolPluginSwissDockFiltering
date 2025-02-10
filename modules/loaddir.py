from pymol import cmd
import glob

def load_files(files):
  """
  load_files <files>

  loads multiple files (using filename globbing)
  into a multiple objects named as the files are (e.g. collection of
  downloaded PDB files).

  e.g. load_files prot_*.pdb
  """
  file_list = glob.glob(files)
  if file_list:
    file_list.sort()
    for i in file_list:
      cmd.load(i)
  else:
    print("No files found for pattern %s" % files)

cmd.extend('load_files',load_files)