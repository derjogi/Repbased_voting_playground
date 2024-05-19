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
# * CandidateWeight is a dictionary with the candidate's ID as key and associated weight
# * FellowshipWeight is a dictionary with the candidate's FellowshipCandidate as key and associated weight
# * WeightedVote is the most complete object wrapped around the FellowshipWeight.

SingleCandidate: TypeAlias = str
RankedCandidates: TypeAlias = List[str]
CandidateWeight: TypeAlias = Dict[str, float]
FellowshipWeight: TypeAlias = Dict[FellowshipCandidate, float]
class WeightedVote:
    def __init__(self, candidate_weights: Dict[FellowshipCandidate, float]):
        self.candidate_weights = candidate_weights

    def __repr__(self):
        return f"WeightedVote({self.candidate_weights})"

# A vote can either be a single FellowshipCandidate, or a WeightedVote.
Vote = Union[SingleCandidate, RankedCandidates, FellowshipWeight, CandidateWeight, FellowshipCandidate, WeightedVote]

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

    def as_weighted_vote(self, vote: Vote) -> WeightedVote:
        # Go through the different shapes of a vote, and build them up to a propper WeightedVote
        if isinstance(vote, str):
            return WeightedVote({FellowshipCandidate(vote): 1}) # Assign a weight of 1, all others will implicitly have 0
        elif isinstance(vote, FellowshipCandidate):
            return WeightedVote({vote: 1})  # Assign a weight of 1, all others will implicitly have 0
        elif isinstance(vote, list):
            as_weighted = {}
            for i, candidate in enumerate(reversed(vote)):
                if isinstance(candidate, str):
                    as_weighted[FellowshipCandidate(candidate)] = i + 1     # Assign increasing weights such that first candidate gets the highest weight
                else:
                    as_weighted[candidate] = i + 1
            return WeightedVote(as_weighted)
        elif isinstance(vote, dict):
            # Different dict shapes are possible here (unfortunately we can't check for a TypeAlias).
            # Convert the dict to a valid WeightedVote per candidate
            vote_w_candidates = {}
            for k, v in vote.items():
                if isinstance(k, str):
                    vote_w_candidates[FellowshipCandidate(k)] = v
                else:
                    vote_w_candidates[k] = v
            return WeightedVote(vote_w_candidates)
        elif isinstance(vote, WeightedVote):
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

    def normalize(self, vote: Vote) -> WeightedVote:
        """
        Normalizes a vote to ensure that all votes 
            * have a weight
            * the weight adds up to 1 
            * the preferred candidate is ranked first
        """

        weighted_vote = self.as_weighted_vote(vote)

        normalized = {}
        total_weight = sum(weighted_vote.candidate_weights.values())
        for candidate in weighted_vote.candidate_weights:
            normalized[candidate] = weighted_vote.candidate_weights[candidate]/total_weight
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
        # Just get the list of candidates in order, no actual weights needed
        return [candidate for candidate in self.weighted_vote.items()]
    
    def get_weighted(self):
        """
        Returns a dictionary of candidates and their weights.
        """
        return self.weighted_vote


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

