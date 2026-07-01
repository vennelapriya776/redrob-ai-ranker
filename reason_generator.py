"""
reason_generator.py

Generates a short explanation for why a candidate received a score.
"""


class ReasonGenerator:

    def __init__(self):
        pass

    def clean(self, value):
        if value is None:
            return ""
        return str(value).strip()

    def generate_reason(self, candidate, features):

        profile = candidate.get("profile", {})

        title = self.clean(profile.get("current_title", "Professional"))

        experience = profile.get("years_of_experience", 0)

        location = self.clean(profile.get("location", ""))

        # Extract first few skills
        skills = []
        for skill in candidate.get("skills", []):
            if isinstance(skill, dict):
                name = self.clean(skill.get("name"))
                if name:
                    skills.append(name)

        top_skills = ", ".join(skills[:3])

        reasons = []

        if experience >= 5:
            reasons.append(
                f"{experience} years of experience as {title}"
            )
        else:
            reasons.append(
                f"{title} with {experience} years of experience"
            )

        if top_skills:
            reasons.append(
                f"Strong skills in {top_skills}"
            )

        if location:
            reasons.append(
                f"Currently based in {location}"
            )

        if features.get("behavior_score", 0) >= 15:
            reasons.append(
                "Shows strong engagement and recruiter responsiveness"
            )

        if features.get("consulting_penalty", 0) < 0:
            reasons.append(
                "Career history is largely consulting-based"
            )

        # Keep only first three points
        reasons = reasons[:3]

        return ". ".join(reasons) + "."


    # =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    import json

    from config import CANDIDATE_FILE
    from feature_extractor import FeatureExtractor

    extractor = FeatureExtractor()
    generator = ReasonGenerator()

    with open(CANDIDATE_FILE, "r", encoding="utf8") as f:
        candidate = json.loads(next(f))

    features = extractor.calculate_total_score(candidate)

    print(generator.generate_reason(candidate, features))
