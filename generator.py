def generate_answer(self, query, docs):
    if not query or not query.strip():
        return "No question entered. Please ask a question.", []

    if not docs:
        return "Sorry, I couldn't find relevant information.", None

    combined_context = "\n\n".join([doc['content'] for doc in docs[:5]])
    if len(combined_context) > 1000:
        combined_context = combined_context[:1000].rsplit('.', 1)[0] + '.'

    sources = [
        {
            "filename": doc['filename'],
            "summary": doc.get('summary', 'No summary available.')
        }
        for doc in docs[:5]
    ]

    prompt = (
        "You are an expert assistant. Use ONLY the context below to answer the question clearly and fully. "
        "Write 3 to 5 complete sentences without repeating phrases or tautologies. "
        "Do NOT add any information not found in the context. Avoid bullet points and repetition. End with a summary sentence.\n\n"
        f"Context:\n{combined_context}\n\n"
        f"Question: {query}\nAnswer:"
    )

    response = self.generator(prompt, max_new_tokens=350)[0]['generated_text']
    answer = self._clean_response(response)

    def _starts_with_verb(word):
        verbs = {"is", "are", "was", "were", "does", "do", "did", "has", "have", "had",
                 "can", "will", "shall", "should", "could", "would", "may", "might", "must"}
        return word.lower() in verbs

    words = query.split()
    question_key = words[0].lower() if words else ""

    answer_lower = answer.lower()
    if not answer_lower.startswith(question_key):
        if _starts_with_verb(question_key) or question_key in {"what", "why", "how", "when", "where", "who"}:
            answer = f"{query.capitalize()} {answer[0].lower() + answer[1:]}" if answer else f"{query.capitalize()}."
        else:
            answer = f"{query.capitalize()} is {answer[0].lower() + answer[1:]}" if answer else f"{query.capitalize()}."

    if len(answer.split()) < 40:
        prompt2 = (
            "Please elaborate on the following answer in 3 to 5 sentences, "
            "without repetition or bullet points:\n\n"
            f"Answer: {answer}\n\n"
            "Elaborated answer:"
        )
        response2 = self.generator(prompt2, max_new_tokens=350)[0]['generated_text']
        answer = self._clean_response(response2)

        answer_lower = answer.lower()
        if not answer_lower.startswith(question_key):
            if _starts_with_verb(question_key) or question_key in {"what", "why", "how", "when", "where", "who"}:
                answer = f"{query.capitalize()} {answer[0].lower() + answer[1:]}" if answer else f"{query.capitalize()}."
            else:
                answer = f"{query.capitalize()} is {answer[0].lower() + answer[1:]}" if answer else f"{query.capitalize()}."

    return answer, sources
