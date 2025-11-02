from supabase_config import supabase
import re

def extract_game_id_from_url(url):
    """Extract game ID from ESPN URL"""
    match = re.search(r'/gameId/(\d+)', url)
    return match.group(1) if match else None

def insert_live_game(game_data):
    """Insert or update live game data"""
    try:
        # Check if game already exists in live_nfl_games
        existing = supabase.table("live_nfl_games").select("id").eq("team_one_name", game_data['team_one_name']).eq("team_two_name", game_data['team_two_name']).execute()
        
        if existing.data:
            # Update existing live game
            result = supabase.table("live_nfl_games").update(game_data).eq("id", existing.data[0]['id']).execute()
            print(f"Updated live game: {game_data['team_one_name']} vs {game_data['team_two_name']}")
        else:
            # Insert new live game
            result = supabase.table("live_nfl_games").insert(game_data).execute()
            print(f"Inserted new live game: {game_data['team_one_name']} vs {game_data['team_two_name']}")
        return True
    except Exception as e:
        print(f"Error inserting/updating live game: {e}")
        return False

def move_game_to_final(game_data):
    """Move game from live_nfl_games to final_games"""
    try:
        # Insert into final_games
        result = supabase.table("final_games").insert(game_data).execute()
        print(f"Moved game to final: {game_data['team_one_name']} vs {game_data['team_two_name']}")
        
        # Remove from live_nfl_games
        supabase.table("live_nfl_games").delete().eq("team_one_name", game_data['team_one_name']).eq("team_two_name", game_data['team_two_name']).execute()
        print(f"Removed from live games: {game_data['team_one_name']} vs {game_data['team_two_name']}")
        
        return True
    except Exception as e:
        print(f"Error moving game to final: {e}")
        return False

