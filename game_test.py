import pandas as pd
import json
from elo import calculate_expected_score, update_elo


def update_elo_ratings_from_matches(match_data):
   
    player_ratings = {i+1: 1500 for i in range(28)} # 先測試28個人

    for _, row in match_data.iterrows():
        player_number = row[0]  # 選手號碼在第一列
        for i in range(1, 11, 2):  # 從第二列開始，每兩列一組，先勝負後對手號碼
            result = row[i]
            opponent_number = row[i + 1]

            if pd.notna(result) and pd.notna(opponent_number):
                player_rating = player_ratings[player_number]
                opponent_rating = player_ratings[opponent_number]

                expected_player, _ = calculate_expected_score(player_rating, opponent_rating)

                if result == 'O':
                    actual_player = 1
                elif result == 'X':
                    actual_player = 0

                player_ratings[player_number] = update_elo(player_rating, expected_player, actual_player)

    return player_ratings

