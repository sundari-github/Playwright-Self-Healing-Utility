"""
AI utilities for self-healing selectors in Playwright automation.

This module leverages the Ollama AI model (specifically qwen2.5-coder) to generate
CSS selectors when the original selectors fail. It provides intelligent fallback
selectors based on HTML context and element descriptions, enabling automated
testing to adapt to UI changes dynamically.
"""

import ollama
import logging

logger = logging.getLogger(__name__)


def get_healed_selector(broken_selector, html_snippet, desc):
    """
    Use AI model to generate a corrected CSS selector for a broken selector.
    
    When a UI element's selector becomes invalid (element moved, ID changed, etc.),
    this function uses AI to analyze the HTML context and generate a new valid
    selector for the same element based on its description and surrounding HTML.
    
    Args:
        broken_selector (str): The original CSS selector that failed to find the element
        html_snippet (str): HTML context containing the target element
        desc (str): Human-readable description of the element to locate (e.g., "Get It Today")
        
    Returns:
        str: A new CSS selector for the target element suggested by the AI model
        
    Notes:
        - Uses the Ollama 'qwen2.5-coder:7b' model with temperature=0 for consistency
        - The AI is instructed to return only the selector string without explanations
        - Only the first word of the AI response is extracted and returned
    """
    # Construct the AI prompt with context about the element to find
    ai_prompt = f"""
    TARGET ELEMENT: {desc}
    HTML CONTEXT:
    {html_snippet}

    TASK:
    Identify the NEW CSS selector for the target element in the HTML above.
    """
    
    # Query the Ollama AI model with specific instructions
    ai_response = ollama.generate(
        model='qwen2.5-coder:7b',
        prompt=ai_prompt,
        options={'temperature': 0},  # Temperature 0 for deterministic results
        system=f"""You are a CSS Selector expert
                   Return ONLY the new selector string.
                   DO NOT return the broken selector '{broken_selector}'
                   No markdown. No explanations. No backticks."""
    )
    
    # Extract the suggested selector (first word of the response)
    corrected_id = ai_response['response'].strip().split()[0]
    logger.info(f"AI suggested selector: {corrected_id}")
    return corrected_id


if __name__ == "__main__":
    # Test block: Verify Ollama server connection and test the healing functionality
    try:
        # Attempt to connect to Ollama server and list available models
        response = ollama.list()
        
        # Check if any models are available
        if not response.models:
            print("Connection okay, but no models found.")
        else:
            # Display all available models
            for m in response.models:
                print(f'Connection Successful. Found model: {m.model}')
    except Exception as e:
        print(f"Could not connect to server {e}")
    
    # Example: Test the get_healed_selector function with sample HTML and selector
    test_html = """
        <div class="filter-section">
            <label>
                <input type="checkbox" id="new-get-it-today" class="checkbox-style">
                <span>Get It Today</span>
            </label>
        </div>
        """
    
    # Simulate a broken selector scenario
    broken_id = "#old-check"  # This selector would fail
    description = "Get it today checkbox"
    
    # Request AI to find the correct selector
    result = get_healed_selector(broken_id, test_html, description)
    print(f'\nAI Suggestion\n{result}')
