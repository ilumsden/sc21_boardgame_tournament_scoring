class Game:

    def __init__(self, name, max_ranking_points, number_of_scores,
                 num_player_range, placement_based):
        self.name = name
        self.max_ranking_points = max_ranking_points
        self.num_scores = number_of_scores
        assert num_player_range[1] >= num_player_range[0]
        self.num_player_range = num_player_range
        self.placement_based = placement_based

    def _invert_placing(self, placing, num_players):
        return num_players + 1 - placing

    def _get_max_points_for_ranking(self, num_players):
        factor = (num_players - self.num_player_range[0] + 1) / (self.num_player_range[1] - self.num_player_range[0] + 1)
        return self.max_ranking_points * factor

    def get_norm_score_no_placing(self, score, num_players, max_score):
        max_pts_for_ranking = self._get_max_points_for_ranking(num_players)
        return (score / max_score) * max_pts_for_ranking

    def get_norm_score_placing(self, placing, num_players):
        inv_placing = self._invert_placing(placing, num_players)
        max_pts_for_ranking = self._get_max_points_for_ranking(num_players)
        return max_pts_for_ranking * (inv_placing / num_players)

    @staticmethod
    def from_toml_dict(toml_dict):
        name = list(toml_dict.keys())[0]
        data = toml_dict[name]
        return Game(name, data["max_ranking_points"], data["number_of_scores"],
                    data["num_player_range"], data["placement_based"])

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        print(name)
