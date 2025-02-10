

from __future__ import absolute_import
from __future__ import print_function

import os


def __init_plugin__(app=None):
    '''
    Add an entry to the PyMOL "Plugin" menu
    '''
    from pymol.plugins import addmenuitemqt
    addmenuitemqt('Process SwissDock Plugin', run_plugin_gui)


# global reference to avoid garbage collection of our dialog
dialog = None

def run_plugin_gui():
    '''
    Open our custom dialog
    '''
    global dialog

    if dialog is None:
        dialog = make_dialog()

    dialog.show()

def make_dialog():
    # entry point to PyMOL's API
    from pymol import cmd

    # import functions
    from .modules import process_swissdock_out

    # pymol.Qt provides the PyQt5 interface, but may support PyQt4
    # and/or PySide as well
    from pymol.Qt import QtWidgets
    from PyQt5.QtWidgets import QFileDialog
    from pymol.Qt.utils import loadUi

    # create a new Window
    dialog = QtWidgets.QDialog()

    # populate the Window from our *.ui file which was created with the Qt Designer
    uifile = os.path.join(os.path.dirname(__file__), 'SwissDockwidget.ui')
    form = loadUi(uifile, dialog)

    # callback for the "Filter" button
    def run():
        # get form data
        dist = form.filter_dist.value()
        dirname = form.indir.text()
        outdir = form.outdir.toPlainText()
        residues = form.binding_residues.toPlainText()
        do_stats = form.doStats.isChecked()
        masterDir = form.masterDir.isChecked()


        if not masterDir:
            if dirname:
                process_swissdock_out.process_swissdock_out(dirname,outdir,do_stats,dist,residues)
            else:
                print('Error: No SwissDock output directory selected.')
        else:
            for item in os.listdir(dirname):
                full_path = os.path.join(dirname, item)
                if os.path.isdir(full_path):
                    print("Processing directory:", full_path)
                    process_swissdock_out.process_swissdock_out(full_path,outdir,do_stats,dist,residues)
                cmd.delete('all')
                cmd.reinitialize()
        

    # callback for the "Browse" button
    def browse_dirname():
        dirname = QFileDialog.getExistingDirectory(dialog, 'Select Directory')
        if dirname:
            form.indir.setText(dirname)

    # hook up button callbacks
    form.button_ray.clicked.connect(run)
    form.button_browse.clicked.connect(browse_dirname)
    form.button_close.clicked.connect(dialog.close)

    return dialog
