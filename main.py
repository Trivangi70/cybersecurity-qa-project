# main.py
from generator import Generator  # make sure generator.py exists
from documents import load_docs  # assuming you have a function to load docs

def main():
    # Load your documents
    docs = load_docs()  # replace with your actual doc-loading function
    generator = Generator()  # initialize your answer generator

    print("Device set to use mps:0")
    print("Ask your questions (type 'exit' to quit):")

    while True:
        query = input("> ").strip()  # remove leading/trailing spaces
        if query.lower() == "exit":
            print("Exiting...")
            break  # exit the program
        if not query:  # skip empty input
            continue

        try:
            answer, sources = generator.generate_answer(query, docs)
            print("\nAnswer:", answer)
            print("Sources:", sources, "\n")
        except Exception as e:
            print("Error generating answer:", e, "\n")

if __name__ == "__main__":
    main()
