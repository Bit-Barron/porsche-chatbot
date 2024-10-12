import chromadb
from chromadb.utils import embedding_functions
import os

def create_chroma_collection():
    client = chromadb.Client()
    # Verwenden Sie hier die gewünschte Embedding-Funktion
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.create_collection(name="porsche_qa", embedding_function=embedding_function)
    return collection

def import_data(collection, file_path, category):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    qa_pairs = content.split('----------')
    
    for i, pair in enumerate(qa_pairs):
        if 'Frage:' in pair and 'Antwort:' in pair:
            question = pair.split('Frage:')[1].split('Antwort:')[0].strip()
            answer = pair.split('Antwort:')[1].strip()
            collection.add(
                documents=[answer],
                metadatas=[{"category": category, "question": question}],
                ids=[f"{category}-{i}"]
            )

def main():
    collection = create_chroma_collection()
    
    files = {
        'connect': 'connect_output.txt',
        'e-mobility': 'e-mobility_output.txt',
        'my-porsche': 'my-porsche_output.txt'
    }
    
    for category, file_name in files.items():
        if os.path.exists(file_name):
            print(f"Importing data from {file_name}...")
            import_data(collection, file_name, category)
        else:
            print(f"File {file_name} not found. Skipping.")
    
    print("Data import completed.")

    # Beispielabfrage
    results = collection.query(
        query_texts=["Wie kann ich mein Porsche Connect aktivieren?"],
        n_results=2
    )
    print("Beispielabfrage Ergebnisse:")
    for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
        print(f"Frage: {metadata['question']}")
        print(f"Antwort: {doc}")
        print("---")

if __name__ == "__main__":
    main()