import unittest
import Testdata
from Vote import *
from Definitions import FellowshipCandidate


class TestRequirements(unittest.TestCase):

    def test_single_winner(self):
        pass # TODO

    def test_candidates_cant_vote(self):
        pass # TODO

    def test_NFT_weights(self):
        pass # TODO

    def test_voters_without_nft_cant_vote(self):
        pass # TODO

    def test_voters_without_tea_account_cant_vote(self):
        pass # TODO

    def test_removing_candidate_does_not_change_ranking(self):        
        voters = Testdata.getRandomVoters(100, 6)
        candidates = list(set([voter.get_single_vote() for voter in voters]))
        print(candidates)
        results = popularity_contest(voters, candidates)
            
        candidates_in_order = [x for x in results]
        print('Order of candidates after first round: ', candidates_in_order)
        candidates_in_order.remove(candidates_in_order[2])

        # remove one candidate and check that the results are again the same after the vote:
        results = popularity_contest(voters, [FellowshipCandidate(c) for c in candidates_in_order])
        
        candidates_in_order_2 = [x for x in results]
        print('Order of candidates after second round: ', candidates_in_order_2)
        # Make sure that we do have the same order:
        self.assertEqual(candidates_in_order, candidates_in_order_2)  

    def test_weigthed_votes(self):
        voters = Testdata.getRandomVoters()
        results_no_weights = accumulated_scores_voting(voters)
        print('Results without NFT weights: ', results_no_weights)
        
        def weighing_mechanism(voter: Voter, id: str):
            return voter.get_weight_for(id) * len(voter.nfts)

        results_with_weights = accumulated_scores_voting(voters, weighing_mechanism=weighing_mechanism)
        print('Results with NFT weights: ', results_with_weights)

        # The candidate order might have changed due to the different distribution of weights.
        # Not sure what we can actually test here properly, except for that all the weights shold be higher...
        
        # First, get all candidates, then we can access them and compare:
        candidates = [candidate for candidate in results_no_weights]

        for candidate in candidates:
            assert results_no_weights[candidate] < results_with_weights[candidate]

    def test_no_tied_winners(self):
        pass # TODO; currently with default RCV & TLV they're often tied if there are only a few voters!

    def test_no_evaluation_below_100_ballots(self):
        pass # TODO

    def test_80_percent_students_cant_outweigh_20_percent_teachers(self):
        pass # TODO

    def test_25_percent_teachers_cant_outweigh_75_percent_students(self):
        pass # TODO

if __name__ == '__main__':
    unittest.main()
