from midiutil import MIDIFile

def create_test_midi():
    degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 120   # In BPM
    volume   = 100  # 0-127

    # One track, defaults to format 1 (tempo track is created automatically)
    MyMIDI = MIDIFile(1)  
    MyMIDI.addTempo(track, time, tempo)

    for i, pitch in enumerate(degrees):
        MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

    with open("midiutil_test.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
    print("Created midiutil_test.mid")

if __name__ == "__main__":
    create_test_midi()
