"""Comprehensive automated test suite for Local Business Automation tools."""

import pytest
from fastapi.testclient import TestClient

from src.tools.google_review_link_builder import GoogleReviewLinkBuilder
from src.tools.ai_review_responder import (
    AIReviewResponder,
    BusinessContext,
    ReviewInput,
    ReviewSentiment,
    BrandTone,
)
from src.tools.sentiment_funnel_server import app, ANALYTICS_LOGS, PRIVATE_FEEDBACK_LOGS


# ---------------------------------------------------------
# 1. Google Review Link Builder Tests
# ---------------------------------------------------------
def test_direct_google_url_from_place_id():
    place_id = "ChIJ3V8eYnTYBFMR8o9V29xZ1-E"
    url = GoogleReviewLinkBuilder.build_direct_google_url(place_id=place_id)
    assert "search.google.com/local/writereview" in url
    assert "placeid=ChIJ3V8eYnTYBFMR8o9V29xZ1-E" in url


def test_direct_google_url_from_shortcode():
    shortcode = "CZZ_0QZ64vDVEBM"
    url = GoogleReviewLinkBuilder.build_direct_google_url(g_page_shortcode=shortcode)
    assert url == "https://g.page/r/CZZ_0QZ64vDVEBM/review"


def test_build_dynamic_nfc_url():
    dynamic_url = GoogleReviewLinkBuilder.build_dynamic_nfc_url(
        business_slug="arisu-korean-yxe",
        agency_domain="tap.yxeagency.ca",
        placement_source="counter_stand_1",
    )
    assert dynamic_url.startswith("https://tap.yxeagency.ca/r/arisu-korean-yxe?")
    assert "src=counter_stand_1" in dynamic_url


def test_nfc_capacity_fit():
    test_url = "https://tap.yxeagency.ca/r/saskatoon-korean-bbq?src=counter_stand_1&cmp=launch"
    capacity = GoogleReviewLinkBuilder.check_nfc_capacity_fit(test_url, chip_type="NTAG215")
    assert capacity["fits"] is True
    assert capacity["byte_length"] < 100
    assert capacity["max_capacity_bytes"] == 504
    assert capacity["remaining_bytes"] > 400


# ---------------------------------------------------------
# 2. AI Review Responder & SEO Injection Tests
# ---------------------------------------------------------
@pytest.fixture
def sample_business_context():
    return BusinessContext(
        business_name="Arisu Korean BBQ",
        city="Saskatoon",
        neighborhood_or_street="8th Street East",
        primary_category="Korean Restaurant",
        primary_services=["authentic Korean BBQ", "crispy Korean fried chicken", "stone bowl bibimbap"],
        manager_name="David Kim",
        manager_contact="manager@arisu.ca",
    )


def test_sentiment_classification(sample_business_context):
    responder = AIReviewResponder(sample_business_context)
    assert responder.classify_sentiment(5) == ReviewSentiment.POSITIVE
    assert responder.classify_sentiment(4) == ReviewSentiment.POSITIVE
    assert responder.classify_sentiment(3) == ReviewSentiment.NEUTRAL
    assert responder.classify_sentiment(2) == ReviewSentiment.NEGATIVE
    assert responder.classify_sentiment(1) == ReviewSentiment.NEGATIVE


def test_positive_ai_reply_seo_injection(sample_business_context):
    responder = AIReviewResponder(sample_business_context, tone=BrandTone.WARM_FRIENDLY)
    review = ReviewInput(
        reviewer_name="Jessica Miller",
        star_rating=5,
        review_text="Best dinner we have had in months! The fried chicken is unbelievable.",
    )
    reply = responder.generate_instant_response(review)
    assert "Jessica" in reply
    assert "Saskatoon" in reply
    # Should include one of the primary offerings
    assert any(service in reply for service in sample_business_context.primary_services)


