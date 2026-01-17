import numpy as np

class MusicEmbedder:
    """
    Converts a sequence of notes into a fixed-size vector (embedding).
    This handles the 'Feature Extraction' part of the pipeline.
    """
    def __init__(self):
        # We are using 4 features for this simple embedding
        self.embedding_dim = 4

    def embed(self, notes):
        """
        Creates an embedding vector from a list of notes.
        
        Args:
            notes (list): List of note dictionaries.
            
        Returns:
            np.array: A 1D array representing the musical idea.
        """
        if not notes:
            # Return a zero vector if there are no notes
            return np.zeros(self.embedding_dim)

        # 1. Extract Pitches
        # We pull out all the pitch values from the simplified note objects
        pitches = [n['pitch'] for n in notes]
        
        # 2. Extract Durations
        # We pull out all the duration values
        durations = [n['duration'] for n in notes]
        
        # --- Feature Calculation ---
        
        # Feature 1: Average Pitch
        # capturing the general register (high vs low)
        avg_pitch = np.mean(pitches)
        
        # Feature 2: Pitch Range
        # Capturing the melodic spread (wide vs narrow)
        pitch_range = np.max(pitches) - np.min(pitches)
        
        # Feature 3: Note Density (Rhythm)
        # Calculates notes per second. Higher means faster/busier.
        total_time = notes[-1]['start'] + notes[-1]['duration'] - notes[0]['start']
        if total_time > 0:
            notes_per_second = len(notes) / total_time
        else:
            notes_per_second = 0
            
        # Feature 4: Average Duration
        # Capturing if the piece is sustained (long notes) or staccato (short notes)
        avg_duration = np.mean(durations)
        
        # Combine features into a vector
        vector = np.array([avg_pitch, pitch_range, notes_per_second, avg_duration])
        
        # **Crucial Step**: Normalization
        # In real systems, we'd normalize across the whole dataset.
        # Here, we return the raw vector, but usually, embeddings are unit vectors
        # to make cosine similarity meaningful.
        # Let's simple L2 normalize it so simple dot products work well as similarity.
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
            
        return vector
