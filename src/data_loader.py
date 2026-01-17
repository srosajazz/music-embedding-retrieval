import mido

def load_midi(file_path):
    """
    Loads a MIDI file and converts it into a simplified sequence of notes.
    
    Args:
        file_path (str): Path to the MIDI file.
        
    Returns:
        list: A list of dictionaries, where each dict represents a note 
              with 'pitch', 'start', 'duration', and 'velocity'.
    """
    # Load the MIDI file using mido
    mid = mido.MidiFile(file_path)
    
    notes = []
    
    # Track the current time in seconds
    current_time = 0.0
    
    # We need to track active notes to calculate duration
    # Dictionary mapping pitch -> start_time
    active_notes = {}
    
    # Iterate through all messages in the MIDI file
    # mid.play() yields messages with their delta time (time since last message)
    # This simplifies timing calculations significantly
    for msg in mid:
        # Update current time by adding the time delta of the message
        # msg.time is the time in seconds since the last message
        current_time += msg.time
        
        # Check if it's a 'note_on' message with velocity > 0 (start of a note)
        if msg.type == 'note_on' and msg.velocity > 0:
            # Record the start time for this pitch
            active_notes[msg.note] = {
                'start': current_time,
                'velocity': msg.velocity
            }
            
        # Check if it's a 'note_off' or 'note_on' with velocity 0 (end of a note)
        elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
            # If this pitch was active, we can now complete the note
            if msg.note in active_notes:
                start_info = active_notes.pop(msg.note)
                duration = current_time - start_info['start']
                
                # Append the complete note to our simplified list
                notes.append({
                    'pitch': msg.note,           # MIDI note number (0-127)
                    'start': start_info['start'], # Start time in seconds
                    'duration': duration,        # Duration in seconds
                    'velocity': start_info['velocity'] # Volume/Intensity
                })
                
    # Sort notes by start time just to be sure
    notes.sort(key=lambda x: x['start'])
    
    return notes
