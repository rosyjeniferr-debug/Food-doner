import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")


def analyze_food_message(message):
    doc = nlp(message)

    result = {
        "numbers": [],
        "locations": [],
        "organizations": [],
        "food_types": [],
        "urgency": "Normal",
        "food_text": message
    }

    # Extract information using spaCy
    for ent in doc.ents:
        if ent.label_ == "CARDINAL":
            result["numbers"].append(ent.text)

        elif ent.label_ == "GPE":
            result["locations"].append(ent.text)

        elif ent.label_ == "ORG":
            result["organizations"].append(ent.text)

    # Detect food-related words
    food_words = [
        "rice",
        "meals",
        "biryani",
        "chapati",
        "roti",
        "food",
        "vegetarian",
        "non-vegetarian"
    ]

    for word in food_words:
        if word.lower() in message.lower():
            result["food_types"].append(word)

    # Detect urgency
    urgent_words = [
        "urgent",
        "urgently",
        "immediately",
        "soon",
        "quickly",
        "within 1 hour",
        "within one hour",
        "collect now",
        "pickup now"
    ]

    message_lower = message.lower()

    for word in urgent_words:
        if word in message_lower:
            result["urgency"] = "Urgent"
            break

    return result