class Game:

    def __init__(self, name, max_ranking_points, number_of_scores, number_of_players, placement_based):
        self.name = name
        self.max_ranking_points = max_ranking_points
        self.num_scores = number_of_scores
        self.number_of_players = number_of_players
        self.placement_based = placement_based

    def invert_placing(self, placing):
        return self.number_of_players + 1 - placing

    def get_norm_score_no_placing(self, score, max_score):
        return (score / max_score) * self.max_ranking_points

    def get_norm_score_placing(self, placing):
        inv_placing = self.invert_placing(placing)
        return (self.max_ranking_points / self.number_of_players) * inv_placing

    @staticmethod
    def from_toml_dict(toml_dict):
        name = list(toml_dict.keys())[0]
        data = toml_dict[name]
        return Game(name, data["max_ranking_points"], data["number_of_scores"],
                    data["number_of_players"], data["placement_based"])

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        print(name)
