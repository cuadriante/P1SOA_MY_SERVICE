import json

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

json_data = load_json_file('data/predefined_sugg.json')

def get_recommendations(json_data, main_dish):
    """
    Retrieve recommendations based on the main dish.
    Args:
        json_data (dict): The JSON dictionary containing main dish keys and recommendation values.
        main_dish (str): The main dish to retrieve recommendations for.
    Returns:
        A list of recommendations for the specified main dish, or None if the main dish is not found.
    """
    main_dish_lower = main_dish.lower()
    for dish_key in json_data:
        if dish_key.lower() == main_dish_lower:
            return json_data[dish_key]
    return None

def get_predefined_suggestion(entry: str) -> str:
    return get_recommendations(json_data, entry)
