import json

game = {
    "game_id": None,
    "game_name": None,
    "game_info": None,
    "game_admin": None,
    "game_rules": {
        "initial_amount": None,
        "steps": None,
        "step_time": None,
        "other_rules": None
    },
    "assets": [
        {
            "asset_type": None,
            "asset_listing": None,
            "asset_name": None,
            "asset_values": [None, None]
        },
        {
            "asset_type": None,
            "asset_listing": None,
            "asset_name": None,
            "asset_values": [None, None]
        }
    ],
    "news": [
        {
            "related_asset": None,
            "news_text": None,
            "news_values": [None, None]
        },
        {
            "related_asset": None,
            "news_text": None,
            "news_values": [None, None]
        }
    ],
    "players": [
        {
            "player_id": None,
            "amount": None,
            "amount_changing": None,
            "players_assets": [
                {
                    "asset_listing": None,
                    "players_asset_values": [None, None]
                },
                {
                    "asset_listing": None,
                    "players_asset_values": [None, None]
                }
            ]
        }
    ]
}

print(game)
with open('test.json', 'w') as outfile:
    json.dump(game, outfile)