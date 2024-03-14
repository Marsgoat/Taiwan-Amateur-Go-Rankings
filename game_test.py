import pandas as pd
import json
import re
from elo import calculate_expected_score, update_elo

def clean_player_number(player_number):
    if not player_number or player_number == '汰' or not isinstance(player_number, str):
        return 0

    # 移除上下調箭頭
    cleaned_number = re.sub(r'[^\d]', '', player_number)
    
    return int(cleaned_number) if cleaned_number else 0

def update_elo_ratings_from_matches(match_data_path, elo_json_path, new_elo_json_path='new.json'):
   
    # 讀取elo.json
    with open(elo_json_path, 'r', encoding='utf-8') as file:
        initial_player_ratings = json.load(file)
    
    updated_player_ratings = initial_player_ratings.copy()

    # 讀取比賽資料
    match_data = pd.read_excel(match_data_path)
    

    # 建立選手號碼到選手名稱的mapping
    player_number_to_name = {row[0]: row[1] for _, row in match_data.iterrows()}
    
    # 紀錄每一局比賽的ELO評分，整場比賽結束後再更新
    elo_changes = {player: 0 for player in initial_player_ratings}

    for _, row in match_data.iterrows():
        player_name = row[1]
        if player_name not in initial_player_ratings:
            continue

        for i in range(9, match_data.shape[1], 2):
            if i + 1 < match_data.shape[1]:
                opponent_number = clean_player_number(row[i])
                
                result = row[i + 1]
                opponent_name = player_number_to_name.get(opponent_number)

                if opponent_name and opponent_name in initial_player_ratings:
                    player_rating = initial_player_ratings[player_name]
                    opponent_rating = initial_player_ratings[opponent_name]
                    # if player_name =='':
                    #     print(player_name, opponent_number, opponent_name)
                    #     print(player_rating, opponent_rating)

                    expected_player, _ = calculate_expected_score(player_rating, opponent_rating)
                    actual_player = 1 if result == 'O' else 0

                    # 計算評分變化量而不是直接更新評分
                    change = update_elo(player_rating, expected_player, actual_player) - player_rating
                    elo_changes[player_name] += change

    print (elo_changes)
    
    # 更新ELO評分
    updated_player_ratings = {player: initial_player_ratings[player] + elo_changes[player] for player in initial_player_ratings}
    updated_player_ratings = dict(sorted(updated_player_ratings.items(), key=lambda item: item[1], reverse=True))

    with open(new_elo_json_path, 'w', encoding='utf-8') as file:
        json.dump(updated_player_ratings, file, ensure_ascii=False)
    
    return updated_player_ratings


# 測試
match_data_path = './game.xlsx'
elo_json_path = './elo.json'

updated_ratings = update_elo_ratings_from_matches(match_data_path, elo_json_path)
# print(updated_ratings)