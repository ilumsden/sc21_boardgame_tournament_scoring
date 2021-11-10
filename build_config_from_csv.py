import tomli_w
import pandas as pd
import argparse

import os

def main():
    parser = argparse.ArgumentParser(description="Convert a CSV file with the necessary column names into a\
                                                  TOML config file")
    parser.add_argument("csv_file", type=str,
                        help="The CSV file to parse")
    parser.add_argument("--config_id", "-c", type=str, default="User Config",
                        help="Set the config_id field of the configuration file")
    parser.add_argument("--dump_fname", "-f", type=str, default="./user_config.toml",
                        help="The path to where the TOML file should be created")
    args = parser.parse_args()
    df = pd.read_csv(os.path.abspath(parser.csv_file))
    config_data = {}
    config_data["config_id"] = args.config_id
    for _, row in df.iterrows():
        config_data[row["game_name"]] = {}
        config_data[row["game_name"]]["scheme"] = row["scheme"]
        config_data[row["game_name"]]["max_ranking_points"] = row["max_ranking_points"]
        config_data[row["game_name"]]["number_of_scores"] = row["number_of_scores"]
        config_data[row["game_name"]]["num_player_range"] = [row["min_num_player_range"], row["max_num_player_range"]]
    with open(os.path.abspath(args.dump_fname), "w") as f:
        tomli_w.dump(config_data, f)

if __name__ == "__main__":
    main()
