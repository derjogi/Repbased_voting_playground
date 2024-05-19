import unittest
from Vote import *
from Definitions import Voter

class TestPopularityContest(unittest.TestCase):

    def test_single_vote(self):
        sample = [Voter(CANDIDATES['C1'])]
        result = popularity_contest(sample)
        self.assertEqual(result, "C1")

    def test_tie(self):
        sample = [Voter(CANDIDATES["C1"]), 
                  Voter(CANDIDATES["C2"])]
        result = popularity_contest(sample)
        self.assertIn(result, ['C1', 'C2'])

    def test_multiple_votes(self):
        sample = [Voter(CANDIDATES["C1"]), 
                  Voter(CANDIDATES["C1"]), 
                  Voter(CANDIDATES["C2"])]
        result = popularity_contest(sample)
        self.assertEqual(result, 'C1')

    def test_single_choice_vote(self):
        pass # TODO

    def test_voters_with_weighing_mechanism(self):
        voters = [Voter("C1", {'C1': 0.8, 'C2': 0.2}),
                  Voter(CANDIDATES["C2"], {'C1': 0.1, 'C2': 0.9})]
        voters = popularity_contest(sample)
        self.assertEqual(result, 'C1')

    def test_popularity_with_weighted(self):
        sample = [
            Voter({
                    'C1': 0.8, 
                    'C2': 0.2
                }),
            Voter({
                    'C1': 0.1, 
                    'C2': 0.9
                }), 
            Voter({
                    'C2': 0.5, 
                    'C3': 0.4,
                    'C4': 0.1
                }), 
        ]
        self.assertEqual(popularity_contest(sample), 'C2')

### Tests that are disabled because of pyvoting package issues
    # def test_weighted_vote_fails_with_equal_first_place(self):
    #     votes = [
    #         Voter({
    #             CANDIDATES["C1"]: 3, 
    #             CANDIDATES['C2']: 1,    # <-- 
    #             CANDIDATES['C3']: 4,
    #             CANDIDATES['C4']: 2,
    #             }),
    #         Voter({
    #             CANDIDATES["C1"]: 1,    # <--
    #             CANDIDATES['C2']: 2,
    #             CANDIDATES['C3']: 3,
    #             CANDIDATES['C4']: 4,
    #             })
    #     ]

    #     results = ranked_choice(votes)
    #     # Both C1 & C2 are first place
    #     self.assertEqual(results[0][1], results[1][1])
    #     self.assertEqual(results[0][1], 1)


    # def test_weighted_vote(self):
    #     votes = [
    #         Voter({'C1': 3, 'C2': 1, 'C3': 4, 'C4': 2}),
    #         Voter({'C1': 2, 'C2': 1, 'C3': 4, 'C4': 3}),
    #         Voter({'C1': 1, 'C2': 2, 'C3': 4, 'C4': 3}),
    #         Voter({'C1': 4, 'C2': 3, 'C3': 2, 'C4': 1})
    #     ]

    #     results = ranked_choice(votes)
    #     self.assertEqual(results[0][0], 'C2')

    # def test_tier_list_vote(self):
    #     votes = [
    #         Voter({'C1': 3, 'C2': 1, 'C3': 4, 'C4': 2}),
    #         Voter({'C1': 2, 'C2': 1, 'C3': 4, 'C4': 3}),
    #         Voter({'C1': 1, 'C2': 2, 'C3': 4, 'C4': 3}),
    #         Voter({'C1': 4, 'C2': 3, 'C3': 2, 'C4': 1})
    #     ]

    #     results = tier_list_voting(votes)
    #     self.assertEqual(results[0][0], 'C2')

    # def test_tier_list_with_random_votes(self):
        
    #     votes = Testdata.getRandomVoters(100, 4)
    #     results = tier_list_voting(votes)
    #     self.assertLess(results[0][1], results[1][1])


if __name__ == '__main__':
    unittest.main()
