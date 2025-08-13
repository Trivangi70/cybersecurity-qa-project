import os
from generator import Generator

UPLOADS_FOLDER = "uploads"

def list_uploaded_files():
    files = os.listdir(UPLOADS_FOLDER)
    return [f for f in files if os.path.isfile(os.path.join(UPLOADS_FOLDER, f))]

def main():
    generator = Generator()

    while True:
        files = list_uploaded_files()
        if not files:
            print("⚠️ No files found in uploads/ folder.")
            return

        print("\n📂 Files in uploads/:")
        for idx, file in enumerate(files, start=1):
            print(f"{idx}. {file}")

        print("\nChoose an option:")
        print("1. Summarize ALL files")
        print("2. Summarize a specific file by name")
        print("3. Exit")

        choice = input("Enter 1, 2, or 3: ").strip()

        if choice == "1":
            selected_files = files
        elif choice == "2":
            file_name = input("Enter exact file name from the list above: ").strip()
            if file_name not in files:
                print("❌ File not found.")
                continue
            selected_files = [file_name]
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")
            continue

        for file in selected_files:
            file_path = os.path.join(UPLOADS_FOLDER, file)
            print(f"\n📄 Processing: {file}")
            text = generator.extract_text(file_path)
            summary, sources = generator.generate_answer("summarize", text)
            print("\n📌 Summary:")
            print(summary)
            print("\n📎 Sources:", sources)

if __name__ == "__main__":
    main()
