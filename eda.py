from collections import Counter
from parser import load_candidates

print("Loading candidates...")
candidates = load_candidates("data/candidates.jsonl")
print(f"Loaded {len(candidates)} candidates.\n")

# -------------------------
# Years of Experience
# -------------------------
experience = []

# -------------------------
# Current Titles
# -------------------------
titles = Counter()

# -------------------------
# Industries
# -------------------------
industries = Counter()

# -------------------------
# Skills
# -------------------------
skills = Counter()

# -------------------------
# Open To Work
# -------------------------
open_to_work = 0

for candidate in candidates:

    profile = candidate["profile"]
    signals = candidate["redrob_signals"]

    experience.append(profile["years_of_experience"])

    titles[profile["current_title"]] += 1

    industries[profile["current_industry"]] += 1

    if signals["open_to_work_flag"]:
        open_to_work += 1

    for skill in candidate["skills"]:
        skills[skill["name"]] += 1


print("=" * 60)

print("Average Experience:")
print(round(sum(experience) / len(experience), 2), "years")

print("\nTop 20 Current Titles:")
for title, count in titles.most_common(20):
    print(f"{title}: {count}")

print("\nTop 20 Skills:")
for skill, count in skills.most_common(20):
    print(f"{skill}: {count}")

print("\nTop 20 Industries:")
for industry, count in industries.most_common(20):
    print(f"{industry}: {count}")

print("\nOpen To Work Candidates:")
print(open_to_work)