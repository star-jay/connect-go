from connect.controller.logic import (
    generate_board_from_moves,
    list_possible_combinations,
)
from connect.controller.settings import (
    ROWS,
    COLS,
    TARGET,
)
from .player import Player


class TrapBot(Player):
    # initieele waardes
    def startgame(self):
        self.nodes = {
            (row, col): {
                'combinations': [],
            } for row in range(ROWS) for col in range(COLS)
        }
        combinations = list_possible_combinations()
        for combination in combinations:
            for row, col in combination:
                self.nodes[row, col]['combinations'].append(combination)

        # self.scores_row = {row: 0 for row in self.list_r}
        # self.scores_row_opp = self.scores_row.copy()

        # self.node_rows = {}
        # for col in range(COLS):
        #     for row in range(ROWS):
        #         self.node_rows[(row, col)] = list(
        #             rij for rij in self.list_r if (row, col) in rij)

        # self.node_rows_opp = self.node_rows.copy()

        # self.blocked_cols = []
        # self.blocked_cols_opp = {}
        # self.target_cols = []


def values_for_combination(combination, nodes):
    values = {}
    for x in range(len(combination)-(TARGET-1)):
        combi = combination[x:x+TARGET]
        for row, col, value in combi:
            nodes.app



# def combi_scores(all_combinations, sign):
#     scores = {}
#     for combi in all_combinations:
#         values = values_for_combination(combi)
#         if values.count(revert_sign(SIGNS, sign)) > 0:
#             scores[combi] = 0
#         else:
#             scores[combi] = values.count(sign)

#     return scores
