import unittest
import Testdata
from Vote import *


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
        ballots = Testdata.getRandomVotes(100, 6)
        candidates = list(set([ballot.vote.id for ballot in ballots]))
        print(candidates)
        results = tier_list_voting(ballots, candidates)
        
        # Just make sure that we do have a distinct order:
        for i in range(len(results)-1):
            self.assertLess(results[i][1], results[i+1][1])
            
        candidates_in_order = [x[0] for x in results]
        print('Order of candidates after first round: ', candidates_in_order)
        one_candidate_less = candidates_in_order.copy()
        one_candidate_less.remove(one_candidate_less[3])

        # remove one candidate and check that the results are again the same after the vote:
        results = tier_list_voting(ballots, one_candidate_less)
        
        candidates_in_order_2 = [x[0] for x in results]
        print('Order of candidates after second round: ', candidates_in_order_2)
        # Make sure that we do have the same order:
        for i in range(len(results)-1):
            self.assertLess(results[i][1], results[i+1][1])
            self.assertEqual(results[i][0], one_candidate_less[i])  
    
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
