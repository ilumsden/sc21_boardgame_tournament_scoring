from .game import Game

import pandas as pd
import tomli

def import_games_from_toml(toml_file):
    toml_file_dict = None
    with open(toml_file, "r") as f:
        toml_file_dict = tomli.load(f)
    if toml_file_dict is None:
        raise RuntimeError("Could not load TOML config file")
    config_name = toml_file_dict["config_id"]
    print("Importing Game Data for {}!".format(config_name))
    del toml_file_dict["config_id"]
    games = []
    for k in toml_file_dict.keys():
        toml_game_dict = {k: toml_file_dict[k]}
        games.append(Game.from_toml_dict(toml_game_dict))
    return games

def split_score_df_by_game(score_df, games):
    per_game_dfs = {}
    for g in games:
        per_game_dfs[g] = score_df.loc[score_df["game"] == g.name]
    return per_game_dfs

def get_max_scores_no_placing(per_game_dfs, games):
    max_scores = {}
    for g in games:
        if not g.placement_based:
            max_scores[g] = per_game_dfs[g]["score"].max()
    return max_scores

def get_normalized_scores(per_game_dfs, max_scores, games):

    def _eval_norm_score_placing(game, row):
        placing = row["score"]
        num_players = row["num_players"]
        row["score"] = game.get_norm_score_placing(placing, num_players)
        return row

    def _eval_norm_score_no_placing(game, max_score, row):
        score = row["score"]
        num_players = row["num_players"]
        row["score"] = game.get_norm_score_no_placing(score, num_players, max_score)
        return row

    normed_per_game_dfs = {}
    for g in games:
        normed_per_game_dfs[g] = per_game_dfs[g].copy()
        if g.placement_based:
            # normed_per_game_dfs[g]["score"] = normed_per_game_dfs[g]["score"].apply(
            #     lambda x: g.get_norm_score_placing(x)
            # )
            normed_per_game_dfs[g] = normed_per_game_dfs[g].apply(
                lambda row: _eval_norm_score_placing(g, row),
                axis=1
            )
        else:
            max_score = max_scores[g]
            # normed_per_game_dfs[g]["score"] = normed_per_game_dfs[g]["score"].apply(
            #     lambda x: g.get_norm_score_no_placing(x, max_score)
            # )
            normed_per_game_dfs[g] = normed_per_game_dfs[g].apply(
                lambda row: _eval_norm_score_no_placing(g, max_score, row),
                axis=1
            )
    return normed_per_game_dfs

def get_final_counted_scores_df(normed_per_game_dfs, games):
    counted_scores_per_game_dfs = {}
    for g in games:
        df = normed_per_game_dfs[g]
        data = []
        for name in df["name"].unique():
            row = {}
            row["name"] = name
            sorted_array = df.loc[df["name"] == name]["score"].to_numpy()
            sorted_array.sort()
            for i in range(g.num_scores):
                row["{}:score{}".format(g.name, i)] = sorted_array[-1 - i]
            data.append(row)
        counted_scores_per_game_dfs[g] = pd.DataFrame(data)
        counted_scores_per_game_dfs[g].set_index("name", inplace=True)
    full_counted_df = pd.concat([d for _, d in counted_scores_per_game_dfs.items()], axis=1)
    return full_counted_df