def test_negative_ai_reply_resolution(sample_business_context):
    responder = AIReviewResponder(sample_business_context)
    review = ReviewInput(
        reviewer_name="Mark Spencer",
        star_rating=1,
        review_text="Waited 45 minutes for our table and staff seemed disorganized.",
    )
    reply = responder.generate_instant_response(review)
    assert "Mark" in reply
    assert "manager@arisu.ca" in reply
    assert "apologize" in reply.lower() or "regret" in reply.lower()


def test_llm_prompt_payload_builder(sample_business_context):
    responder = AIReviewResponder(sample_business_context)
    review = ReviewInput(
        reviewer_name="Amy Chen",
        star_rating=5,
        review_text="Great food and service!",
    )
    prompt_spec = responder.build_llm_prompt(review)
    assert "system_instruction" in prompt_spec
    assert "user_content" in prompt_spec
    assert "Amy Chen" in prompt_spec["user_content"]
    assert "Saskatoon" in prompt_spec["system_instruction"]


# ---------------------------------------------------------
# 3. Dynamic Redirect & Sentiment Funnel API Tests
# ---------------------------------------------------------
@pytest.fixture
def client():
    return TestClient(app)


def test_api_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["market"] == "Saskatoon, SK"


def test_direct_mode_redirect(client):
    # 'broadway-fade-barber' has funnel_enabled=False -> should 302 redirect directly
    response = client.get("/r/broadway-fade-barber", follow_redirects=False)
    assert response.status_code == 302
    assert "search.google.com/local/writereview" in response.headers["location"]


def test_funnel_mode_html_render(client):
    # 'yxe-korean-bbq' has funnel_enabled=True -> should return 200 HTML funnel page
    response = client.get("/r/yxe-korean-bbq")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Arisu Korean BBQ & Chicken" in response.text
    assert "VIP Guest Experience" in response.text
    assert "compliance-link" in response.text


def test_submit_private_feedback(client):
    initial_count = len(PRIVATE_FEEDBACK_LOGS)
    response = client.post(
        "/api/feedback/submit",
        data={
            "tag_slug": "yxe-korean-bbq",
            "rating": 2,
            "name": "Tom Davis",
            "contact": "tom.davis@example.com",
            "message": "The table was not wiped clean when we sat down.",
        },
    )
    assert response.status_code == 200
    assert "Thank You, Tom Davis" in response.text
    assert len(PRIVATE_FEEDBACK_LOGS) == initial_count + 1
    latest = PRIVATE_FEEDBACK_LOGS[-1]
    assert latest["customer_name"] == "Tom Davis"
    assert latest["rating"] == 2


