def calculate_daily_norms(user):
    """
    Mifflin–St Jeor формула + активность + цель + разбивка БЖУ.
    """

    if user.gender.lower() == "male":
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age + 5
    else:
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age - 161

    activity = {
        "low": 1.2,
        "medium": 1.4,
        "high": 1.6,
    }

    bmr *= activity.get(user.activity_level, 1.2)

    if user.goal == "lose":
        bmr *= 0.85
    elif user.goal == "gain":
        bmr *= 1.15

    protein = (bmr * 0.30) / 4
    fat = (bmr * 0.25) / 9
    carbs = (bmr * 0.45) / 4

    return bmr, protein, fat, carbs
