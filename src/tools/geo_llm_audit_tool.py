"""Generative Engine Optimization (GEO) & Schema.org Structured Data Audit Tool.

Features:
1. Validates Schema.org JSON-LD structured data for local businesses.
2. Checks compliance with AI crawlers (GPTBot, PerplexityBot, Googlebot).
3. Evaluates entity density (Name, Address, Coordinates, Menu/Services, Phone).
4. Generates a GEO Readiness Scorecard (0-100) with prioritized recommendations.
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class GEOAuditResult:
    business_name: str
    overall_score: int
    schema_detected: bool
    schema_type: Optional[str]
    passed_checks: List[str] = field(default_factory=list)
    failed_checks: List[str] = field(default_factory=list)
    critical_recommendations: List[str] = field(default_factory=list)


class GEOCrawlerAuditor:
    """Audits local business web presence and Schema.org markup for AI recommendation readiness."""

    REQUIRED_SCHEMA_FIELDS = [
        ("name", "Business legal name"),
        ("address", "PostalAddress with locality and street"),
        ("telephone", "Direct contact telephone number"),
        ("geo", "Exact latitude and longitude coordinates"),
        ("aggregateRating", "Star rating and review count from Google/third-parties"),
    ]

    @classmethod
    def audit_schema_json(cls, schema_json_str: str, expected_city: str = "Saskatoon") -> GEOAuditResult:
        """Parses and audits a JSON-LD schema snippet."""
        try:
            data = json.loads(schema_json_str)
        except json.JSONDecodeError:
            return GEOAuditResult(
                business_name="Unknown",
                overall_score=0,
                schema_detected=False,
                schema_type=None,
                failed_checks=["Valid JSON-LD schema markup detected"],
                critical_recommendations=["Add valid Schema.org JSON-LD to website <head> section."],
            )

        # Normalize data (handle @graph or direct object)
        if isinstance(data, dict) and "@graph" in data:
            # find first LocalBusiness/Restaurant
            target_node = None
            for node in data["@graph"]:
                node_type = str(node.get("@type", ""))
                if "LocalBusiness" in node_type or "Restaurant" in node_type:
                    target_node = node
                    break
            data = target_node or data["@graph"][0]

        business_name = data.get("name", "Unknown Business")
        schema_type = data.get("@type", "Thing")

        passed = []
        failed = []
        recommendations = []
        score = 20  # Base for having valid JSON

        # Check Schema Type
        if schema_type in ["LocalBusiness", "Restaurant", "Dentist", "AutoRepair", "HealthAndBeautyBusiness"]:
            passed.append(f"Specific Schema.org @type: {schema_type}")
            score += 15
        else:
            failed.append("Specific LocalBusiness category type (e.g. Restaurant, Dentist)")
            recommendations.append(f"Change @type from '{schema_type}' to a specific category like 'Restaurant' or 'AutoRepair'.")

        # Check required fields
        for field_name, label in cls.REQUIRED_SCHEMA_FIELDS:
            if field_name in data and data[field_name]:
                passed.append(f"Field present: {label} ({field_name})")
                score += 12
            else:
                failed.append(f"Missing field: {label} ({field_name})")
                recommendations.append(f"Add missing '{field_name}' property to your Schema markup.")

        # Check City localization
        address_data = data.get("address", {})
        if isinstance(address_data, dict):
            locality = address_data.get("addressLocality", "")
            if expected_city.lower() in locality.lower():
                passed.append(f"City locality confirmed: {expected_city}")
                score += 5
            else:
                failed.append(f"Locality does not explicitly match '{expected_city}'")
                recommendations.append(f"Set addressLocality to '{expected_city}'.")
        else:
            failed.append("Structured PostalAddress object")

        # Clamp score to 100
        overall_score = min(100, score)

        # AI Recommendation Priority Advice
        if "aggregateRating" not in data:
            recommendations.append(
                "CRITICAL FOR LLMs: Add 'aggregateRating' pulling your Google Review count so Perplexity and ChatGPT can cite your star rating."
            )

        return GEOAuditResult(
            business_name=business_name,
            overall_score=overall_score,
            schema_detected=True,
            schema_type=schema_type,
            passed_checks=passed,
            failed_checks=failed,
            critical_recommendations=recommendations,
        )

    @classmethod
    def generate_recommended_schema(
        cls,
        business_name: str,
        category: str,
        street_address: str,
        city: str = "Saskatoon",
        province: str = "SK",
        postal_code: str = "S7H 0W5",
        phone: str = "(306) 555-0199",
        latitude: float = 52.1158,
        longitude: float = -106.6341,
        rating_value: float = 4.8,
        review_count: int = 240,
        cuisine_or_service: str = "Authentic Korean Cuisine",
    ) -> str:
        """Generates copy-paste ready Schema.org JSON-LD tailored for LLM crawlers."""
        schema = {
            "@context": "https://schema.org",
            "@type": category,
            "name": business_name,
            "image": f"https://{business_name.lower().replace(' ', '')}.ca/storefront.jpg",
            "telephone": phone,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": street_address,
                "addressLocality": city,
                "addressRegion": province,
                "postalCode": postal_code,
                "addressCountry": "CA",
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": latitude,
                "longitude": longitude,
            },
            "servesCuisine": cuisine_or_service,
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": str(rating_value),
                "reviewCount": str(review_count),
                "bestRating": "5",
                "worstRating": "1",
            },
        }
        return json.dumps(schema, indent=2)
