from together import Together
from utils.formatters import format_step, is_json_like
from reflection.prompts import (
    INITIAL_SYSTEM_PROMPT,
    CRITICAL_ANALYSIS_PROMPT,
    QUESTIONABLE_JUDGMENTS_PROMPT,
    REFLECTIVE_QUESTIONS_PROMPT,
    ANALYSIS_TONES_PROMPT,
    FINAL_REFLECTIONS_PROMPT
)

def process_step(client, model_name, messages, max_tokens, temperature, context_window, step_num, title, as_code=False):
    """Обрабатывает один шаг рефлексии"""
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        max_context_length=context_window
    )
    content = response.choices[0].message.content
    return format_step(step_num, title, content, as_code=as_code)

def process_initial_response(client, model_name, user_input, max_tokens, temperature, context_window):
    """Обрабатывает начальный ответ"""
    messages = [
        {"role": "system", "content": INITIAL_SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    return process_step(client, model_name, messages, max_tokens, temperature, context_window, 1, "Initial Response")

def process_critical_analysis(client, model_name, text, max_tokens, temperature, context_window):
    """Обрабатывает критический анализ"""
    messages = [
        {"role": "system", "content": CRITICAL_ANALYSIS_PROMPT},
        {"role": "user", "content": f"Text: {text}"}
    ]
    return process_step(client, model_name, messages, max_tokens, temperature, context_window, 2, "Critical Analysis")

def process_questionable_judgments(client, model_name, text, max_tokens, temperature, context_window):
    """Обрабатывает сомнительные суждения"""
    messages = [
        {"role": "system", "content": QUESTIONABLE_JUDGMENTS_PROMPT},
        {"role": "user", "content": f"Text: {text}"}
    ]
    return process_step(client, model_name, messages, max_tokens, temperature, context_window, 3, "Top-3 Questionable Judgments", as_code=True)

def process_reflective_questions(client, model_name, text, max_tokens, temperature, context_window):
    """Обрабатывает рефлексивные вопросы"""
    messages = [{"role": "user", "content": f"{text}\n{REFLECTIVE_QUESTIONS_PROMPT}"}]
    return process_step(client, model_name, messages, max_tokens, temperature, context_window, 4, "Reflective Questions", as_code=True)

def process_analysis_tones(client, model_name, text, max_tokens, temperature, context_window):
    """Обрабатывает анализ в разных тонах"""
    messages = [
        {"role": "system", "content": ANALYSIS_TONES_PROMPT},
        {"role": "user", "content": f"Text: {text}"}
    ]
    return process_step(client, model_name, messages, max_tokens, temperature, context_window, 5, "Analysis in Different Tones", as_code=True)

def process_final_reflections(client, model_name, text, max_tokens, temperature, context_window):
    """Обрабатывает финальные размышления"""
    messages = [{"role": "user", "content": f"{text}\n{FINAL_REFLECTIONS_PROMPT}"}]
    return process_step(client, model_name, messages, max_tokens, temperature, context_window, 6, "Final Reflections", as_code=True) 