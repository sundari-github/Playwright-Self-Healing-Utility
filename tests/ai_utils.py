
import ollama
import logging

logger = logging.getLogger(__name__)


def get_healed_selector(broken_selector, html_snippet, desc):
    ai_prompt = f"""
    TARGET ELEMENT: {desc}
    HTML CONTEXT:
    {html_snippet}

    TASK:
    Identify the NEW CSS selector for the target element in the HTML above.
    """
    ai_response = ollama.generate(model='qwen2.5-coder:7b', prompt=ai_prompt, options={'temperature': 0},
                                  system=f"""You are a CSS Selector expert
                                             Return ONLY the new selector string.
                                             DO NOT return the broken selector '{broken_selector}'
                                             No markdown. No explanations. No backticks.""")
    corrected_id = ai_response['response'].strip().split()[0]
    logger.info(f"AI suggested selector: {corrected_id}")
    return corrected_id


if __name__ == "__main__":
    try:
        response = ollama.list()
        # Check if we actually have models
        if not response.models:
            print("Connection okay, but no models found.")
        else:
            for m in response.models:
                # In the latest library, m is an object, so we use m.model
                print(f'Connection Successful. Found model: {m.model}')
    except Exception as e:
        print(f"Could not connect to server {e}")
    test_html = """
        <div class="filter-section">
            <label>
                <input type="checkbox" id="new-get-it-today" class="checkbox-style">
                <span>Get It Today</span>
            </label>
        </div>
        """
    broken_id = "#old-check"
    description = "Get it today checkbox"
    result = get_healed_selector(broken_id, test_html, description)
    print(f'\nAI Suggestion\n{result}')
