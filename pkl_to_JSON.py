import faiss
import pickle
import json

# Load FAISS index
faiss_index_path = "index.faiss"  # Replace with your actual path
index = faiss.read_index(faiss_index_path)

# Load metadata from PKL file
pkl_file_path = "index.pkl"  # Replace with your actual path
with open(pkl_file_path, "rb") as f:
    metadata = pickle.load(f)  # Assuming it's a dictionary with text data

# Ensure metadata matches FAISS vectors
assert len(metadata) == index.ntotal, "Mismatch between metadata and FAISS index"

# Convert to JSONL format
jsonl_file_path = "output_data.jsonl"
with open(jsonl_file_path, "w") as jsonl_file:
    for i in range(index.ntotal):
        data_entry = metadata[i]  # Extract corresponding metadata
        json_line = {
            "input": data_entry.get("symptoms", ""),  # Replace with correct key
            "output": data_entry.get("treatment", "")  # Replace with correct key
        }
        jsonl_file.write(json.dumps(json_line) + "\n")

print(f"JSONL file saved at: {jsonl_file_path}")
