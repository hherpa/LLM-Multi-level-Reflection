import os
from datetime import datetime
from together import Together
from utils import format_step, is_json_like, save_reflection_data

def process_with_together(inputs, step=1):
    try:
        debug_output = []
        print(f"\n=== Starting step {step} processing ===")
        
        input_text = inputs.get('text', '')
        system_prompt = inputs.get('System prompt', 'You are a helpful AI assistant.')
        api_key = inputs.get('API Key', '')
        max_tokens = int(inputs.get('Max Tokens', 1024))
        temperature = round(float(inputs.get('Temperature', 0.5)), 1)
        model_name = inputs.get('model', 'Qwen/Qwen2.5-72B-Instruct-Turbo')
        context_window = int(inputs.get('Context Window', 4096))
        
        if not api_key or not input_text:
            error_msg = "API key or input text not provided"
            return [{"role": "assistant", "content": error_msg}], "\n".join(debug_output)

        # Initialize Together client
        os.environ["TOGETHER_API_KEY"] = api_key
        client = Together()
        
        try:
            if step == 1:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": input_text}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature,
                    max_context_length=context_window
                )
                content = response.choices[0].message.content
                formatted_step = format_step(1, "Initial Response", content)
                return [
                    {"role": "user", "content": input_text},
                    {"role": "assistant", "content": formatted_step}
                ], "\n".join(debug_output)
                
            elif step == 2:
                sys_prompt = (
                    "Role: You are a professional critic with the characteristics of a person who doubts every statement. \n"
                    "Task: add to each judgment next to the degree of your confidence in its correctness [an integer from 0 to 100].\n"
                    "Limitations:\n"
                    "- Do not add your own comments. Send the source text with the added ratings.\n"
                    "Format:\n"
                    "Entropy is always decreasing in isolated systems [30] which is why ice melts faster in warmer temperatures [20]..."
                )
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": f"Text: {input_text}"}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature,
                    max_context_length=context_window
                )
                content = response.choices[0].message.content
                formatted_step = format_step(2, "Critical Analysis", content)
                return [{"role": "assistant", "content": formatted_step}], "\n".join(debug_output)
                
            elif step == 3:
                json_sys_prompt = (
                    "At the entrance, you receive a text that is divided into the ratings of each sentence. Output the json with the top-3 smallest values from the text.\n"
                    "Output Format:\n"
                    "{\n"
                    "    \"judgment\": \"Entropy is always decreasing in isolated systems\",\n"
                    "    \"confidence\": 30\n"
                    "},"
                )
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": json_sys_prompt},
                        {"role": "user", "content": f"Text: {input_text}"}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature,
                    max_context_length=context_window
                )
                content = response.choices[0].message.content
                formatted_step = format_step(3, "Top-3 Questionable Judgments", content, as_code=is_json_like(content))
                return [{"role": "assistant", "content": formatted_step}], "\n".join(debug_output)
                
            elif step == 4:
                prompt = f"""Edit the json and add a reflective question based on the confidence score to each one.\nOutput format: json code only."""
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature,
                    max_context_length=context_window
                )
                content = response.choices[0].message.content
                formatted_step = format_step(4, "Reflective Questions", content, as_code=is_json_like(content))
                return [{"role": "assistant", "content": formatted_step}], "\n".join(debug_output)
                
            elif step == 5:
                sys_prompt = (
                    "You are a critical judgment analyst. For each statement generate three responses:\n"
                    "1. logical_answer: Objective analysis\n"
                    "2. empathic_answer: Empathy and support\n"
                    "3. skeptic_answer: Doubt and questioning\n"
                    "Output in JSON format."
                )
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": f"Text: {input_text}"}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature,
                    max_context_length=context_window
                )
                content = response.choices[0].message.content
                formatted_step = format_step(5, "Analysis in Different Tones", content, as_code=is_json_like(content))
                return [{"role": "assistant", "content": formatted_step}], "\n".join(debug_output)
                
            elif step == 6:
                prompt = """Select 1-2 best answers for each critical element.\nOutput format: json code only."""
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature,
                    max_context_length=context_window
                )
                content = response.choices[0].message.content
                formatted_step = format_step(6, "Final Reflections", content, as_code=is_json_like(content))
                return [{"role": "assistant", "content": formatted_step}], "\n".join(debug_output)
            
            else:
                raise ValueError(f"Unknown step: {step}")
                
        except Exception as e:
            error_msg = f"Error during step {step} execution: {str(e)}"
            print(f"\nERROR: {error_msg}")
            debug_output.append(error_msg)
            return [{"role": "assistant", "content": error_msg}], "\n".join(debug_output)
            
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        print(f"\nERROR: {error_msg}")
        debug_output.append(error_msg)
        print("\n=== End of request processing ===\n")
        return [{"role": "assistant", "content": error_msg}], "\n".join(debug_output)

