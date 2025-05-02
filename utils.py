import os
import json
from datetime import datetime

def format_step(step_num, title, content, as_code=False):
    formatted_content = content.strip()
    
    if as_code:
        # Remove existing code markers if they exist
        if formatted_content.startswith('```json'):
            formatted_content = formatted_content[7:]
        elif formatted_content.startswith('```'):
            formatted_content = formatted_content[3:]
        if formatted_content.endswith('```'):
            formatted_content = formatted_content[:-3]
        
        formatted_content = formatted_content.strip()
        
        # Add code markers only if they don't exist
        if not formatted_content.startswith('```'):
            formatted_content = f"```json\n{formatted_content}\n```"
    
    # Add clear visual separators
    return f"""### Step {step_num}: {title}

{formatted_content}

-----------------------------------"""

def format_final_message(steps_data):
    """Formats the final message with results of all reflection steps"""
    if isinstance(steps_data, str):
        return steps_data
        
    message = "# 🤔 Reflection Complete\n\n"
    
    for step in steps_data:
        if isinstance(step, dict) and 'content' in step:
            # Remove old separators and add new ones
            content = step['content'].replace('---', '').strip()
            message += f"{content}\n\n=====================================\n\n"
    
    # Add final separator
    message += "\n# ✨ Reflection Process Complete"
    return message

def is_json_like(text):
    """Checks if the text looks like JSON"""
    text = text.strip()
    return text.startswith('{') and text.endswith('}') or text.startswith('[') and text.endswith(']')

def save_reflection_data(data):
    """Saves reflection data to a JSON file"""
    try:
        # Create directory if it doesn't exist
        os.makedirs("reflections", exist_ok=True)
        
        # Add timestamp in readable format
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        data['timestamp'] = timestamp
        
        # Form filename
        filepath = os.path.join("reflections", f"reflection_{timestamp}.json")
        
        # Save data to JSON with indentation for readability
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Reflection saved to {filepath}")
        return True
    except Exception as e:
        print(f"Error saving reflection: {str(e)}")
        return False 