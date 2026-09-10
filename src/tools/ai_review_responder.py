"""AI Automated Google Review Responder Engine.

Features:
1. Sentiment analysis and rating classification.
2. Local SEO keyword injection (City, neighborhood, high-margin services).
3. Brand tone adaptation (Warm, Professional, Casual, Luxury).
4. Generates both template-assisted fast responses and LLM prompt specifications.
"""

from dataclasses import dataclass, field
from enum import Enum
import random
from typing import List, Optional


class BrandTone(str, Enum):
    WARM_FRIENDLY = "warm_friendly"
    PROFESSIONAL = "professional"
    CASUAL_TRENDY = "casual_trendy"
    LUXURY_ELEVATED = "luxury_elevated"


class ReviewSentiment(str, Enum):
    POSITIVE = "positive"  # 4-5 stars
    NEUTRAL = "neutral"    # 3 stars
    NEGATIVE = "negative"  # 1-2 stars


@dataclass
class BusinessContext:
    business_name: str
    city: str = "Saskatoon"
    neighborhood_or_street: str = "8th Street East"
    primary_category: str = "Korean Restaurant"
    primary_services: List[str] = field(default_factory=lambda: [
        "authentic Korean BBQ",
        "crispy Korean fried chicken",
        "stone bowl bibimbap",
    ])
    manager_name: str = "Management Team"
    manager_contact: str = "feedback@yxeagency.ca"


@dataclass
class ReviewInput:
    reviewer_name: str
    star_rating: int
    review_text: str
    review_id: str = "rev_001"


class AIReviewResponder:
    """Generates Local SEO-optimized Google Review responses."""

    def __init__(self, context: BusinessContext, tone: BrandTone = BrandTone.WARM_FRIENDLY):
        self.context = context
        self.tone = tone

    def classify_sentiment(self, star_rating: int) -> ReviewSentiment:
        if star_rating >= 4:
            return ReviewSentiment.POSITIVE
        elif star_rating == 3:
            return ReviewSentiment.NEUTRAL
        else:
            return ReviewSentiment.NEGATIVE

    def build_llm_prompt(self, review: ReviewInput) -> dict:
        """Constructs an optimized prompt payload for Google Gemini or OpenAI APIs."""
        sentiment = self.classify_sentiment(review.star_rating)
        system_instruction = (
            f"You are the reputation manager for '{self.context.business_name}', a premier "
            f"{self.context.primary_category} located on {self.context.neighborhood_or_street} in {self.context.city}.\n"
            f"Tone of Voice: {self.tone.value.replace('_', ' ').title()}.\n"
            "Goal: Write an authentic, polite response to this Google Review that:\n"
            "1. Addresses the reviewer warmly by their first name.\n"
            "2. Naturally weaves in 1-2 relevant local keywords or signature offerings without keyword stuffing.\n"
            f"Available Keywords/Offerings: {', '.join(self.context.primary_services)}, {self.context.neighborhood_or_street}, {self.context.city}.\n"
            "3. If POSITIVE (4-5 stars): Express gratitude, highlight their experience, and warmly invite them back.\n"
            "4. If NEGATIVE (1-2 stars): Empathize, apologize for failing their expectations without admitting legal liability, "
            f"and request they contact {self.context.manager_name} directly at {self.context.manager_contact} to make it right.\n"
            "5. Keep the response between 40 and 80 words. Never sound robotic."
        )

        user_content = (
            f"Reviewer: {review.reviewer_name}\n"
            f"Rating: {review.star_rating}/5 Stars\n"
            f"Review Content: \"{review.review_text}\""
        )

        return {
            "system_instruction": system_instruction,
            "user_content": user_content,
            "sentiment": sentiment.value,
        }

    def generate_instant_response(self, review: ReviewInput) -> str:
        """Generates an immediate, algorithmic Local SEO response (fallback or offline engine)."""
        sentiment = self.classify_sentiment(review.star_rating)
        first_name = review.reviewer_name.strip().split(" ")[0] if review.reviewer_name else "Valued Guest"
        service = random.choice(self.context.primary_services)

        if sentiment == ReviewSentiment.POSITIVE:
            positive_templates = [
                (
                    f"Hi {first_name}, thank you so much for the 5-star review! "
                    f"Our team at {self.context.business_name} takes huge pride in serving the best {service} "
                    f"here on {self.context.neighborhood_or_street} in {self.context.city}. "
                    f"We look forward to welcoming you back again soon!"
                ),
                (
                    f"Thank you {first_name}! We're thrilled you had such a wonderful experience with us. "
                    f"Whether you're stopping by for {service} or catching up with friends, "
                    f"it's always a pleasure to serve our {self.context.city} community. See you next time!"
                ),
            ]
            return random.choice(positive_templates)

        elif sentiment == ReviewSentiment.NEUTRAL:
            return (
                f"Hi {first_name}, thank you for taking the time to share your feedback. "
                f"We always aim to provide a 5-star experience for every guest at our {self.context.neighborhood_or_street} location. "
                f"We’d love the opportunity to exceed your expectations on your next visit for {service}."
            )

        else:  # NEGATIVE
            return (
                f"Dear {first_name}, thank you for bringing this to our attention. "
                f"Providing exceptional service and quality is our top priority in {self.context.city}, and we regret that your visit did not reflect our usual standards. "
                f"We would appreciate the chance to make this right. Please reach out to our management team directly at {self.context.manager_contact} so we can assist you personally."
            )
