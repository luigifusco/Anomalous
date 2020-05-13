def get_notes():
    with open('data/notes.txt') as file:
        notes = [line for line in file]

    return notes


def get_filelist():
    return [filename.split('.')[0] for filename in glob.glob('data/files/*.dat')]