import pandas as pd
import json
from elo import calculate_expected_score, update_elo


def update_elo_ratings_from_matches(match_data):
   
    initial_player_ratings = {i+1: 1500 for i in range(28)}
    updated_player_ratings = initial_player_ratings.copy()

    for _, row in match_data.iterrows():
        player_number = row[0]  # 選手號碼在第一列
        temp_player_rating = initial_player_ratings[player_number]

        for i in range(1, 11, 2):  # 從第二列開始，每兩列一組，先勝負後對手號碼
            result = row[i]
            opponent_number = row[i + 1]

            if pd.notna(result) and pd.notna(opponent_number):
                temp_opponent_rating = initial_player_ratings[opponent_number]

                expected_player, _ = calculate_expected_score(temp_player_rating, temp_opponent_rating)

                if result == 'O':
                    actual_player = 1
                elif result == 'X':
                    actual_player = 0

                new_player_rating = update_elo(temp_player_rating, expected_player, actual_player)
                temp_player_rating = new_player_rating

        updated_player_ratings[player_number] = temp_player_rating

    return updated_player_ratings

