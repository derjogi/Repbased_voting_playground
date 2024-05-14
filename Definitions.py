from enum import Enum
import pandas as pd
from typing import Dict, Union, TypeAlias

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

class WeightedVote:
    def __init__(self, candidate_weights: Dict[FellowshipCandidate, float]):
        self.candidate_weights = candidate_weights

    def __repr__(self):
        return f"WeightedVote({self.candidate_weights})"

CandidateWeight: TypeAlias = Dict[str, float]
FellowshipWeight: TypeAlias = Dict[FellowshipCandidate, float]

# A vote can either be a single FellowshipCandidate, or a WeightedVote.
Vote = Union[FellowshipWeight, CandidateWeight, FellowshipCandidate, WeightedVote]

class Voter:

    def __init__(self, vote: Vote, nfts = [], hasTeaAccount = True, hasWalletConnected = True, isCandidate = False):
        if isinstance(vote, dict):
            vote_w_candidates = {}
            for k, v in vote.items():
                if isinstance(k, str):
                    vote_w_candidates[FellowshipCandidate(k)] = v
                else:
                    vote_w_candidates[k] = v
            vote = vote_w_candidates
            vote = WeightedVote(vote)
        if isinstance(vote, WeightedVote):
            # sanitize weights so they're proportional 
            # in case there's a voting mechanism that allows arbitrary numbers.)
            total_weight = sum(vote.candidate_weights.values())
            for candidate in vote.candidate_weights:
                vote.candidate_weights[candidate] /= total_weight
            self.weighted_vote = vote
            # If this is used with simple voting:
            self.vote = max(vote.candidate_weights, key=vote.candidate_weights.get)
        elif isinstance(vote, FellowshipCandidate):
            self.vote = vote
        else:
            raise Exception(
                """
                Invalid vote!\n
                Either provide a FellowshipCandidate (e.g. 'C1'),\n 
                or a dictionary of candidates and their weights: \n
                '{{'C1':0.4, 'C2':0.6}}'
                """
                )        
        
        # List of NFTs that this voter holds. Must refer to the NFT enum. Ignore invalid NFTs.
        self.nfts = [nft for nft in nfts if nft in iter(NFT)] 

        # Voter has an TEA account. Must be True to participate in voting.
        self.hasTeaAccount = hasTeaAccount

        # Voter has connected their wallet. Must be true to participate in voting.
        self.hasWalletConnected = hasWalletConnected

        # Candidates are not allowed to vote (?)
        self.isCandidate = isCandidate

class Ballot:
    def __init__(self, voters: [Voter]):
        self.voters = voters
        ballot = {}
        for voter in voters:
            if hasattr(voter, 'weighted_vote'):
                for candidate, weight in voter.weighted_vote.candidate_weights.items():
                    ballot[candidate] = weight
        self.ballot = pd.Series(ballot)

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

