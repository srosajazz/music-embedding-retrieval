import os
import glob
from src.utils import generate_random_midi
from src.data_loader import load_midi
from src.embedder import MusicEmbedder
from src.retriever import MusicRetriever

def main():
    """
    Main execution flow for the Mini Music Embedding + Retrieval System.
    """
    print("--- Mini Music Embedding + Retrieval System ---")
    
    # 1. Generate Synthetic Data
    # We create a 'database' of music with known styles.
    print("\n[1] Generating Synthetic MIDI Data...")
    midi_dir = "midi_data"
    os.makedirs(midi_dir, exist_ok=True)
    
    # Generate 5 Happy songs and 5 Sad songs
    dataset_files = []
    
    for i in range(5):
        filename = f"{midi_dir}/happy_{i}.mid"
        generate_random_midi(filename, style="happy")
        dataset_files.append(filename)
        
    for i in range(5):
        filename = f"{midi_dir}/sad_{i}.mid"
        generate_random_midi(filename, style="sad")
        dataset_files.append(filename)
        
    print(f"Generated {len(dataset_files)} MIDI files.")
    
    # 2. Initialize System
    print("\n[2] Initializing Embedder and Retriever...")
    embedder = MusicEmbedder()
    retriever = MusicRetriever()
    
    # 3. Process Data (Load -> Embed -> Index)
    print("\n[3] Processing Dataset...")
    for file_path in dataset_files:
        # Load the MIDI notes
        notes = load_midi(file_path)
        
        # Create the embedding vector
        vector = embedder.embed(notes)
        
        # Add to the retrieval index
        retriever.add_item(file_path, vector)
        
        # Print a small debug info
        print(f"Indexed {os.path.basename(file_path)}: Vector {vector}")
        
    # 4. Perform Retrieval
    print("\n[4] Performing Retrieval Demos...")
    
    # Demo A: Query with a Happy song (should find other Happy songs)
    print("\n--- Query: Happy Song (happy_0.mid) ---")
    query_file = f"{midi_dir}/happy_0.mid"
    query_notes = load_midi(query_file)
    query_vector = embedder.embed(query_notes)
    
    results = retriever.search(query_vector, k=5)
    
    print(f"Query Vector: {query_vector}")
    print("Top 5 Results:")
    for rank, (file_id, score) in enumerate(results, 1):
        print(f"{rank}. {os.path.basename(file_id)} (Similarity: {score:.4f})")
        
    # Demo B: Query with a Sad song
    print("\n--- Query: Sad Song (sad_0.mid) ---")
    query_file = f"{midi_dir}/sad_0.mid"
    query_notes = load_midi(query_file)
    query_vector = embedder.embed(query_notes)
    
    results = retriever.search(query_vector, k=5)
    
    print(f"Query Vector: {query_vector}")
    print("Top 5 Results:")
    for rank, (file_id, score) in enumerate(results, 1):
        print(f"{rank}. {os.path.basename(file_id)} (Similarity: {score:.4f})")
        
    # 5. Analysis
    print("\n[5] Trade-offs Analysis")
    print("Why this works: We handcrafted features that capture 'Mood' (Tempo/Pitch).")
    print("Where it fails: Note sequences with same stats but different melodies are seen as identical.")
    print("Trade-offs: Handcrafted is interpretable but rigid vs Learned (Neural) which is black-box but powerful.")

if __name__ == "__main__":
    main()
