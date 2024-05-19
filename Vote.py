import Testdata
import sys, os
# sys.path.append(os.path.abspath("../pyvoting"))
# import pyvoting as pv
import pandas as pd
from Definitions import Voter, FellowshipCandidate


CANDIDATES = Testdata.CANDIDATES

# A quick and dirty voting algorithm.
# Counts all votes and returns the id of the candidate who got the most votes.
# In case of a tie, the winning candidate with the lowest id will be returned.
# This algorithm completely ignores the proven qualifications of both candidates and voters.
def popularity_contest(voters: list[Voter], candidates: list[FellowshipCandidate] = CANDIDATES.values()):
    votecount = {}
    for candidate in candidates:
        votecount[candidate.id] = len([voter for voter in voters if voter.get_single_vote() == candidate])
    
    return dict(sorted(votecount.items(), key=lambda x: x[1], reverse=True))
    # return max(votecount, key=votecount.get)

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