# main.py
import os
from generator import Generator

UPLOADS_FOLDER = "uploads"
SUMMARY_FOLDER = "summaries"

os.makedirs(SUMMARY_FOLDER, exist_ok=True)

def list_uploaded_files():
    files = os.listdir(UPLOADS_FOLDER)
    return [f for f in files if os.path.isfile(os.path.join(UPLOADS_FOLDER, f))]

def save_summary(filename, summary):
    save_path = os.path.join(SUMMARY_FOLDER, f"summary_{filename}")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"✅ Summary saved to {save_path}")

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
        print("2. Summarize specific files")
        print("3. View previous summaries")
        print("4. Exit")

        choice = input("Enter 1, 2, 3, or 4: ").strip()

        if choice == "1":
            selected_files = files
        elif choice == "2":
            file_input = input("Enter file numbers separated by commas (e.g., 1,3,5): ")
            try:
                indices = [int(i.strip())-1 for i in file_input.split(",")]
                selected_files = [files[i] for i in indices if 0 <= i < len(files)]
            except:
                print("❌ Invalid input.")
                continue
        elif choice == "3":
            summaries = os.listdir(SUMMARY_FOLDER)
            if summaries:
                print("\n📂 Existing summaries:")
                for s in summaries:
                    print(s)
            else:
                print("⚠️ No summaries found.")
            continue
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")
            continue

        # Ask for summary format
        print("\nChoose summary format:")
        print("1. Paragraph")
        print("2. Bullet Points")
        summary_style = input("Enter 1 or 2: ").strip()
        summary_style = "paragraph" if summary_style == "1" else "bullet"

        # Ask for word limit if paragraph
        word_limit = None
        if summary_style == "paragraph":
            word_input = input("Enter maximum number of words for the summary (e.g., 100): ").strip()
            try:
                word_limit = int(word_input)
            except:
                print("⚠️ Invalid input. Using full summary.")

        # Process selected files
        for file in selected_files:
            file_path = os.path.join(UPLOADS_FOLDER, file)
            print(f"\n📄 Processing: {file}")
            try:
                docs = generator.extract_text(file_path)
            except Exception as e:
                print(f"❌ Failed to read file: {e}")
                continue

            summary, sources = generator.generate_answer("Summarize", docs)

            # Apply word limit if specified
            if word_limit:
                words = summary.split()
                if len(words) > word_limit:
                    summary = " ".join(words[:word_limit]) + "..."

            # Print in selected format
            print("\n📌 Summary:")
            if summary_style == "bullet":
                for sentence in summary.split('. '):
                    if sentence.strip():
                        print(f"- {sentence.strip()}.")
            else:
                print(summary)

            print("📎 Sources:", ", ".join(sources))
            save_summary(file, summary)

if __name__ == "__main__":
    main()

