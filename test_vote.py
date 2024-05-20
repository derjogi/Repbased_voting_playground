from Vote import *
from Definitions import Voter
import pytest

@pytest.fixture(params=["popularity", "score"])
def voting_mechanism(request):
    if request.param == "popularity":
        return popularity_contest
    elif request.param == "score":
        return accumulated_scores_voting

# def evaluate(voting_mechanism, result, expected):
#     if voting_mechanism == popularity_contest:
#         assert next(iter(result)) == 
#     elif voting_mechanism == accumulated_scores_voting:
#         return result

def test_single_vote(voting_mechanism):
    voters = [Voter(CANDIDATES['C1'])]
    result = voting_mechanism(voters)
    assert ('C1', 1.0) in result.items()
    
def test_tie(voting_mechanism):
    voters = [Voter('C1'), Voter('C2')]
    result = voting_mechanism(voters)
    assert result['C1'] == result['C2'], "Expected both 'C1' and 'C2' to have the same score"

def test_multiple_votes(voting_mechanism):
    sample = [Voter(CANDIDATES["C1"]), 
                Voter(CANDIDATES["C1"]), 
                Voter(CANDIDATES["C2"])]
    result = voting_mechanism(sample)
    assert ('C1', 2.0) in result.items()

def test_weighted(voting_mechanism):
    voters = [
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
    result = voting_mechanism(voters)
    print(result)
    assert 'C2' == list(result.keys())[0]
    assert result['C2'] in (1.6, 2)

def test_voters_with_decimal_scoring(voting_mechanism):
    voters = [Voter({'C1': 0.8, 'C2': 0.2}),
              Voter({'C1': 0.1, 'C2': 0.9})]
    result = voting_mechanism(voters)

    # In scored voting, C1 = 0.9, C2 = 1.1; C2 wins.
    if voting_mechanism == accumulated_scores_voting:
        assert 'C2' == list(result.keys())[0]
        assert ('C1', 0.9) in result.items()
        assert ('C2', 1.1) in result.items()
    
    # In popularity voting, C1 wins one, C2 the other, so they tie.
    elif voting_mechanism == popularity_contest:
        assert ('C1', 1.0) in result.items()
        assert ('C2', 1.0) in result.items()    

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