def test_api_generate_reply(client):
    response = client.post(
        "/api/reviews/generate-reply",
        json={
            "tag_slug": "yxe-korean-bbq",
            "reviewer_name": "Chloe Vance",
            "star_rating": 5,
            "review_text": "Loved the bibimbap and welcoming atmosphere!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["reviewer_name"] == "Chloe Vance"
    assert "Chloe" in data["generated_seo_reply"]
    assert "Saskatoon" in data["generated_seo_reply"]


def test_tag_analytics_stats(client):
    # Tap the card first
    client.get("/r/yxe-korean-bbq?src=test_tap")
    response = client.get("/api/stats/yxe-korean-bbq")
    assert response.status_code == 200
    data = response.json()
    assert data["tag_slug"] == "yxe-korean-bbq"
    assert data["total_taps"] >= 1


# ---------------------------------------------------------
# 4. GEO & Schema.org Auditor Tests
# ---------------------------------------------------------
from src.tools.geo_llm_audit_tool import GEOCrawlerAuditor


def test_geo_schema_generator():
    schema_str = GEOCrawlerAuditor.generate_recommended_schema(
        business_name="Arisu Korean BBQ",
        category="Restaurant",
        street_address="1505 8th St E",
        city="Saskatoon",
        phone="(306) 555-0199",
        rating_value=4.9,
        review_count=310,
    )
    assert "Arisu Korean BBQ" in schema_str
    assert "Saskatoon" in schema_str
    assert "AggregateRating" in schema_str
    assert '"ratingValue": "4.9"' in schema_str


def test_geo_schema_audit_success():
    schema_str = GEOCrawlerAuditor.generate_recommended_schema(
        business_name="Arisu Korean BBQ",
        category="Restaurant",
        street_address="1505 8th St E",
        city="Saskatoon",
    )
    result = GEOCrawlerAuditor.audit_schema_json(schema_str, expected_city="Saskatoon")
    assert result.schema_detected is True
    assert result.overall_score >= 80
    assert result.schema_type == "Restaurant"
    assert len(result.failed_checks) == 0


def test_geo_schema_audit_missing_fields():
    incomplete_json = '{"@type": "Thing", "name": "Basic Spot"}'
    result = GEOCrawlerAuditor.audit_schema_json(incomplete_json, expected_city="Saskatoon")
    assert result.schema_detected is True
    assert result.overall_score < 50
    assert any("Specific LocalBusiness category type" in f for f in result.failed_checks)
    assert any("aggregateRating" in r for r in result.critical_recommendations)


# ---------------------------------------------------------
# 5. Print Asset & Vector QR Code Generator Tests
# ---------------------------------------------------------
from src.tools.print_asset_generator import PrintAssetGenerator


def test_print_asset_generator_svg():
    svg_out = PrintAssetGenerator.generate_composite_sticker_svg(
        business_name="Arisu Korean BBQ",
        dynamic_url="https://tap.yxeagency.ca/r/yxe-korean-bbq",
        city="Saskatoon",
    )
    assert "<svg" in svg_out
    assert "ARISU KOREAN BBQ" in svg_out
    assert "Saskatoon" in svg_out
    assert "TAP PHONE HERE" in svg_out
    assert "OR SCAN WITH CAMERA" in svg_out
    assert 'viewBox="0 0 856 540"' in svg_out


# ---------------------------------------------------------
# 6. Reddit Opportunity Scanner Tests
# ---------------------------------------------------------
from src.tools.reddit_scanner import RedditOpportunityScanner


def test_reddit_scanner_search():
    threads = RedditOpportunityScanner.search_subreddit(query="best korean", limit=5)
    assert len(threads) > 0
    t = threads[0]
    assert hasattr(t, "title")
    assert hasattr(t, "opportunity_score")
    assert t.opportunity_score > 0
    assert "reddit.com" in t.permalink


# ---------------------------------------------------------
# 7. Web Dashboard & Pitch Demonstration Tests
# ---------------------------------------------------------
def test_dashboard_ui_render(client):
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Agency Operating Dashboard" in response.text
    assert "Active Saskatoon Clients" in response.text
    assert "Arisu Korean BBQ" in response.text


def test_pitch_ui_render(client):
    response = client.get("/pitch")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "The 5-Star Velocity Demo" in response.text
    assert "Hormozi ROI Value Calculator" in response.text
    assert "30-Day" in response.text


def test_toggle_funnel_api(client):
    # Initial state of broadway-fade-barber is False
    res = client.post("/api/locations/broadway-fade-barber/toggle-funnel")
    assert res.status_code == 200
    data = res.json()
    assert data["funnel_enabled"] is True
    assert data["plan_tier"] == "pro"

    # Toggle back
    res2 = client.post("/api/locations/broadway-fade-barber/toggle-funnel")
    assert res2.status_code == 200
    assert res2.json()["funnel_enabled"] is False


def test_download_sticker_svg_api(client):
    response = client.get("/api/locations/yxe-korean-bbq/sticker.svg")
    assert response.status_code == 200
    assert "image/svg+xml" in response.headers["content-type"]
    assert "<svg" in response.text
    assert "ARISU KOREAN BBQ" in response.text


