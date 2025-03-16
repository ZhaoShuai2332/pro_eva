from openai import OpenAI
import re, json, ast

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',
)

def chat_with_ai(prompt, user = 'user'):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': user,
                'content': prompt,
            }
        ],
        model='deepseek-r1:8b',
    )
    return chat_completion.choices[0].message.content


def generate_prompt(dish_names=[], collect_dishes=[]):
    """
    Generate a prompt for simulating user behavior in a recommendation system, specifically for selecting a single meal per session.

    :param dish_names: List of dishes recommended by the system
    :param collect_dishes: List of dishes collected by the user
    :return: A structured prompt string
    """
    
    prompt = f"""You are a real food enthusiast browsing restaurant recommendations provided by the system during a single meal session. Based on your collection habits, simulate your real behavior and strictly return your click and purchase data in **JSON format**.

                The recommendation system suggests the following dishes:
                {json.dumps(dish_names, ensure_ascii=False)}

                Your collected dishes:
                {json.dumps(collect_dishes, ensure_ascii=False)}

                As a real user, based on your collection history, simulate your behavior and strictly return the result in the following JSON format:

                Rules:
                1. You can click on multiple dishes to check details.
                2. You can purchase at most **one dish** or choose not to purchase at all (Purchase_Count must be **0 or 1**).
                3. All four parameters **must be explicitly provided** in the response.

                ```json
                {{
                "Click_List": ["Clicked Dish 1", "Clicked Dish 2", "Clicked Dish 3"],
                "Purchase_List": ["Purchased Dish"],
                "Click_Count": 0 or more,
                "Purchase_Count": 0 or 1
                }}
                ```"""
    return prompt


def extract_json_data(response):
    """
    Extract click and purchase data from the model response using regex.

    :param response: The model's raw text response
    :return: Extracted JSON data as a dictionary
    """
    json_pattern = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
    if json_pattern:
        try:
            extracted_json = json.loads(json_pattern.group(1))
            return {
                "Click_List": extracted_json.get("Click_List", []),
                "Purchase_List": extracted_json.get("Purchase_List", []),
                "Click_Count": extracted_json.get("Click_Count", 0),
                "Purchase_Count": extracted_json.get("Purchase_Count", 0),
            }
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format"}
    return {"error": "No JSON found in response"}

def extract_click_purchase_counts(data):
    """
    Extract Click_Count and Purchase_Count from JSON data.

    :param data: Dictionary containing click and purchase information
    :return: Tuple (Click_Count, Purchase_Count)
    """
    return data.get('Click_Count', 0), data.get('Purchase_Count', 0)

def parse_json_string(json_string):
    """
    Convert a JSON-like string to a Python dictionary.

    :param json_string: JSON-like string
    :return: Parsed dictionary
    """
    try:
        data = ast.literal_eval(json_string)  # Safely evaluate string to dictionary
        return extract_click_purchase_counts(data)
    except (ValueError, SyntaxError):
        print("Error: Invalid JSON-like string")
        return (0, 0)  # Default fallback if parsing fails

def calculate_precision_coverage(recommended_dishes, purchase_list):
    """
    计算推荐系统的准确率 (Precision) 和覆盖率 (Coverage)。

    :param recommended_dishes: 推荐的菜品列表
    :param purchase_list: 用户购买的菜品列表
    :return: (准确率, 覆盖率)
    """
    if not purchase_list:
        return 0.0, 0.0  # 避免除零错误
    
    purchased_recommended = [dish for dish in purchase_list if dish in recommended_dishes]
    precision = len(purchased_recommended) / len(purchase_list)
    coverage = len(purchased_recommended) / len(recommended_dishes) if recommended_dishes else 0.0
    
    return precision, coverage