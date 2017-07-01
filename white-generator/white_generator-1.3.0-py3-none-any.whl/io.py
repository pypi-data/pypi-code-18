import uuid

_UUID_NAMESPACE = uuid.uuid1()

def read_notes(notes_filename):
    with open(notes_filename) as notes_file:
        note = ''
        for line in notes_file:
            if len(line.rstrip()) != 0:
                note += line.rstrip() + '\n'
            elif len(note.rstrip()) != 0:
                yield note.rstrip()
                note = ''

        if len(note.rstrip()) != 0:
            yield note.rstrip()

def generate_note_id(note):
    return str(uuid.uuid5(_UUID_NAMESPACE, note))
