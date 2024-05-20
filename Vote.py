import Testdata
import sys, os
# sys.path.append(os.path.abspath("../pyvoting"))
# import pyvoting as pv
import pandas as pd
from Definitions import Voter, FellowshipCandidate
from typing import Callable


CANDIDATES = Testdata.CANDIDATES

# A quick and dirty voting algorithm.
# Counts all votes and returns the id of the candidate who got the most votes.
# In case of a tie, the winning candidate with the lowest id will be returned.
# This algorithm completely ignores the proven qualifications of both candidates and voters.
def popularity_contest(voters: list[Voter], candidates: list[FellowshipCandidate] = CANDIDATES.values()):
    votecount = {}
    for candidate in candidates:
        votecount[candidate.id] = len([voter for voter in voters if voter.get_single_vote() == candidate])
    
    return sort(votecount)
    # return max(votecount, key=votecount.get)

def sort(results):
    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

def accumulated_scores_voting(voters: list[Voter], candidates: list[FellowshipCandidate] = CANDIDATES.values(), weighing_mechanism: Callable[[Voter], int] = None):
    candidate_scores = {}
    for voter in voters:
        for candidate, distribution in voter.get_distributed():
            id = candidate.id
            print(f'Voter voted for {id} with distribution {distribution}')
            if id not in candidate_scores:
                candidate_scores[id] = 0
            if weighing_mechanism is None:
                candidate_scores[id] += distribution
            else:
                candidate_scores[id] += weighing_mechanism(voter)
    return sort(candidate_scores)

# Unfortunately, the pyvoting package doesn't work as a package because of some broken imports.
# So I'll have to uncomment these methods for a bit until that is fixed.
# def ranked_choice(votes, candidates = Testdata.candidate_names):
#     election = pv.RankedChoiceVoting(candidates)
#     for voter in votes:
#         election.AddBallot(get_as_ballot(voter))
    
#     results = election.RunElection()
#     print(results)
#     return results

# def tier_list_voting(votes, candidates = Testdata.candidate_names):
#     election = pv.TierListVoting(candidates)
#     for voter in votes:
#         election.AddBallot(get_as_ballot(voter))
    
#     results = election.RunElection()
#     print(results)
#     return results

def get_as_ballot(voter) -> pd.Series:
    ballot = {}
    if hasattr(voter, 'weighted_vote'):
        for candidate, weight in voter.weighted_vote.candidate_weights.items():
            ballot[candidate.id] = weight
    return pd.Series(ballot)