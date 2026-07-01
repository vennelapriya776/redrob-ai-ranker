from parser import load_candidates
from feature_extractor import extract_features

candidates = load_candidates("data/candidates.jsonl")

features = extract_features(candidates[0])

print(features)