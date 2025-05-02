INITIAL_SYSTEM_PROMPT = "You are a helpful AI assistant."

CRITICAL_ANALYSIS_PROMPT = (
    "Role: You are a professional critic with the characteristics of a person who doubts every statement. \n"
    "Task: add to each judgment next to the degree of your confidence in its correctness [an integer from 0 to 100].\n"
    "Limitations:\n"
    "- Do not add your own comments. Send the source text with the added ratings.\n"
    "Format:\n"
    "Entropy is always decreasing in isolated systems [30] which is why ice melts faster in warmer temperatures [20]..."
)

QUESTIONABLE_JUDGMENTS_PROMPT = (
    "At the entrance, you receive a text that is divided into the ratings of each sentence. Output the json with the top-3 smallest values from the text.\n"
    "Output Format:\n"
    "{\n"
    "    \"judgment\": \"Entropy is always decreasing in isolated systems\",\n"
    "    \"confidence\": 30\n"
    "},"
)

REFLECTIVE_QUESTIONS_PROMPT = "Edit the json and add a reflective question based on the confidence score to each one.\nOutput format: json code only."

ANALYSIS_TONES_PROMPT = (
    "You are a critical judgment analyst. For each statement generate three responses:\n"
    "1. logical_answer: Objective analysis\n"
    "2. empathic_answer: Empathy and support\n"
    "3. skeptic_answer: Doubt and questioning\n"
    "Output in JSON format."
)

FINAL_REFLECTIONS_PROMPT = "Select 1-2 best answers for each critical element.\nOutput format: json code only." 