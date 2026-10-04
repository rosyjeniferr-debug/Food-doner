from receivers import receivers


def find_matches(food_data):

    matches = []

    # Donor information
    message = food_data.get("food_text", "").lower()

    locations = [
        str(location).lower().strip()
        for location in food_data.get("locations", [])
    ]

    food_types = [
        str(food).lower().strip()
        for food in food_data.get("food_types", [])
    ]

    for receiver in receivers:

        receiver_location = receiver["location"].lower().strip()
        receiver_food = receiver["needed_food"].lower().strip()

        # -------------------------
        # LOCATION MATCH
        # -------------------------
        location_match = False

        for location in locations:
            if (
                receiver_location in location
                or location in receiver_location
            ):
                location_match = True

        if receiver_location in message:
            location_match = True

        # -------------------------
        # FOOD MATCH
        # -------------------------
        food_match = False

        # Receiver wants general food
        if receiver_food == "food":
            food_match = True

        # Receiver wants meals
        elif receiver_food == "meals":

            if (
                "meal" in message
                or "food" in message
                or "meals" in food_types
            ):
                food_match = True

        # Receiver wants vegetarian food
        elif receiver_food == "vegetarian":

            if (
                "vegetarian" in message
                or "veg" in message
                or "vegetarian" in food_types
            ):
                food_match = True

        # -------------------------
        # DISTANCE MATCH
        # -------------------------
        distance_match = (
            receiver["distance_km"] <= 50
        )

        # -------------------------
        # FINAL MATCH
        # -------------------------
        if (
            location_match
            and food_match
            and distance_match
        ):
            matches.append(receiver)

    return matches