"""Command Line Interface for Local Business Automation Agency.

Usage:
    python src/cli.py generate-link --place-id <PLACE_ID> --slug <BUSINESS_SLUG>
    python src/cli.py test-reply --business <NAME> --stars <1-5> --reviewer <NAME> --comment <TEXT>
    python src/cli.py serve --port 8000
"""

import argparse
import os
import sys

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uvicorn
from src.tools.google_review_link_builder import GoogleReviewLinkBuilder
from src.tools.ai_review_responder import AIReviewResponder, BusinessContext, ReviewInput
from src.tools.geo_llm_audit_tool import GEOCrawlerAuditor


def cmd_generate_link(args):
    print("\n==========================================")
    print("  LOCAL BUSINESS NFC LINK GENERATOR")
    print("==========================================")
    
    if args.place_id:
        direct_google = GoogleReviewLinkBuilder.build_direct_google_url(place_id=args.place_id)
        print(f"[+] Direct Google Review URL : {direct_google}")
    elif args.shortcode:
        direct_google = GoogleReviewLinkBuilder.build_direct_google_url(g_page_shortcode=args.shortcode)
        print(f"[+] Direct Google Review URL : {direct_google}")
    else:
        print("[!] Error: Specify --place-id or --shortcode")
        sys.exit(1)

    dynamic_nfc = GoogleReviewLinkBuilder.build_dynamic_nfc_url(
        business_slug=args.slug,
        agency_domain=args.domain,
        placement_source=args.source,
    )
    print(f"[+] Dynamic NFC Redirect URL : {dynamic_nfc}")
    
    fit = GoogleReviewLinkBuilder.check_nfc_capacity_fit(dynamic_nfc, chip_type="NTAG215")
    print(f"[+] NTAG215 Chip Capacity    : {fit['byte_length']} / {fit['max_capacity_bytes']} bytes (FITS: {fit['fits']})")
    print("\n--> INSTRUCTION: Program the *Dynamic NFC Redirect URL* into your NFC Tools app.")
    print("==========================================\n")


def cmd_test_reply(args):
    print("\n==========================================")
    print("  AI LOCAL SEO REVIEW RESPONDER TEST")
    print("==========================================")
    context = BusinessContext(
        business_name=args.business,
        city=args.city,
        neighborhood_or_street=args.location,
        primary_category="Local Business",
        primary_services=[s.strip() for s in args.services.split(",")],
    )
    responder = AIReviewResponder(context)
    review = ReviewInput(
        reviewer_name=args.reviewer,
        star_rating=args.stars,
        review_text=args.comment,
    )
    
    reply = responder.generate_instant_response(review)
    print(f"Reviewer: {args.reviewer} ({args.stars}/5 Stars)")
    print(f"Review  : \"{args.comment}\"\n")
    print(f"Generated SEO Response:\n{reply}\n")
    print("==========================================\n")


def cmd_geo_audit(args):
    print("\n==========================================")
    print("  GENERATIVE ENGINE OPTIMIZATION (GEO) AUDIT")
    print("==========================================")
    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()
    
    result = GEOCrawlerAuditor.audit_schema_json(content, expected_city=args.city)
    print(f"Business: {result.business_name}")
    print(f"Score   : {result.overall_score}/100")
    print(f"Category: {result.schema_type}\n")
    print("Passed Checks:")
    for p in result.passed_checks:
        print(f"  [+] {p}")
    print("\nFailed Checks / Gaps:")
    for f in result.failed_checks:
        print(f"  [-] {f}")
    print("\nCritical Recommendations for AI Agents (ChatGPT/Perplexity/Gemini):")
    for r in result.critical_recommendations:
        print(f"  [!] {r}")
    print("==========================================\n")


def cmd_generate_schema(args):
    print("\n==========================================")
    print("  AI CRAWLER SCHEMA.ORG JSON-LD GENERATOR")
    print("==========================================")
    schema = GEOCrawlerAuditor.generate_recommended_schema(
        business_name=args.business,
        category=args.category,
        street_address=args.address,
        city=args.city,
        phone=args.phone,
        rating_value=args.rating,
        review_count=args.reviews,
        cuisine_or_service=args.services,
    )
    print(schema)
    print("\n--> INSTRUCTION: Embed this JSON-LD script inside the client's website <head> tag.")
    print("==========================================\n")


def cmd_export_sticker(args):
    print("\n==========================================")
    print("  VECTOR NFC PRINT STICKER EXPORTER")
    print("==========================================")
    from src.tools.print_asset_generator import PrintAssetGenerator
    
    dynamic_url = f"https://{args.domain}/r/{args.slug}"
    out_file = PrintAssetGenerator.save_sticker_to_file(
        output_path=args.out,
        business_name=args.business,
        dynamic_url=dynamic_url,
        city=args.city,
    )
    print(f"[+] Business Name    : {args.business}")
    print(f"[+] Dynamic URL      : {dynamic_url}")
    print(f"[+] Sticker Artwork  : {os.path.abspath(out_file)}")
    print("\n--> Send this SVG file to Minuteman Press Saskatoon or Staples for printing.")
    print("==========================================\n")


