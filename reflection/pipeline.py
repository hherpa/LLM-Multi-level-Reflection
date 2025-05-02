import os
from together import Together
from reflection.steps import (
    process_initial_response,
    process_critical_analysis,
    process_questionable_judgments,
    process_reflective_questions,
    process_analysis_tones,
    process_final_reflections
)

def reflection_pipeline_stream(user_input, api_type, api_key, temperature, max_tokens, context_window, model):
    """The main pipeline of reflection"""
    if not api_key:
        yield [{"role": "assistant", "content": "Error: API key not provided"}]
        return
        
    try:
        # Инициализация клиента Together и переменных
        os.environ["TOGETHER_API_KEY"] = api_key
        client = Together()
        model_name = model
        
        # Инициализация чата для полного анализа
        chat_history = []
        chat_history.append({"role": "user", "content": user_input})
        
        # Step 1: Initial Response
        chat_history.append({"role": "assistant", "content": "⏳ Generating initial response..."})
        yield chat_history
        initial_response = process_initial_response(client, model_name, user_input, max_tokens, temperature, context_window)
        chat_history[-1] = {"role": "assistant", "content": initial_response}
        yield chat_history

        # Step 2: Critical Analysis
        chat_history.append({"role": "assistant", "content": "⏳ Performing critical analysis..."})
        yield chat_history
        analyzed_text = process_critical_analysis(client, model_name, initial_response, max_tokens, temperature, context_window)
        chat_history[-1] = {"role": "assistant", "content": analyzed_text}
        yield chat_history
        
        # Step 3: Top-3 Questionable Judgments
        chat_history.append({"role": "assistant", "content": "⏳ Finding questionable judgments..."})
        yield chat_history
        text2json = process_questionable_judgments(client, model_name, analyzed_text, max_tokens, temperature, context_window)
        chat_history[-1] = {"role": "assistant", "content": text2json}
        yield chat_history
        
        # Step 4: Reflective Questions
        chat_history.append({"role": "assistant", "content": "⏳ Generating reflective questions..."})
        yield chat_history
        edit_json = process_reflective_questions(client, model_name, text2json, max_tokens, temperature, context_window)
        chat_history[-1] = {"role": "assistant", "content": edit_json}
        yield chat_history
        
        # Step 5: Analysis in Different Tones
        chat_history.append({"role": "assistant", "content": "⏳ Analyzing in different tones..."})
        yield chat_history
        answers_json = process_analysis_tones(client, model_name, edit_json, max_tokens, temperature, context_window)
        chat_history[-1] = {"role": "assistant", "content": answers_json}
        yield chat_history
        
        # Step 6: Final Reflections
        chat_history.append({"role": "assistant", "content": "⏳ Generating final reflections..."})
        yield chat_history
        final_json = process_final_reflections(client, model_name, answers_json, max_tokens, temperature, context_window)
        chat_history[-1] = {"role": "assistant", "content": final_json}
        yield chat_history

    except Exception as e:
        error_message = f"Ошибка: {str(e)}"
        if not chat_history:
            chat_history = []
        chat_history.append({"role": "assistant", "content": error_message})
        yield chat_history 