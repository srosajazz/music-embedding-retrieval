from midiutil import MIDIFile
import random
import os

def generate_random_midi(filename, style="random"):
    """
    Generates a synthetic MIDI file with a specific musical style using midiutil.
    
    Args:
        filename (str): Output filename.
        style (str): 'happy', 'sad', 'chaotic'.
    """
    # Create MIDIFile object with 1 track
    # adjust_origin=False means time 0 is the start of the track
    mid = MIDIFile(1, adjust_origin=False)
    
    track = 0
    time = 0
    
    # Defaults
    duration = 1 # beat
    volume = 100
    
    # Configure style parameters
    if style == "happy":
        # Major key, higher pitch, faster
        scale = [60, 62, 64, 65, 67, 69, 71, 72] # C Major
        base_pitch = 72 # Start high (C5)
        tempo = 120
        program = 0 # Acoustic Grand Piano
    elif style == "sad":
        # Minor key, lower pitch, slower
        scale = [60, 62, 63, 65, 67, 68, 70, 72] # C Minor
        base_pitch = 48 # Start low (C3)
        tempo = 70
        program = 40 # Violin
    else: # chaotic
        scale = list(range(40, 90)) # Chromatic
        base_pitch = 60
        tempo = 120
        program = 11 # Vibraphone
        
    # Add Track Name and Tempo
    mid.addTrackName(track, time, f"{style.capitalize()} Song")
    mid.addTempo(track, time, tempo)
    
    # Add Program Change (Instrument)
    mid.addProgramChange(track, channel=0, time=time, program=program)
    
    # Generate a random melody
    # We generate 20 notes
    for i in range(20):
        # Pick a random note from the scale
        note_idx = random.randint(0, len(scale)-1)
        pitch = scale[note_idx]
        
        # Add some variation to velocity
        vel = volume + random.randint(-10, 10)
        
        # Duration customization
        dur = duration if style != "chaotic" else random.uniform(0.5, 2.0)
        
        # Add note
        mid.addNote(track, channel=0, pitch=pitch, time=time, duration=dur, volume=vel)
        
        # Move time forward
        time += dur
        
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save the file
    with open(filename, "wb") as output_file:
        mid.writeFile(output_file)
        
    print(f"Generated {style} MIDI: {filename}")
