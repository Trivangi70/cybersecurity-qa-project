from generator import AnswerGenerator  # updated to use your existing class
from file_loader import load_file
from summarizer import summarize_text
import os

def load_docs():
    """Load all .txt and .pdf files from the repo root into a list."""
    docs = []
    files = [f for f in os.listdir('.') if f.endswith(('.txt', '.pdf'))]

    for file_path in files:
        try:
            content = load_file(file_path)
            docs.append({
                "filename": file_path,
                "content": content,
                "summary": summarize_text(content)
            })
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return docs

def main():
    # Load your documents
    docs = load_docs()
    generator = AnswerGenerator()  # initialize your answer generator

    print("Device set to use mps:0")
    print("Ask your questions (type 'exit' to quit):")

    while True:
        query = input("> ").strip()
        if query.lower() == "exit":
            print("Exiting...")
            break
        if not query:
            continue

        try:
            answer, sources = generator.generate_answer(query, docs)
            print("\nAnswer:", answer)

            if sources:
                print("\nSources:")
                for i, src in enumerate(sources, start=1):
                    print(f"{i}. {src['filename']} — {src['summary']}")
            print()

        except Exception as e:
            print(f"Error generating answer: {e}\n")

if __name__ == "__main__":
    main()