def cmd_scan_reddit(args):
    print("\n==========================================")
    print(f"  REDDIT r/saskatoon RECOMMENDATION SCANNER")
    print("==========================================")
    from src.tools.reddit_scanner import RedditOpportunityScanner
    
    threads = RedditOpportunityScanner.search_subreddit(query=args.query, limit=args.limit)
    print(f"Found {len(threads)} relevant discussions for '{args.query}':\n")
    for idx, t in enumerate(threads, 1):
        print(f"{idx}. [{t.opportunity_score}/100 Opp Score] {t.title}")
        print(f"   Comments: {t.num_comments} | Score: {t.score} | By: {t.author}")
        print(f"   Link: {t.permalink}\n")
    print("==========================================\n")


def cmd_serve(args):
    print(f"\n[+] Starting Local Business Reputation Funnel server on http://127.0.0.1:{args.port} ...")
    uvicorn.run("src.tools.sentiment_funnel_server:app", host="127.0.0.1", port=args.port, reload=False)


def main():
    parser = argparse.ArgumentParser(description="Local Business Automation CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: generate-link
    gen_parser = subparsers.add_parser("generate-link", help="Generate direct Google & dynamic NFC URLs")
    gen_parser.add_argument("--place-id", help="Google Place ID")
    gen_parser.add_argument("--shortcode", help="Google GBP shortcode")
    gen_parser.add_argument("--slug", required=True, help="Business slug (e.g., 'korean-bbq-8th')")
    gen_parser.add_argument("--domain", default="tap.yxeagency.ca", help="Agency dynamic redirect domain")
    gen_parser.add_argument("--source", default="counter_stand", help="Placement source tag")
    gen_parser.set_defaults(func=cmd_generate_link)

    # Subcommand: test-reply
    reply_parser = subparsers.add_parser("test-reply", help="Test AI review response generation with SEO keywords")
    reply_parser.add_argument("--business", default="Arisu Korean BBQ", help="Business name")
    reply_parser.add_argument("--city", default="Saskatoon", help="Target city")
    reply_parser.add_argument("--location", default="8th Street East", help="Neighborhood or street")
    reply_parser.add_argument("--services", default="authentic Korean BBQ,crispy Korean fried chicken,stone bowl bibimbap", help="Comma-separated offerings")
    reply_parser.add_argument("--stars", type=int, default=5, help="Star rating (1-5)")
    reply_parser.add_argument("--reviewer", default="Jessica", help="Reviewer name")
    reply_parser.add_argument("--comment", default="Best meal in Saskatoon! Loved the fried chicken.", help="Review text")
    reply_parser.set_defaults(func=cmd_test_reply)

    # Subcommand: serve
    serve_parser = subparsers.add_parser("serve", help="Run local dynamic redirect & sentiment funnel web server")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    serve_parser.set_defaults(func=cmd_serve)

    # Subcommand: geo-audit
    audit_parser = subparsers.add_parser("geo-audit", help="Audit Schema.org JSON-LD for AI crawler readiness")
    audit_parser.add_argument("--file", required=True, help="Path to JSON or JSON-LD file")
    audit_parser.add_argument("--city", default="Saskatoon", help="Target city")
    audit_parser.set_defaults(func=cmd_geo_audit)

    # Subcommand: generate-schema
    schema_parser = subparsers.add_parser("generate-schema", help="Generate AI-optimized Schema.org JSON-LD markup")
    schema_parser.add_argument("--business", required=True, help="Business name")
    schema_parser.add_argument("--category", default="Restaurant", help="Schema type (e.g. Restaurant, Dentist, AutoRepair)")
    schema_parser.add_argument("--address", default="1505 8th St E", help="Street address")
    schema_parser.add_argument("--city", default="Saskatoon", help="City")
    schema_parser.add_argument("--phone", default="(306) 555-0199", help="Phone number")
    schema_parser.add_argument("--rating", type=float, default=4.8, help="Star rating")
    schema_parser.add_argument("--reviews", type=int, default=180, help="Total review count")
    schema_parser.add_argument("--services", default="Authentic Korean Cuisine", help="Cuisine or service description")
    schema_parser.set_defaults(func=cmd_generate_schema)

    # Subcommand: export-sticker
    sticker_parser = subparsers.add_parser("export-sticker", help="Export custom print-ready vector SVG sticker")
    sticker_parser.add_argument("--business", required=True, help="Business name")
    sticker_parser.add_argument("--slug", required=True, help="Business slug")
    sticker_parser.add_argument("--domain", default="tap.yxeagency.ca", help="Domain")
    sticker_parser.add_argument("--city", default="Saskatoon", help="City")
    sticker_parser.add_argument("--out", default="output/stickers/nfc_sticker.svg", help="Output file path")
    sticker_parser.set_defaults(func=cmd_export_sticker)

    # Subcommand: scan-reddit
    reddit_parser = subparsers.add_parser("scan-reddit", help="Scan r/saskatoon for recommendation opportunities")
    reddit_parser.add_argument("--query", default="best korean", help="Search query")
    reddit_parser.add_argument("--limit", type=int, default=5, help="Number of threads")
    reddit_parser.set_defaults(func=cmd_scan_reddit)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
