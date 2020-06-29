"""
Contains various utility functions
"""
import glob


def get_notes():
    """
    :return: a list containing all notes
    """
    with open('data/notes.txt') as file:
        notes = [line[0] for line in file]

    return notes


def get_filelist():
    """
    :return: a list containing all data filenames
    """
    return [filename.split('.')[0] for filename in glob.glob('data/files/*.dat')]
