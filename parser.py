import json
from pathlib import Path


def load_candidates(file_path):
    candidates = []

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                candidate = json.loads(line)
                candidates.append(candidate)

            except json.JSONDecodeError:
                print(f"Skipping invalid JSON at line {line_number}")

    return candidates


if __name__ == "__main__":

    dataset_path = "data/candidates.jsonl"

    candidates = load_candidates(dataset_path)

    print(f"Loaded {len(candidates)} candidates.")
    print("First Candidate ID:", candidates[0]["candidate_id"])