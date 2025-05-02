def format_step(step_num, title, content, as_code=False):
    formatted_content = content.strip()
    
    if as_code:
        # Удаляем существующие маркеры кода, если они есть
        if formatted_content.startswith('```json'):
            formatted_content = formatted_content[7:]
        elif formatted_content.startswith('```'):
            formatted_content = formatted_content[3:]
        if formatted_content.endswith('```'):
            formatted_content = formatted_content[:-3]
        
        formatted_content = formatted_content.strip()
        
        # Добавляем маркеры кода только если их нет
        if not formatted_content.startswith('```'):
            formatted_content = f"```json\n{formatted_content}\n```"
    
    # Добавляем четкие визуальные разделители
    return f"""### Step {step_num}: {title}

{formatted_content}

-----------------------------------"""

def format_final_message(steps_data):
    """Форматирует итоговое сообщение с результатами всех этапов рефлексии"""
    if isinstance(steps_data, str):
        return steps_data
        
    message = "# 🤔 Reflection Complete\n\n"
    
    for step in steps_data:
        if isinstance(step, dict) and 'content' in step:
            # Удаляем старые разделители и добавляем новые
            content = step['content'].replace('---', '').strip()
            message += f"{content}\n\n=====================================\n\n"
    
    # Добавляем финальный разделитель
    message += "\n# ✨ Reflection Process Complete"
    return message

def is_json_like(text):
    """Проверяет, похож ли текст на JSON"""
    text = text.strip()
    return text.startswith('{') and text.endswith('}') or text.startswith('[') and text.endswith(']') 