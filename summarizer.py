def summarize_text(text, max_sentences=3):
    """
    Simple summarizer: returns the first few sentences from the text.
    In production, replace with an NLP-based summarizer.
    """
    if not text:
        return "No content to summarize."

    sentences = text.split(".")
    summary = ". ".join(sentences[:max_sentences]).strip()

    if not summary.endswith("."):
        summary += "."

    return summary
