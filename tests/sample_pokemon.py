# Sample pokemon with attributes covered by this package
SAMPLE_POKEMON = {
    "id": 999,
    "name": "sample",
    "height": 200.2,
    "weight": 201.2,
    "base_experience": 200,
    "types": [{"type": {"name": "type_1"}}, {"type": {"name": "type_2"}}],
    "stats": [
        {"base_stat": 1, "stat": {"name": "hp"}},
        {"base_stat": 2, "stat": {"name": "attack"}},
        {"base_stat": 3, "stat": {"name": "defense"}},
        {"base_stat": 4, "stat": {"name": "special-attack"}},
        {"base_stat": 5, "stat": {"name": "special-defense"}},
        {"base_stat": 6, "stat": {"name": "speed"}},
    ],
    "abilities": [
        {"ability": {"name": "ability_1"}, "is_hidden": True},
        {"ability": {"name": "ability_2"}, "is_hidden": False},
    ],
    "moves": [
        {
            "move": {"name": "move_1"},
            "version_group_details": [
                {
                    "level_learned_at": 0,
                    "move_learn_method": {"name": "tutor"},
                    "version_group": {"name": "game_1"},
                },
                {
                    "level_learned_at": 5,
                    "move_learn_method": {"name": "level-up"},
                    "version_group": {"name": "game_2"},
                },
            ],
        }
    ],
    "sprites": {
        "back_default": "default_back_url",
        "back_female": None,
        "back_shiny": "shiny_back_url",
        "back_shiny_female": None,
        "front_default": "default_front_url",
        "front_female": None,
        "front_shiny": "front_shiny_url",
        "front_shiny_female": None,
    },
}
