def calculate_expected_score(rating_a, rating_b):
    except_score_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    except_score_b = 1 / (1 + 10 ** ((rating_a - rating_b) / 400))
    return except_score_a, except_score_b


def update_elo(rating, except_score, actual_score, k_factor=40):
    new_rating = rating + k_factor * (actual_score - except_score)
    return new_rating
