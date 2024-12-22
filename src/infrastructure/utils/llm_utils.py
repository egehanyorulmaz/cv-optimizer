from typing import Optional

def clean_llm_json_response(response: str) -> str:
    """
    Clean JSON response from LLM by removing markdown formatting.
    
    :param response: Raw response string from LLM that may contain markdown
    :type response: str
    :return: Cleaned JSON string
    :rtype: str
    """
    if not response:
        return ""
        
    # Clean up potential markdown formatting
    response = response.strip()
    if response.startswith('```json'):
        response = response[7:]
    elif response.startswith('```'):
        response = response[3:]
    if response.endswith('```'):
        response = response[:-3]
        
    return response.strip() 