def create_game_data_dict(team_one_logo, team_one_name, team_one_score, team_one_records, 
                         team_two_logo, team_two_name, team_two_score, team_two_records,
                         team_one_passing_yard_player_image, team_one_passing_yard_player_name, 
                         team_one_passing_yard_player_position, team_one_passing_yard_player_game_state, 
                         team_one_player_one_passing_yard, team_two_passing_yard_player_image, 
                         team_two_passing_yard_player_name, team_two_passing_yard_player_position, 
                         team_two_passing_yard_player_game_state, team_two_player_two_passing_yard,
                         team_one_rushing_yard_player_image, team_one_rushing_yard_player_name, 
                         team_one_rushing_yard_player_position, team_one_rushing_yard_player_game_state, 
                         team_one_player_one_rushing_yard, team_two_rushing_yard_player_image, 
                         team_two_rushing_yard_player_name, team_two_rushing_yard_player_position, 
                         team_two_rushing_yard_player_game_state, team_two_player_two_rushing_yard,
                         team_one_receiving_yard_player_image, team_one_receiving_yard_player_name, 
                         team_one_receiving_yard_player_position, team_one_receiving_yard_player_game_state, 
                         team_one_player_one_receiving_yard, team_two_receiving_yard_player_image, 
                         team_two_receiving_yard_player_name, team_two_receiving_yard_player_position, 
                         team_two_receiving_yard_player_game_state, team_two_player_two_receiving_yard,
                         team_one_sacks_player_image, team_one_sacks_player_name, team_one_sacks_player_position, 
                         team_one_player_one_sacks, team_two_sacks_player_image, team_two_sacks_player_name, 
                         team_two_sacks_player_position, team_two_player_two_sacks,
                         team_one_tackles_player_image, team_one_tackles_player_name, team_one_tackles_player_position, 
                         team_one_tackles_player_game_state, team_one_player_one_tackles, team_two_tackles_player_image, 
                         team_two_tackles_player_name, team_two_tackles_player_position, team_two_tackles_player_game_state, 
                         team_two_player_two_tackles, team_one_total_yards, team_two_total_yards, 
                         team_one_total_turnovers, team_two_total_turnovers, team_one_first_downs, 
                         team_two_first_downs, team_one_penalties, team_two_penalties, team_one_third_down, 
                         team_two_third_down, team_one_forth_down, team_two_forth_down, team_one_red_zone, 
                         team_two_red_zone, team_one_possession, team_two_possession, game_status):
    """Create a dictionary with all the game data"""
    return {
        "team_one_logo": team_one_logo,
        "team_one_name": team_one_name,
        "team_one_score": team_one_score,
        "team_one_records": team_one_records,
        "team_two_logo": team_two_logo,
        "team_two_name": team_two_name,
        "team_two_score": team_two_score,
        "team_two_records": team_two_records,
        "team_one_passing_yard_player_image": team_one_passing_yard_player_image,
        "team_one_passing_yard_player_name": team_one_passing_yard_player_name,
        "team_one_passing_yard_player_position": team_one_passing_yard_player_position,
        "team_one_passing_yard_player_game_state": team_one_passing_yard_player_game_state,
        "team_one_player_one_passing_yard": team_one_player_one_passing_yard,
        "team_two_passing_yard_player_image": team_two_passing_yard_player_image,
        "team_two_passing_yard_player_name": team_two_passing_yard_player_name,
        "team_two_passing_yard_player_position": team_two_passing_yard_player_position,
        "team_two_passing_yard_player_game_state": team_two_passing_yard_player_game_state,
        "team_two_player_two_passing_yard": team_two_player_two_passing_yard,
        "team_one_rushing_yard_player_image": team_one_rushing_yard_player_image,
        "team_one_rushing_yard_player_name": team_one_rushing_yard_player_name,
        "team_one_rushing_yard_player_position": team_one_rushing_yard_player_position,
        "team_one_rushing_yard_player_game_state": team_one_rushing_yard_player_game_state,
        "team_one_player_one_rushing_yard": team_one_player_one_rushing_yard,
        "team_two_rushing_yard_player_image": team_two_rushing_yard_player_image,
        "team_two_rushing_yard_player_name": team_two_rushing_yard_player_name,
        "team_two_rushing_yard_player_position": team_two_rushing_yard_player_position,
        "team_two_rushing_yard_player_game_state": team_two_rushing_yard_player_game_state,
        "team_two_player_two_rushing_yard": team_two_player_two_rushing_yard,
        "team_one_receiving_yard_player_image": team_one_receiving_yard_player_image,
        "team_one_receiving_yard_player_name": team_one_receiving_yard_player_name,
        "team_one_receiving_yard_player_position": team_one_receiving_yard_player_position,
        "team_one_receiving_yard_player_game_state": team_one_receiving_yard_player_game_state,
        "team_one_player_one_receiving_yard": team_one_player_one_receiving_yard,
        "team_two_receiving_yard_player_image": team_two_receiving_yard_player_image,
        "team_two_receiving_yard_player_name": team_two_receiving_yard_player_name,
        "team_two_receiving_yard_player_position": team_two_receiving_yard_player_position,
        "team_two_receiving_yard_player_game_state": team_two_receiving_yard_player_game_state,
        "team_two_player_two_receiving_yard": team_two_player_two_receiving_yard,
        "team_one_sacks_player_image": team_one_sacks_player_image,
        "team_one_sacks_player_name": team_one_sacks_player_name,
        "team_one_sacks_player_position": team_one_sacks_player_position,
        "team_one_player_one_sacks": team_one_player_one_sacks,
        "team_two_sacks_player_image": team_two_sacks_player_image,
        "team_two_sacks_player_name": team_two_sacks_player_name,
        "team_two_sacks_player_position": team_two_sacks_player_position,
        "team_two_player_two_sacks": team_two_player_two_sacks,
        "team_one_tackles_player_image": team_one_tackles_player_image,
        "team_one_tackles_player_name": team_one_tackles_player_name,
        "team_one_tackles_player_position": team_one_tackles_player_position,
        "team_one_tackles_player_game_state": team_one_tackles_player_game_state,
        "team_one_player_one_tackles": team_one_player_one_tackles,
        "team_two_tackles_player_image": team_two_tackles_player_image,
        "team_two_tackles_player_name": team_two_tackles_player_name,
        "team_two_tackles_player_position": team_two_tackles_player_position,
        "team_two_tackles_player_game_state": team_two_tackles_player_game_state,
        "team_two_player_two_tackles": team_two_player_two_tackles,
        "team_one_total_yards": team_one_total_yards,
        "team_two_total_yards": team_two_total_yards,
        "team_one_total_turnovers": team_one_total_turnovers,
        "team_two_total_turnovers": team_two_total_turnovers,
        "team_one_first_downs": team_one_first_downs,
        "team_two_first_downs": team_two_first_downs,
        "team_one_penalties": team_one_penalties,
        "team_two_penalties": team_two_penalties,
        "team_one_third_down": team_one_third_down,
        "team_two_third_down": team_two_third_down,
        "team_one_forth_down": team_one_forth_down,
        "team_two_forth_down": team_two_forth_down,
        "team_one_red_zone": team_one_red_zone,
        "team_two_red_zone": team_two_red_zone,
        "team_one_possession": team_one_possession,
        "team_two_possession": team_two_possession, 
        "game_status": game_status,
    }
