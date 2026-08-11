import sys
import os
import json

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieval.retriever import retrieve
from generation.llm_client import generate_answer

def run_evaluation():
    testset_path = os.path.join(os.path.dirname(__file__), "qa_testset.json")
    if not os.path.exists(testset_path):
        print("Testset not found.")
        return
        
    with open(testset_path, "r") as f:
        testset = json.load(f)
        
    results = []
    
    print("| Question | Retrieved Chunks | Answer Excerpt | Match Found |")
    print("|----------|------------------|----------------|-------------|")
    
    for item in testset:
        question = item["question"]
        expected_keywords = item["expected_answer_keywords"]
        
        chunks = retrieve(question, top_k=3)
        answer = generate_answer(question, chunks)
        
        chunk_count = len(chunks)
        
        match_found = any(kw.lower() in answer.lower() for kw in expected_keywords)
        match_str = "✅ Yes" if match_found else "❌ No"
        
        answer_excerpt = answer[:50].replace("\n", " ") + "..."
        
        print(f"| {question[:30]}... | {chunk_count} | {answer_excerpt} | {match_str} |")
        
if __name__ == "__main__":
    run_evaluation()
