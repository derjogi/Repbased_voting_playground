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
    
    def test_no_tied_winners(self):
        pass # TODO; currently happens with default RCV & TLV!

    def test_no_evaluation_below_100_ballots(self):
        pass # TODO

    def test_80_percent_students_cant_outweigh_20_percent_teachers(self):
        pass # TODO

    def test_25_percent_teachers_cant_outweigh_75_percent_students(self):
        pass # TODO

if __name__ == '__main__':
    unittest.main()
