import mido, time, threading, keyboard

class app:
    def __init__(self):
        self.lock = threading.Lock()
        self.notes = []

    def addNote(self, msg):
        with self.lock:
            self.notes.append(msg)

    def clearnotes(self):
        with self.lock:
            self.notes = []

    def getNotes(self):
        with self.lock:
            return self.notes.copy()

def initMidiThread(app):
    print("Midi Thread Started")
    with mido.open_input('P-Series 0') as inport:
        for msg in inport:
            app.addNote(msg)

def midi_to_note_name(midi_number):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    

    note_index = midi_number % 12
    octave = midi_number // 12 - 1  
    
    note_name = note_names[note_index] #+ str(octave)
    
    return note_name

def main():
    myapp = app()
    statTable = {}
    mdThread = threading.Thread(target=initMidiThread, args=(myapp,))
    mdThread.daemon = True  # This ensures the thread will exit when the main program exits
    mdThread.start()

    running = True
    while running:
        if len(myapp.getNotes()) > 0:
            for note in myapp.getNotes():
                if note.type == 'note_on':
                    # Sans l'octave pour le comptage
                    translatedNote = midi_to_note_name(note.note)
                    statTable[translatedNote] = statTable.get(translatedNote,0) + 1
            myapp.clearnotes()
        time.sleep(0.01)
        if keyboard.is_pressed('q'):
            running = False
    print("Note Statistics:")
    for note in statTable:
        print(f"{note}: {statTable[note]}")

if __name__ == '__main__':
    main()
