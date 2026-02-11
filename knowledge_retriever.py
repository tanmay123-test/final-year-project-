import json
import os
from sentence_transformers import SentenceTransformer, util
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(BASE_DIR, "medical-knowledge.json")

print("📚 Loading knowledge base from:", KB_PATH)

if not os.path.exists(KB_PATH):
    raise FileNotFoundError(f"❌ medical-knowledge.json not found at {KB_PATH}")

with open(KB_PATH, "r", encoding="utf-8") as f:
    KNOWLEDGE = json.load(f)

# 🧠 Load semantic model once
print("🧠 Loading sentence-transformers model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Pre-embed all knowledge entries for fast matching
knowledge_embeddings = []
for entry in KNOWLEDGE:
    # Combine keywords for better semantic representation
    text = " ".join(entry["keywords"])
    embedding = model.encode(text, convert_to_tensor=True)
    knowledge_embeddings.append(embedding)

print(f"✅ Pre-computed embeddings for {len(KNOWLEDGE)} medical conditions")

def find_specialist_from_knowledge(user_text: str) -> dict:
    """
    Semantic RAG matcher using sentence transformers
    Finds best matching specialist using cosine similarity
    """
    
    # Embed user symptoms
    user_embedding = model.encode(user_text, convert_to_tensor=True)
    
    # Calculate cosine similarity with all knowledge entries
    similarities = []
    for knowledge_embedding in knowledge_embeddings:
        similarity = util.cos_sim(user_embedding, knowledge_embedding).item()
        similarities.append(similarity)
    
    # Find best match
    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]
    
    # Only return match if similarity is above threshold
    if best_score > 0.3:  # Threshold for semantic similarity
        best_match = KNOWLEDGE[best_idx]["specialist"]
        print(f"🎯 Semantic match: {best_match} (similarity: {best_score:.3f})")
    else:
        best_match = "General Physician"
        print(f"🎯 Low similarity ({best_score:.3f}), defaulting to General Physician")
    
    return {"specialist": best_match, "similarity": best_score}