def reflection_pipeline_stream(user_input, api_type, api_key, temperature, max_tokens, context_window, model):
    if not api_key:
        yield [{"role": "assistant", "content": "Error: API key not provided"}]
        return
        
    try:
        # Initialize Together client and variables
        os.environ["TOGETHER_API_KEY"] = api_key
        client = Together()
        model_name = model
        
        # Initialize chat for complete analysis
        chat_history = []
        chat_history.append({"role": "user", "content": user_input})
        
        # Step 1: Initial Response
        chat_history.append({"role": "assistant", "content": "⏳ Generating initial response..."})
        yield chat_history

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            max_context_length=context_window
        )
        initial_response = response.choices[0].message.content
        chat_history[-1] = {"role": "assistant", "content": format_step(1, "Initial Response", initial_response)}
        yield chat_history

        # Step 2: Critical Analysis
        chat_history.append({"role": "assistant", "content": "⏳ Performing critical analysis..."})
        yield chat_history

        sys_prompt = (
            "Role: You are a professional critic with the characteristics of a person who doubts every statement. \n"
            "Task: add to each judgment next to the degree of your confidence in its correctness [an integer from 0 to 100].\n"
            "Limitations:\n"
            "- Do not add your own comments. Send the source text with the added ratings.\n"
            "Format:\n"
            "Entropy is always decreasing in isolated systems [30] which is why ice melts faster in warmer temperatures [20]..."
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": f"Text: {initial_response}"}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            max_context_length=context_window
        )
        analyzed_text = response.choices[0].message.content
        chat_history[-1] = {"role": "assistant", "content": format_step(2, "Critical Analysis", analyzed_text)}
        yield chat_history
        
        # Step 3: Top-3 Questionable Judgments
        chat_history.append({"role": "assistant", "content": "⏳ Finding questionable judgments..."})
        yield chat_history

        json_sys_prompt = (
            "At the entrance, you receive a text that is divided into the ratings of each sentence. Output the json with the top-3 smallest values from the text.\n"
            "Output Format:\n"
            "{\n"
            "    \"judgment\": \"Entropy is always decreasing in isolated systems\",\n"
            "    \"confidence\": 30\n"
            "},"
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": json_sys_prompt},
                {"role": "user", "content": f"Text: {analyzed_text}"}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            max_context_length=context_window
        )
        text2json = response.choices[0].message.content
        chat_history[-1] = {"role": "assistant", "content": format_step(3, "Top-3 Questionable Judgments", text2json, as_code=True)}
        yield chat_history
        
        # Step 4: Reflective Questions
        chat_history.append({"role": "assistant", "content": "⏳ Generating reflective questions..."})
        yield chat_history

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": f"{text2json}\nEdit the json and add a reflective question based on the confidence score to each one.\nOutput format: json code only."}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            max_context_length=context_window
        )
        questions_json = response.choices[0].message.content
        chat_history[-1] = {"role": "assistant", "content": format_step(4, "Reflective Questions", questions_json, as_code=True)}
        yield chat_history
        
        # Step 5: Analysis in Different Tones
        chat_history.append({"role": "assistant", "content": "⏳ Analyzing in different tones..."})
        yield chat_history

        sys_prompt = (
            "You are a critical judgment analyst. For each statement generate three responses:\n"
            "1. logical_answer: Objective analysis\n"
            "2. empathic_answer: Empathy and support\n"
            "3. skeptic_answer: Doubt and questioning\n"
            "Output in JSON format."
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": f"Text: {questions_json}"}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            max_context_length=context_window
        )
        analysis_json = response.choices[0].message.content
        chat_history[-1] = {"role": "assistant", "content": format_step(5, "Analysis in Different Tones", analysis_json, as_code=True)}
        yield chat_history
        
        # Step 6: Final Reflections
        chat_history.append({"role": "assistant", "content": "⏳ Selecting final reflections..."})
        yield chat_history

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": f"{analysis_json}\nSelect 1-2 best answers for each critical element.\nOutput format: json code only."}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            max_context_length=context_window
        )
        final_json = response.choices[0].message.content
        chat_history[-1] = {"role": "assistant", "content": format_step(6, "Final Reflections", final_json, as_code=True)}
        yield chat_history
        
        # Save reflection data
        save_reflection_data({
            "user_input": user_input,
            "steps": chat_history
        })
        
    except Exception as e:
        error_msg = f"Error in reflection pipeline: {str(e)}"
        print(f"\nERROR: {error_msg}")
        yield [{"role": "assistant", "content": error_msg}] 