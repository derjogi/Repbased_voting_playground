import copy
import random
from Definitions import *


# The eligible candidates.
# For now, let's just assume that they all fulfill the requirements.
# In future, a list of a candidate's proven accomplishments could be used by a voting algorithm.
CANDIDATES = {
    "C1": FellowshipCandidate("C1", [Accomplishments.FULFILLED_ALL_REQUIREMENTS]),
    "C2": FellowshipCandidate("C2", [Accomplishments.FULFILLED_ALL_REQUIREMENTS]),
    "C3": FellowshipCandidate("C3", [Accomplishments.FULFILLED_ALL_REQUIREMENTS]),
    "C4": FellowshipCandidate("C4", [Accomplishments.FULFILLED_ALL_REQUIREMENTS]),
}

candidate_names = list(CANDIDATES.keys())

def getSample():
    # Sample voter data.
    # Each voter has voted for a specific candidate. Different voters have different proven qualifications.
    # One voter in the sample is a fellowship candidate. Should they be allowed to vote?
    return [
        Voter(CANDIDATES["C1"], []),
        Voter(CANDIDATES["C1"], [NFT.FELLOWSHIP_COMM, NFT.FUNDA_1, NFT.FUNDA_2, NFT.FUNDA_3, NFT.FUNDA_4, NFT.FUNDA_4, NFT.FUNDA_5, NFT.FUNDA_LEGACY]),
        Voter(CANDIDATES["C2"], [], isCandidate = True),
        Voter(CANDIDATES["C3"], [NFT.FUNDA_1]),
        Voter(CANDIDATES["C4"], [NFT.FUNDA_1, NFT.FUNDA_2]),
        Voter(CANDIDATES["C3"], [NFT.ETHCC_TE_2023_BARCAMP_SPEAKER]),
        Voter(CANDIDATES["C1"], [NFT.STUDY_SEASON_REGISTRATION, NFT.LIVE_TRACK_4, NFT.WONDERVERSE_TOP50]),
        Voter(CANDIDATES["C4"], [NFT.STUDY_SEASON_REGISTRATION]),
        Voter(CANDIDATES["C2"], [NFT.STUDY_SEASON_REGISTRATION, NFT.LIVE_TRACK_1, NFT.LIVE_TRACK_2]),
        Voter(CANDIDATES["C4"], []),
    ]

def getRandomVoters(num_voters = 100, num_candidates = 4):
    """
    Generates a random set of n voters.
    
    Args:
        num_voters (int): The number of voters to generate.
        num_candidates (int): The number of candidates.
        
    Returns:
        list: A list of n randomly generated Voter objects.
    """
    voters = []
    candidates = [FellowshipCandidate(f"C{i+1}") for i in range(num_candidates)]
    
    for _ in range(num_voters):
        # generate a weighted vote; if the election mechanism doesn't support 
        #  weighted votes, the candidate with the highest weight will be returned
        candidate_weights = {candidate: random.random() for candidate in candidates}
        weights = DistributedVote(candidate_weights)
        nfts = random.sample(list(NFT), random.randint(0, len(NFT)))
        
        try:
            voter = Voter(weights, nfts)
            voters.append(voter)
        except Exception as e:
            print(f"Error creating voter: {e}")
    
    return voters
