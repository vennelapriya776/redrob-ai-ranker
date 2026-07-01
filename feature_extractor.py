"""
feature_extractor.py

Extracts features from a candidate profile.
"""

from config import (
    AI_SKILLS,
    GOOD_TITLES,
    GOOD_INDUSTRIES,
    CONSULTING_COMPANIES,
    MIN_EXPERIENCE,
    MAX_EXPERIENCE,
)


class FeatureExtractor:

    def __init__(self):
        pass

    # ----------------------------------------
    # Utility
    # ----------------------------------------

    def clean(self, text):
        if text is None:
            return ""
        return str(text).lower().strip()

    # ----------------------------------------
    # Skill Score
    # ----------------------------------------

    def skill_score(self, candidate):

        total = 0

        skills = candidate.get("skills", [])

        candidate_skills = []

        for skill in skills:
            name = self.clean(skill.get("name"))
            candidate_skills.append(name)

        for skill_name, weight in AI_SKILLS.items():

            if skill_name.lower() in candidate_skills:
                total += weight

        return total

    # ----------------------------------------
    # Experience Score
    # ----------------------------------------

    def experience_score(self, candidate):

        years = (
            candidate
            .get("profile", {})
            .get("years_of_experience", 0)
        )

        if years < MIN_EXPERIENCE:
            return years * 2

        elif years <= MAX_EXPERIENCE:
            return 20

        elif years <= 12:
            return 16

        else:
            return 10

    # ----------------------------------------
    # Current Title Score
    # ----------------------------------------

    def title_score(self, candidate):

        title = self.clean(
            candidate
            .get("profile", {})
            .get("current_title", "")
        )

        for good_title in GOOD_TITLES:

            if good_title.lower() in title:
                return 15

        return 0
        # ----------------------------------------
    # Industry Score
    # ----------------------------------------

    def industry_score(self, candidate):

        industry = self.clean(
            candidate.get("profile", {}).get("current_industry", "")
        )

        for good in GOOD_INDUSTRIES:
            if good.lower() in industry:
                return 10

        return 3

    # ----------------------------------------
    # Career History Score
    # ----------------------------------------

    def career_score(self, candidate):

        history = candidate.get("career_history", [])

        score = 0

        important_keywords = [

            "machine learning",
            "deep learning",
            "artificial intelligence",
            "ai",
            "llm",
            "rag",
            "retrieval",
            "ranking",
            "recommendation",
            "embedding",
            "vector",
            "nlp",
            "transformer",
            "bert",
            "search",
            "semantic search",
            "information retrieval"
        ]

        for job in history:

            title = self.clean(job.get("title", ""))

            description = self.clean(job.get("description", ""))

            combined = title + " " + description

            for keyword in important_keywords:

                if keyword in combined:
                    score += 2

        return min(score, 20)

    # ----------------------------------------
    # Consulting Company Penalty
    # ----------------------------------------

    def consulting_penalty(self, candidate):

        history = candidate.get("career_history", [])

        if len(history) == 0:
            return 0

        consulting_jobs = 0

        for job in history:

            company = self.clean(job.get("company", ""))

            for consulting in CONSULTING_COMPANIES:

                if consulting.lower() in company:
                    consulting_jobs += 1

        if consulting_jobs == len(history):
            return -15

        elif consulting_jobs >= len(history) / 2:
            return -5

        return 0

    # ----------------------------------------
    # Product Company Bonus
    # ----------------------------------------

    def product_bonus(self, candidate):

        history = candidate.get("career_history", [])

        bonus = 0

        product_keywords = [

            "saas",
            "fintech",
            "ai",
            "software",
            "product",
            "startup",
            "healthtech",
            "e-commerce"
        ]

        for job in history:

            industry = self.clean(job.get("industry", ""))

            for keyword in product_keywords:

                if keyword in industry:
                    bonus += 2

        return min(bonus, 10)
        # ----------------------------------------
    # Behavioral Score
    # ----------------------------------------

    def behavior_score(self, candidate):

        signals = candidate.get("redrob_signals", {})

        score = 0

        if signals.get("open_to_work_flag", False):
            score += 5

        score += min(signals.get("profile_completeness_score", 0) / 20, 5)

        score += min(signals.get("recruiter_response_rate", 0) * 5, 5)

        score += min(signals.get("interview_completion_rate", 0) * 5, 5)

        github = signals.get("github_activity_score", -1)

        if github > 0:
            score += github / 20

        if signals.get("willing_to_relocate", False):
            score += 2

        notice = signals.get("notice_period_days", 180)

        if notice <= 30:
            score += 3
        elif notice <= 60:
            score += 2

        return round(score, 2)

    # ----------------------------------------
    # Location Score
    # ----------------------------------------

    def location_score(self, candidate):

        location = self.clean(
            candidate.get("profile", {}).get("location", "")
        )

        preferred = [
            "pune",
            "noida",
            "hyderabad",
            "bangalore",
            "bengaluru",
            "mumbai",
            "delhi",
            "gurgaon",
            "gurugram"
        ]

        for city in preferred:
            if city in location:
                return 5

        return 2

    # ----------------------------------------
    # Final Feature Extraction
    # ----------------------------------------

    def extract_features(self, candidate):

        features = {}

        features["candidate_id"] = candidate.get("candidate_id")

        features["skill_score"] = self.skill_score(candidate)

        features["experience_score"] = self.experience_score(candidate)

        features["title_score"] = self.title_score(candidate)

        features["industry_score"] = self.industry_score(candidate)

        features["career_score"] = self.career_score(candidate)

        features["behavior_score"] = self.behavior_score(candidate)

        features["location_score"] = self.location_score(candidate)

        features["product_bonus"] = self.product_bonus(candidate)

        features["consulting_penalty"] = self.consulting_penalty(candidate)

        return features
        # ----------------------------------------
    # Total Score
    # ----------------------------------------

    def calculate_total_score(self, candidate):

        features = self.extract_features(candidate)

        total = (
            features["skill_score"] * 0.35
            + features["experience_score"] * 0.15
            + features["career_score"] * 0.15
            + features["behavior_score"] * 0.20
            + features["industry_score"] * 0.05
            + features["location_score"] * 0.05
            + features["title_score"] * 0.05
            + features["product_bonus"] * 0.05
            + features["consulting_penalty"]
        )

        features["total_score"] = round(total, 2)

        return features


# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    import gzip
    import json

    from config import CANDIDATE_FILE

    extractor = FeatureExtractor()

    print("Loading first candidate...")

    with open(CANDIDATE_FILE, "rt", encoding="utf8") as f:

        first_candidate = json.loads(next(f))

    result = extractor.calculate_total_score(first_candidate)

    print()

    print("Extracted Features")

    print("-" * 40)

    for key, value in result.items():
        print(f"{key:25} : {value}")