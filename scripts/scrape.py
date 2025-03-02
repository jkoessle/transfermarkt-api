import requests
from tqdm import tqdm


BASE_URL = "http://localhost:8000" # adjust


def get_club_ids_per_league(league_ids: list[str]) -> list[str]:
    club_ids = []
    for league_id in tqdm(league_ids, unit="Leagues"):
        # call api with league_id
        response = requests.get(f"{BASE_URL}/competitions/{league_id}/clubs").json()
        for club in response["clubs"]:
            club_ids.append(club["id"])

    return club_ids


def get_player_ids_per_club(club_ids: list[str]) -> list[str]:
    player_ids = []
    for club_id in tqdm(club_ids, unit="Clubs"):
        # call api with club_id
        response = requests.get(f"{BASE_URL}/clubs/{club_id}/players").json()
        for player in response["players"]:
            player_ids.append(player["id"])

    return player_ids


def get_player_profiles(player_ids: list[str]) -> list[dict]:
    player_profiles = []
    for player_id in player_ids:
        # call profile api with player_id
        profile_response = requests.get(f"{BASE_URL}/players/{player_id}/profile").json()
        # call transfer api with player_id
        transfer_response = requests.get(f"{BASE_URL}/players/{player_id}/transfers").json()

        profile_response["transfers"] = transfer_response["transfers"]
        profile_response["youthClubs"] = transfer_response["youthClubs"]

        player_profiles.append(profile_response)

    return player_profiles



def main():

    league_ids = [
        "L1",  # 1. Bundesliga
        "L2",  # 2. Bundesliga
        "ES1",  # LaLiga
        "GB1",  # Premier League
        "IT1",  # Serie A
        "FR1",  # Ligue 1
    ]

    league_ids = ["L1"]

    club_ids = get_club_ids_per_league(league_ids=league_ids)

    print("Number of clubs: ", len(club_ids))

    player_ids = get_player_ids_per_club(club_ids=club_ids)

    print("Number of players: ", len(player_ids))


if __name__ == "__main__":
    main()