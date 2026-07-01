# rank.py

import csv
import heapq
import json
from pathlib import Path

from config import (
    CANDIDATE_FILE,
    SUBMISSION_FILE,
)

from feature_extractor import FeatureExtractor


class CandidateRanker:

    def __init__(self):

        self.extractor = FeatureExtractor()

        # Keep only Top 100 candidates
        self.top_k = 100

        self.heap = []

    # ----------------------------------------
    # Stream Candidates
    # ----------------------------------------

    def stream_candidates(self):

        with open(CANDIDATE_FILE, "r", encoding="utf8") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                try:
                    yield json.loads(line)

                except Exception:
                    continue

    # ----------------------------------------
    # Candidate Summary Text
    # ----------------------------------------

    def build_candidate_text(self, candidate):

        profile = candidate.get("profile", {})

        headline = profile.get("headline", "")

        summary = profile.get("summary", "")

        title = profile.get("current_title", "")

        history = candidate.get("career_history", [])

        history_text = []

        for job in history:

            history_text.append(
                f"{job.get('title','')} "
                f"{job.get('industry','')} "
                f"{job.get('description','')}"
            )

        return (
            headline
            + " "
            + summary
            + " "
            + title
            + " "
            + " ".join(history_text)
        ).lower()

    # ----------------------------------------
    # Product Company Detection
    # ----------------------------------------

    def product_company_score(self, candidate):

        history = candidate.get("career_history", [])

        score = 0

        product_words = [

            "saas",
            "software",
            "platform",
            "product",
            "marketplace",
            "fintech",
            "healthtech",
            "ecommerce",
            "e-commerce",
            "ai",
            "ml",
            "search"
        ]

        for job in history:

            industry = str(
                job.get("industry", "")
            ).lower()

            for word in product_words:

                if word in industry:

                    score += 1
                    break

        return min(score, 8)

    # ----------------------------------------
    # Ranking / Retrieval Relevance
    # ----------------------------------------

    def retrieval_relevance_score(self, candidate):

        text = self.build_candidate_text(candidate)

        keywords = [

            "retrieval",
            "ranking",
            "recommendation",
            "recommendation system",
            "search",
            "semantic search",
            "vector",
            "embedding",
            "embeddings",
            "information retrieval",
            "relevance",
            "matching",
            "candidate ranking",
            "retriever",
            "dense retrieval",
            "hybrid retrieval",
            "rag",
            "llm",
            "transformer",
            "bert",
            "ndcg",
            "mrr",
            "map",
            "evaluation",
            "ab testing"
        ]

        score = 0

        for kw in keywords:

            if kw in text:
                score += 1

        return min(score, 15)

    # ----------------------------------------
    # Title Relevance
    # ----------------------------------------

    def title_relevance_score(self, candidate):

        title = str(
            candidate
            .get("profile", {})
            .get("current_title", "")
        ).lower()

        strong_titles = [

            "ai engineer",
            "machine learning engineer",
            "ml engineer",
            "search engineer",
            "relevance engineer",
            "recommendation engineer",
            "nlp engineer",
            "applied scientist",
            "research engineer",
            "data scientist",
            "generative ai engineer"
        ]

        for t in strong_titles:

            if t in title:
                return 10

        return 0

    # ----------------------------------------
    # Experience Band Match
    # ----------------------------------------

    def experience_band_score(self, candidate):

        years = (
            candidate
            .get("profile", {})
            .get("years_of_experience", 0)
        )

        if 5 <= years <= 9:
            return 12

        if 4 <= years < 5:
            return 8

        if 9 < years <= 12:
            return 8

        return 3
        # ----------------------------------------
    # Career Stability Score
    # ----------------------------------------

    def career_stability_score(self, candidate):

        history = candidate.get("career_history", [])

        if not history:
            return 0

        total_duration = 0

        for job in history:

            total_duration += job.get("duration_months", 0)

        avg_duration = total_duration / len(history)

        if avg_duration >= 36:
            return 10

        elif avg_duration >= 24:
            return 8

        elif avg_duration >= 18:
            return 5

        return 2

    # ----------------------------------------
    # Education Score
    # ----------------------------------------

    def education_score(self, candidate):

        education = candidate.get("education", [])

        score = 0

        for edu in education:

            tier = str(
                edu.get("tier", "")
            ).lower()

            if tier == "tier_1":
                score = max(score, 10)

            elif tier == "tier_2":
                score = max(score, 7)

            elif tier == "tier_3":
                score = max(score, 5)

        return score

    # ----------------------------------------
    # Skill Quality Score
    # ----------------------------------------

    def skill_quality_score(self, candidate):

        skills = candidate.get("skills", [])

        score = 0

        proficiency_weight = {

            "expert": 4,
            "advanced": 3,
            "intermediate": 2,
            "beginner": 1
        }

        for skill in skills:

            p = str(
                skill.get("proficiency", "")
            ).lower()

            endorsements = skill.get(
                "endorsements",
                0
            )

            duration = skill.get(
                "duration_months",
                0
            )

            score += proficiency_weight.get(p, 0)

            score += min(duration / 24, 2)

            score += min(endorsements / 50, 2)

        return min(score, 25)

    # ----------------------------------------
    # Recency / Availability Score
    # ----------------------------------------

    def activity_score(self, candidate):

        signals = candidate.get(
            "redrob_signals",
            {}
        )

        score = 0

        if signals.get("open_to_work_flag"):
            score += 6

        score += min(
            signals.get(
                "profile_views_received_30d",
                0
            ) / 40,
            3
        )

        score += min(
            signals.get(
                "saved_by_recruiters_30d",
                0
            ) / 10,
            3
        )

        score += min(
            signals.get(
                "search_appearance_30d",
                0
            ) / 30,
            3
        )

        score += min(
            signals.get(
                "recruiter_response_rate",
                0
            ) * 5,
            5
        )

        score += min(
            signals.get(
                "interview_completion_rate",
                0
            ) * 5,
            5
        )

        return round(score, 2)

    # ----------------------------------------
    # Notice Period Score
    # ----------------------------------------

    def notice_score(self, candidate):

        notice = (
            candidate
            .get("redrob_signals", {})
            .get("notice_period_days", 180)
        )

        if notice <= 30:
            return 10

        elif notice <= 60:
            return 7

        elif notice <= 90:
            return 4

        return 1

    # ----------------------------------------
    # Honeypot Detection
    # ----------------------------------------

    def honeypot_penalty(self, candidate):

        penalty = 0

        profile = candidate.get(
            "profile",
            {}
        )

        years = profile.get(
            "years_of_experience",
            0
        )

        skills = candidate.get(
            "skills",
            []
        )

        expert_skills = 0

        for skill in skills:

            if str(
                skill.get("proficiency", "")
            ).lower() == "expert":

                expert_skills += 1

        # Too many expert skills for low experience

        if years < 3 and expert_skills >= 8:
            penalty -= 15

        history = candidate.get(
            "career_history",
            []
        )

        total_months = sum(
            job.get("duration_months", 0)
            for job in history
        )

        if abs(total_months / 12 - years) > 4:
            penalty -= 10

        return penalty

    # ----------------------------------------
    # Final Model Score
    # ----------------------------------------

    def calculate_score(self, candidate):

        base = self.extractor.calculate_total_score(candidate)

        score = base["total_score"]

        score += self.product_company_score(candidate)

        score += self.retrieval_relevance_score(candidate)

        score += self.title_relevance_score(candidate)

        score += self.experience_band_score(candidate)

        score += self.career_stability_score(candidate)

        score += self.education_score(candidate)

        score += self.skill_quality_score(candidate)

        score += self.activity_score(candidate)

        score += self.notice_score(candidate)

        score += self.honeypot_penalty(candidate)

        return round(score, 2)
        # ----------------------------------------
    # Generate Reasoning
    # ----------------------------------------

    def generate_reasoning(self, candidate, score):

        profile = candidate.get("profile", {})
        signals = candidate.get("redrob_signals", {})

        years = profile.get("years_of_experience", 0)
        title = profile.get("current_title", "Professional")
        location = profile.get("location", "")

        strengths = []

        if self.retrieval_relevance_score(candidate) >= 8:
            strengths.append(
                "strong experience in retrieval, ranking and search systems"
            )

        if self.product_company_score(candidate) >= 4:
            strengths.append(
                "good product-company background"
            )

        if self.skill_quality_score(candidate) >= 18:
            strengths.append(
                "high-quality technical skill profile"
            )

        if self.activity_score(candidate) >= 15:
            strengths.append(
                "high recruiter engagement"
            )

        if self.notice_score(candidate) >= 7:
            strengths.append(
                "short notice period"
            )

        if len(strengths) == 0:
            strengths.append(
                "relevant engineering background"
            )

        concerns = []

        if signals.get("notice_period_days", 180) > 60:
            concerns.append("long notice period")

        if signals.get("recruiter_response_rate", 0) < 0.3:
            concerns.append("low recruiter responsiveness")

        if self.career_stability_score(candidate) <= 2:
            concerns.append("frequent job changes")

        reason = (
            f"{title} with {years} years of experience, "
            f"{', '.join(strengths)}."
        )

        if concerns:
            reason += " Minor concern: " + ", ".join(concerns) + "."

        return reason

    # ----------------------------------------
    # Maintain Top 100 Heap
    # ----------------------------------------

    def add_candidate(self, candidate):

        score = self.calculate_score(candidate)

        candidate_id = candidate["candidate_id"]

        reasoning = self.generate_reasoning(candidate, score)

        item = (
            score,
            candidate_id,
            reasoning
        )

        if len(self.heap) < self.top_k:

            heapq.heappush(
                self.heap,
                item
            )

        else:

            if score > self.heap[0][0]:

                heapq.heapreplace(
                    self.heap,
                    item
                )

    # ----------------------------------------
    # Rank All Candidates
    # ----------------------------------------

    def rank_candidates(self):

        print("Ranking candidates...\n")

        count = 0

        for candidate in self.stream_candidates():

            self.add_candidate(candidate)

            count += 1

            if count % 5000 == 0:

                print(f"Processed {count:,} candidates")

        print(f"\nFinished processing {count:,} candidates.")

        ranked = sorted(
            self.heap,
            key=lambda x: (-x[0], x[1])
        )

        return ranked

    # ----------------------------------------
    # Save Submission CSV
    # ----------------------------------------

    def save_submission(self, ranked):

        SUBMISSION_FILE.parent.mkdir(
            parents=True,exist_ok=True
        )

        with open(
            SUBMISSION_FILE,
            "w",
            newline="",
            encoding="utf8"
        ) as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(

                [
                    "candidate_id",
                    "rank",
                    "score",
                    "reasoning"
                ]
            )

            for rank, item in enumerate(ranked, start=1):

                score, candidate_id, reasoning = item

                writer.writerow(

                    [
                        candidate_id,
                        rank,
                        round(score, 4),
                        reasoning
                    ]
                )

        print("\nSubmission saved successfully.")
        print(SUBMISSION_FILE)
# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("Redrob Candidate Ranking System")
    print("=" * 60)

    ranker = CandidateRanker()

    ranked = ranker.rank_candidates()

    ranker.save_submission(ranked)

    print("\nTop 10 Candidates\n")

    for rank, item in enumerate(ranked[:10], start=1):

        score, cid, reason = item

        print(
            f"{rank:2}. "
            f"{cid} | "
            f"{score:.2f}"
        )

    print("\nDone.")


if __name__ == "__main__":
    main()