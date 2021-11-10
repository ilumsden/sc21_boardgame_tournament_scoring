class Game:

    def __init__(self, name, scheme, max_ranking_points,
                 number_of_scores, num_player_range):
        self.name = name
        self.max_ranking_points = max_ranking_points
        self.num_scores = number_of_scores
        assert num_player_range[1] >= num_player_range[0]
        self.num_player_range = num_player_range
        self.scheme_table = {
            "num_player_no_placing": Game.get_norm_score_no_placing,
            "num_player_placing": Game.get_norm_score_placing,
            "top_three": Game.get_norm_score_top_three_ranking,
        }
        self.current_scheme = "top_three"

    def set_scheme(self, scheme):
        if scheme not in list(self.scheme_table.keys()):
            raise ValueError("Invalid Scheme")
        self.current_scheme = scheme

    def get_norm_score(self, placing_or_score, **kwargs):
        return self.scheme_table[self.current_scheme](self, placing_or_score, **kwargs)

    def _invert_placing(self, placing, num_players):
        return num_players + 1 - placing

    def _get_max_points_for_ranking(self, num_players):
        factor = (num_players - self.num_player_range[0] + 1) / (self.num_player_range[1] - self.num_player_range[0] + 1)
        return self.max_ranking_points * factor

    def get_norm_score_no_placing(self, score, **kwargs):
        num_players = kwargs["num_players"]
        max_score = kwargs["max_score"]
        max_pts_for_ranking = self._get_max_points_for_ranking(num_players)
        return (score / max_score) * max_pts_for_ranking

    def get_norm_score_placing(self, placing, **kwargs):
        num_players = kwargs["num_players"]
        inv_placing = self._invert_placing(placing, num_players)
        max_pts_for_ranking = self._get_max_points_for_ranking(num_players)
        return max_pts_for_ranking * (inv_placing / num_players)

    def get_norm_score_top_three_ranking(self, placing, **kwargs):
        if placing == 1:
            return 6
        if placing == 2:
            return 4
        if placing == 3:
            return 3
        return 2

    @staticmethod
    def from_toml_dict(toml_dict):
        name = list(toml_dict.keys())[0]
        data = toml_dict[name]
        return Game(name, data["scheme"], data["max_ranking_points"],
                    data["number_of_scores"], data["num_player_range"])

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name
