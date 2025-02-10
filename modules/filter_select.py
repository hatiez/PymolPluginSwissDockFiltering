from pymol import cmd
def filter_selected_molecules(object_pattern, selection_name, write_results=False):
    """
    Remove objects that do not contain any atom that is part of the specified selection.

    Example usage: "filter_selected_molecules("seed.*", "bind_site")"

    Parameters:
    object_pattern (str): The pattern for the objects to be removed (e.g "seed.*").
    selection_name (str): The name of the selection to check against.
    write_results: write which objects are kept into a text file (default = False)

    Returns:
    None
    """
    # open file to write results
    if write_results:
        filename = "filtered_for_" + selection_name
        file = open(filename, 'w')
    # Iterate over the objects matching the specified pattern
    for obj in cmd.get_object_list(object_pattern):
        # Check if any atom of the object is in the specified selection
        cmd.select("tmp", f"{obj} and {selection_name}")
        if cmd.count_atoms("tmp") == 0:
            cmd.delete(obj)
        # if requested, save object if not deleted
        elif write_results:
            file.write(obj+"\n")

    # Delete the temporary selection
    cmd.delete("tmp")
    if write_results:
        file.close()


