from parser import load_candidates

candidates = load_candidates("data/candidates.jsonl")

candidate = candidates[0]

print("=" * 60)

print("Candidate ID:")
print(candidate["candidate_id"])

print("\nProfile:")
print(candidate["profile"])

print("\nCareer History:")
print(candidate["career_history"])

print("\nEducation:")
print(candidate["education"])

print("\nSkills:")
print(candidate["skills"])

print("\nSignals:")
print(candidate["redrob_signals"])