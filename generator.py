# generator.py
class Generator:
    def __init__(self):
        # Placeholder: In real use, integrate AI model here
        self.generator = lambda prompt, max_new_tokens=350: [{"generated_text": f"Simulated summary for: {prompt}"}]

    def _clean_response(self, text):
        return text.strip()

    def extract_text(self, file_path):
        if file_path.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                return [{"filename": file_path.split("/")[-1], "content": f.read()}]
        elif file_path.lower().endswith(".pdf"):
            try:
                import PyPDF2
                text = ""
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                return [{"filename": file_path.split("/")[-1], "content": text}]
            except Exception as e:
                return [{"filename": file_path.split("/")[-1], "content": f"Could not read PDF: {e}"}]
        else:
            return [{"filename": file_path.split("/")[-1], "content": ""}]

    def generate_answer(self, query, docs, word_limit=None, bullet_points=False):
        """
        query: string like "summarize"
        docs: list of dicts with keys ['filename', 'content']
        word_limit: maximum words in summary (None means default length)
        bullet_points: if True, format summary in bullets
        """
        # Combine content for summarization
        combined_context = "\n".join([doc['content'] for doc in docs])
        prompt = f"{query}: {combined_context}"

        response = self.generator(prompt)[0]['generated_text']
        summary = self._clean_response(response)

        # Limit summary by word count if word_limit is specified
        if word_limit:
            words = summary.split()
            summary = " ".join(words[:word_limit])

        # Convert to bullet points if requested
        if bullet_points:
            summary_lines = summary.split(". ")
            summary = "\n- " + "\n- ".join([line.strip() for line in summary_lines if line.strip()])

        return summary, [doc['filename'] for doc in docs]

