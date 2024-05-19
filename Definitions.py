from enum import Enum
import pandas as pd
from typing import List, Dict, Union, TypeAlias

class Accomplishments(Enum):

    FULFILLED_ALL_REQUIREMENTS = 1,     # More accomplishments could be defined and used by the voting algorithm...

class FellowshipCandidate:

    def __init__(self, id, accomplishments = [Accomplishments.FULFILLED_ALL_REQUIREMENTS]):

        self.id = id

        # The candidate's proven accomplishments. Must refer to the Accomplishments enum. Ignore invalid accomplishments.
        self.accomplishments = [acc for acc in accomplishments if acc in iter(Accomplishments)]
    
    def __eq__(self, other):
        return (self.id == other.id)
    
    def __hash__(self) -> int:
        return hash(self.id)


# There are different ways to specify a 'valid' vote, we want to make sure that we let typical ones pass.
# All of these are ultimately converted to a WeightedVote object.
# * SingleCandidate is the easiest with just the ID or a FellowshipCandidate object and no weights
# * RankedCandidates just has a list of candidate IDs in order
# * CandidateDistribution is a dictionary with the candidate's ID as key and the distribution (weight/percentage that is given to that candidate (always relative to other candidates))
# * FellowshipDistribution is a dictionary with the candidate's FellowshipCandidate as key and associated distribution
# * DistributedVote is the most complete object wrapped around the FellowshipDistribution.

SingleCandidate: TypeAlias = str
RankedCandidates: TypeAlias = List[str]
CandidateDistribution: TypeAlias = Dict[str, float]
FellowshipDistribution: TypeAlias = Dict[FellowshipCandidate, float]
class DistributedVote:
    def __init__(self, distributed_vote: Dict[FellowshipCandidate, float]):
        self.distributed_vote = distributed_vote

    def __repr__(self):
        return f"DistributedVote({self.distributed_vote})"

# A vote is the union of DistributedVote and all the simpler variants
Vote = Union[SingleCandidate, RankedCandidates, FellowshipDistribution, CandidateDistribution, FellowshipCandidate, DistributedVote]

class Voter:

    def __init__(self, vote: Vote, nfts = [], hasTeaAccount = True, hasWalletConnected = True, isCandidate = False):
        self.normalized_vote = self.normalize(vote)
        
        # List of NFTs that this voter holds. Must refer to the NFT enum. Ignore invalid NFTs.
        self.nfts = [nft for nft in nfts if nft in iter(NFT)] 

        # Voter has an TEA account. Must be True to participate in voting.
        self.hasTeaAccount = hasTeaAccount

        # Voter has connected their wallet. Must be true to participate in voting.
        self.hasWalletConnected = hasWalletConnected

        # Candidates are not allowed to vote (?)
        self.isCandidate = isCandidate

    def as_distributed_vote(self, vote: Vote) -> DistributedVote:
        # Go through the different shapes of a vote, and build them up to a propper WeightedVote
        if isinstance(vote, str):
            return DistributedVote({FellowshipCandidate(vote): 1}) # Assign a weight of 1, all others will implicitly have 0
        elif isinstance(vote, FellowshipCandidate):
            return DistributedVote({vote: 1})  # Assign a weight of 1, all others will implicitly have 0
        elif isinstance(vote, list):
            as_weighted = {}
            for i, candidate in enumerate(reversed(vote)):
                if isinstance(candidate, str):
                    as_weighted[FellowshipCandidate(candidate)] = i + 1     # Assign increasing weights such that first candidate gets the highest weight
                else:
                    as_weighted[candidate] = i + 1
            return DistributedVote(as_weighted)
        elif isinstance(vote, dict):
            # Different dict shapes are possible here (unfortunately we can't check for a TypeAlias).
            # Convert the dict to a valid WeightedVote per candidate
            vote_w_candidates = {}
            for k, v in vote.items():
                if isinstance(k, str):
                    vote_w_candidates[FellowshipCandidate(k)] = v
                else:
                    vote_w_candidates[k] = v
            return DistributedVote(vote_w_candidates)
        elif isinstance(vote, DistributedVote):
            return vote
        else:
            raise Exception(
                """
                Invalid vote!\n
                Provide a FellowshipCandidate (e.g. 'C1'),\n 
                or a dictionary of candidates and their weights: \n
                '{{'C1':0.4, 'C2':0.6}}'
                """
                )    

    def normalize(self, vote: Vote) -> DistributedVote:
        """
        Normalizes a vote to ensure that all votes 
            * have a distribution
            * the distribution adds up to 1 
            * if there's a weighing_mechanism, the weight is calculated based on the NFTs and calculated with the normalized distribution
            * the preferred candidate is ranked first
        """

        vote = self.as_distributed_vote(vote)

        normalized = {}
        summed = sum(vote.distributed_vote.values())
        for candidate in vote.distributed_vote:
            normalized[candidate] = vote.distributed_vote[candidate]/summed
        sorted_candidates = sorted(normalized.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_candidates

    def get_single_vote(self):
        """
        Returns the single candidate that this voter voted for. If the voter voted for multiple candidates, this will return the first/highest rated one.
        """
        return self.normalized_vote[0][0]
    
    def get_ranked(self):
        """
        Returns a list of candidates that this voter voted for, ordered by their weight with the best candidate first.
        """
        # Just get the list of candidates in order, no actual distribution needed
        return [candidate for candidate in self.normalized_vote.items()]
    
    def get_distributed(self):
        """
        Returns a dictionary of candidates and their relative distributions.
        """
        return self.normalized_vote


class NFT(Enum):

    FUNDA_1 = 1                         # TE Fundamentals module 1
    FUNDA_2 = 2                         # TE Fundamentals module 2
    FUNDA_3 = 3                         # TE Fundamentals module 3
    FUNDA_4 = 4                         # TE Fundamentals module 4
    FUNDA_5 = 5                         # TE Fundamentals module 5
    FUNDA_LEGACY = 6                    # TE Fundamentals legacy NFT
    FELLOWSHIP_COMM = 7,                # Fellowship Committee member
    STUDY_SEASON_SPEAKER = 8,           # Study Season speaker
    ETHCC_TE_2023_BARCAMP_SPEAKER = 9,  # Speaker at EthCC TE 2023/Barcamp
    STUDY_SEASON_REGISTRATION = 10,     # Registered to Study Season
    WONDERVERSE_TOP50 = 11,             # Made it into top 50 on the Wonderverse leaderboard
    LIVE_TRACK_1 = 12,                  # Participated in Study Season live track 1
    LIVE_TRACK_2 = 13,                  # Participated in Study Season live track 2
    LIVE_TRACK_3 = 14,                  # Participated in Study Season live track 3
    LIVE_TRACK_4 = 15,                  # Participated in Study Season live track 4
    LIVE_TRACK_5 = 16,                  # Participated in Study Season live track 5 (Offered by candidate)
    LIVE_TRACK_6 = 17,                  # Participated in Study Season live track 6 (Offered by candidate)
    LIVE_TRACK_7 = 18,                  # Participated in Study Season live track 7 (Offered by candidate)
    LIVE_TRACK_8 = 19,                  # Participated in Study Season live track 8 (Offered by candidate)

