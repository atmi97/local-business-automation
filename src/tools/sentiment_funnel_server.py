"""FastAPI Prototype: Dynamic NFC Redirector & Sentiment Resolution Funnel.

Demonstrates:
1. Dynamic NFC tap routing (/r/{tag_slug}).
2. Compliance-first Sentiment Funnel (4-5 stars -> Google Review; 1-3 stars -> Private Manager Intake).
3. Analytics logging (tap counts, ratings).
4. Automated AI review response generation endpoint.
"""

from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from pydantic import BaseModel

from .ai_review_responder import AIReviewResponder, BusinessContext, ReviewInput
from .google_review_link_builder import GoogleReviewLinkBuilder
from .print_asset_generator import PrintAssetGenerator
from .reddit_scanner import RedditOpportunityScanner

app = FastAPI(title="Local Business Reputation & Sentiment Engine", version="1.0.0")

# In-memory database mock for testing & verification
DB_LOCATIONS = {
    "yxe-korean-bbq": {
        "name": "Arisu Korean BBQ & Chicken",
        "city": "Saskatoon",
        "neighborhood": "8th Street East",
        "place_id": "ChIJ3V8eYnTYBFMR8o9V29xZ1-E",
        "google_review_url": "https://search.google.com/local/writereview?placeid=ChIJ3V8eYnTYBFMR8o9V29xZ1-E",
        "funnel_enabled": True,
        "manager_email": "manager@arisu-yxe.ca",
        "primary_services": ["authentic Korean BBQ", "crispy Korean fried chicken", "stone bowl bibimbap"],
        "total_taps": 48,
        "plan_tier": "pro",
    },
    "broadway-fade-barber": {
        "name": "Broadway Heritage Barbershop",
        "city": "Saskatoon",
        "neighborhood": "Broadway Avenue",
        "place_id": "ChIJ4455YnTYBFMR8o9V29xZ1-B",
        "google_review_url": "https://search.google.com/local/writereview?placeid=ChIJ4455YnTYBFMR8o9V29xZ1-B",
        "funnel_enabled": False,  # Direct mode
        "manager_email": "barber@broadway-yxe.ca",
        "primary_services": ["skin fades", "hot towel shaves", "beard sculpting"],
        "total_taps": 26,
        "plan_tier": "starter",
    },
    "prairie-shine-detail": {
        "name": "Prairie Shine Auto Detailing",
        "city": "Saskatoon",
        "neighborhood": "North Industrial",
        "place_id": "ChIJ9988YnTYBFMR8o9V29xZ1-D",
        "google_review_url": "https://search.google.com/local/writereview?placeid=ChIJ9988YnTYBFMR8o9V29xZ1-D",
        "funnel_enabled": True,
        "manager_email": "owner@prairieshine.ca",
        "primary_services": ["ceramic coating", "paint correction", "interior detailing"],
        "total_taps": 19,
        "plan_tier": "pro",
    }
}

ANALYTICS_LOGS: List[dict] = []
PRIVATE_FEEDBACK_LOGS: List[dict] = [
    {
        "tag_slug": "yxe-korean-bbq",
        "rating": 2,
        "customer_name": "Marcus Evans",
        "customer_contact": "marcus.e@example.com",
        "message": "The wait time was about 25 minutes longer than quoted on Friday night.",
        "status": "resolved",
        "timestamp": "2026-09-08T19:30:00Z",
    }
]


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Local Business Automation Engine",
        "market": "Saskatoon, SK",
        "endpoints": {
            "demo_funnel_enabled": "/r/yxe-korean-bbq",
            "demo_direct_mode": "/r/broadway-fade-barber",
            "stats": "/api/stats/yxe-korean-bbq",
        }
    }


@app.get("/r/{tag_slug}", response_class=HTMLResponse)
def handle_nfc_tap(tag_slug: str, request: Request, src: str = "nfc_counter"):
    """Handles an incoming NFC tap or QR scan."""
    location = DB_LOCATIONS.get(tag_slug)
    if not location:
        raise HTTPException(status_code=404, detail="Business profile not found.")

    # Record analytics tap
    tap_record = {
        "tag_slug": tag_slug,
        "source": src,
        "user_agent": request.headers.get("user-agent", "Unknown"),
        "client_ip": request.client.host if request.client else "127.0.0.1",
        "timestamp": datetime.utcnow().isoformat(),
    }
    ANALYTICS_LOGS.append(tap_record)

    # 1. Direct Mode (Starter Tier): Immediate 302 Redirect to Google Review
    if not location["funnel_enabled"]:
        return RedirectResponse(url=location["google_review_url"], status_code=302)

    # 2. Pro Mode: Render the Mobile-Optimized Sentiment Funnel
    business_name = location["name"]
    google_url = location["google_review_url"]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{business_name} - Guest Experience</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            body {{ background: #f8fafc; color: #1e293b; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 16px; }}
            .card {{ background: #ffffff; max-width: 420px; width: 100%; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); padding: 32px 24px; text-align: center; }}
            .badge {{ display: inline-block; background: #e0f2fe; color: #0369a1; font-size: 13px; font-weight: 600; padding: 4px 12px; border-radius: 999px; margin-bottom: 16px; }}
            h1 {{ font-size: 22px; font-weight: 700; margin-bottom: 8px; color: #0f172a; }}
            p.subtext {{ font-size: 15px; color: #64748b; margin-bottom: 24px; }}
            .star-container {{ display: flex; justify-content: center; gap: 8px; margin-bottom: 24px; }}
            .star-btn {{ background: none; border: 1px solid #e2e8f0; border-radius: 12px; font-size: 28px; cursor: pointer; padding: 10px 14px; transition: transform 0.15s, background 0.15s; }}
            .star-btn:hover, .star-btn:active {{ transform: scale(1.15); background: #fef9c3; }}
            .feedback-panel {{ display: none; margin-top: 20px; text-align: left; background: #f1f5f9; padding: 20px; border-radius: 16px; }}
            .feedback-panel h3 {{ font-size: 16px; margin-bottom: 8px; color: #0f172a; }}
            .feedback-panel p {{ font-size: 13px; color: #475569; margin-bottom: 12px; }}
            .form-input {{ width: 100%; padding: 10px 12px; border: 1px solid #cbd5e1; border-radius: 8px; margin-bottom: 10px; font-size: 14px; }}
            .btn-submit {{ width: 100%; background: #2563eb; color: #ffffff; border: none; padding: 12px; border-radius: 8px; font-weight: 600; font-size: 15px; cursor: pointer; }}
            .compliance-link {{ display: block; margin-top: 18px; font-size: 12px; color: #94a3b8; text-decoration: none; }}
            .compliance-link:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">VIP Guest Experience</span>
            <h1>{business_name}</h1>
            <p class="subtext">How would you rate your visit with us today?</p>
            
            <div class="star-container">
                <button class="star-btn" onclick="rate(1)">⭐</button>
                <button class="star-btn" onclick="rate(2)">⭐</button>
                <button class="star-btn" onclick="rate(3)">⭐</button>
                <button class="star-btn" onclick="rate(4)">⭐</button>
                <button class="star-btn" onclick="rate(5)">⭐</button>
            </div>
            
            <div id="feedbackPanel" class="feedback-panel">
                <h3>We Want to Make This Right!</h3>
                <p>Please tell our General Manager directly what went wrong so we can resolve it immediately:</p>
                <form action="/api/feedback/submit" method="POST">
                    <input type="hidden" name="tag_slug" value="{tag_slug}">
                    <input type="hidden" id="ratingInput" name="rating" value="3">
                    <input class="form-input" type="text" name="name" placeholder="Your Name" required>
                    <input class="form-input" type="text" name="contact" placeholder="Phone or Email" required>
                    <textarea class="form-input" name="message" rows="3" placeholder="How can we make your next visit better?" required></textarea>
                    <button type="submit" class="btn-submit">Send to General Manager</button>
                </form>
            </div>

            <a class="compliance-link" href="{google_url}">Or continue directly to public Google Reviews &rarr;</a>
        </div>

        <script>
            function rate(stars) {{
                if (stars >= 4) {{
                    window.location.href = "{google_url}";
                }} else {{
                    document.getElementById('ratingInput').value = stars;
                    document.getElementById('feedbackPanel').style.display = 'block';
                }}
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/api/feedback/submit", response_class=HTMLResponse)
def submit_private_feedback(
    tag_slug: str = Form(...),
    rating: int = Form(...),
    name: str = Form(...),
    contact: str = Form(...),
    message: str = Form(...),
):
    """Stores private negative feedback and triggers manager resolution notification."""
    feedback_record = {
        "tag_slug": tag_slug,
        "rating": rating,
        "customer_name": name,
        "customer_contact": contact,
        "message": message,
        "status": "new",
        "timestamp": datetime.utcnow().isoformat(),
    }
    PRIVATE_FEEDBACK_LOGS.append(feedback_record)

    html_success = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Message Received</title>
        <style>
            body {{ font-family: -apple-system, sans-serif; background: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 16px; }}
            .box {{ background: white; max-width: 400px; padding: 32px; border-radius: 16px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
            h2 {{ color: #15803d; margin-bottom: 12px; }}
            p {{ color: #475569; font-size: 15px; line-height: 1.5; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Thank You, {name}</h2>
            <p>Your feedback has been sent directly to the General Manager. We take your experience seriously and will reach out to you shortly at {contact} to make things right.</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_success)


class ReviewReplyRequest(BaseModel):
    tag_slug: str
    reviewer_name: str
    star_rating: int
    review_text: str


@app.post("/api/reviews/generate-reply")
def api_generate_reply(payload: ReviewReplyRequest):
    """Generates an SEO-optimized AI review reply using business context and local keywords."""
    location = DB_LOCATIONS.get(payload.tag_slug)
    if not location:
        raise HTTPException(status_code=404, detail="Business location not found.")

    context = BusinessContext(
        business_name=location["name"],
        city=location["city"],
        neighborhood_or_street=location["neighborhood"],
        primary_category="Local Business",
        primary_services=location.get("primary_services", ["premier local service"]),
    )

    responder = AIReviewResponder(context)
    review_input = ReviewInput(
        reviewer_name=payload.reviewer_name,
        star_rating=payload.star_rating,
        review_text=payload.review_text,
    )

    llm_prompt = responder.build_llm_prompt(review_input)
    reply_text = responder.generate_instant_response(review_input)

    return {
        "business_name": location["name"],
        "reviewer_name": payload.reviewer_name,
        "star_rating": payload.star_rating,
        "generated_seo_reply": reply_text,
        "llm_prompt_spec": llm_prompt,
    }


@app.get("/api/stats/{tag_slug}")
def get_tag_stats(tag_slug: str):
    """Returns analytics for taps and intercepted feedback."""
    taps = [log for log in ANALYTICS_LOGS if log["tag_slug"] == tag_slug]
    feedbacks = [fb for fb in PRIVATE_FEEDBACK_LOGS if fb["tag_slug"] == tag_slug]
    return {
        "tag_slug": tag_slug,
        "total_taps": len(taps),
        "private_feedback_intercepted": len(feedbacks),
        "recent_taps": taps[-10:],
        "recent_feedbacks": feedbacks[-5:],
    }


@app.get("/api/locations/{slug}/sticker.svg")
def download_sticker_svg(slug: str):
    """Generates and serves the custom vector SVG sticker artwork for a client."""
    loc = DB_LOCATIONS.get(slug)
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    
    dynamic_url = f"https://tap.yxeagency.ca/r/{slug}"
    svg_content = PrintAssetGenerator.generate_composite_sticker_svg(
        business_name=loc["name"],
        dynamic_url=dynamic_url,
        city=loc["city"],
    )
    return Response(
        content=svg_content,
        media_type="image/svg+xml",
        headers={"Content-Disposition": f'attachment; filename="{slug}_nfc_sticker.svg"'},
    )


class CreateLocationRequest(BaseModel):
    slug: str
    name: str
    city: str = "Saskatoon"
    neighborhood: str = "8th Street East"
    place_id: str
    primary_services: List[str] = ["Local Service"]
    manager_email: str = "owner@business.ca"
    funnel_enabled: bool = True


@app.post("/api/locations/create")
def create_location(payload: CreateLocationRequest):
    """Registers a new local business client."""
    if payload.slug in DB_LOCATIONS:
        raise HTTPException(status_code=400, detail="Slug already exists")
    
    direct_url = GoogleReviewLinkBuilder.build_direct_google_url(place_id=payload.place_id)
    DB_LOCATIONS[payload.slug] = {
        "name": payload.name,
        "city": payload.city,
        "neighborhood": payload.neighborhood,
        "place_id": payload.place_id,
        "google_review_url": direct_url,
        "funnel_enabled": payload.funnel_enabled,
        "manager_email": payload.manager_email,
        "primary_services": payload.primary_services,
        "total_taps": 0,
        "plan_tier": "pro" if payload.funnel_enabled else "starter",
    }
    return {"status": "created", "slug": payload.slug, "location": DB_LOCATIONS[payload.slug]}


@app.post("/api/locations/{slug}/toggle-funnel")
def toggle_funnel(slug: str):
    """Toggles a client between Direct 302 mode and Compliant Sentiment Funnel mode."""
    loc = DB_LOCATIONS.get(slug)
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    loc["funnel_enabled"] = not loc["funnel_enabled"]
    loc["plan_tier"] = "pro" if loc["funnel_enabled"] else "starter"
    return {"slug": slug, "funnel_enabled": loc["funnel_enabled"], "plan_tier": loc["plan_tier"]}


@app.get("/api/reddit/scan")
def api_reddit_scan(query: str = "best korean"):
    """Scans r/saskatoon for live recommendation opportunities."""
    threads = RedditOpportunityScanner.search_subreddit(query=query, limit=6)
    return {
        "query": query,
        "subreddit": "r/saskatoon",
        "total_found": len(threads),
        "threads": [
            {
                "title": t.title,
                "author": t.author,
                "score": t.score,
                "comments": t.num_comments,
                "opportunity_score": t.opportunity_score,
                "permalink": t.permalink,
            }
            for t in threads
        ],
    }


@app.get("/dashboard", response_class=HTMLResponse)
def serve_dashboard():
    """Agency Management & Telemetry Dashboard."""
    total_clients = len(DB_LOCATIONS)
    total_taps = sum(loc.get("total_taps", 0) for loc in DB_LOCATIONS.values()) + len(ANALYTICS_LOGS)
    intercepted_count = len(PRIVATE_FEEDBACK_LOGS)

    rows = ""
    for slug, loc in DB_LOCATIONS.items():
        mode_badge = (
            '<span style="background:#dcfce7; color:#15803d; padding:4px 8px; border-radius:6px; font-weight:600; font-size:12px;">SHIELD ACTIVE</span>'
            if loc["funnel_enabled"]
            else '<span style="background:#f1f5f9; color:#475569; padding:4px 8px; border-radius:6px; font-weight:600; font-size:12px;">DIRECT GOOGLE</span>'
        )
        toggle_btn_text = "Switch to Direct" if loc["funnel_enabled"] else "Enable Shield"
        rows += f"""
        <tr>
            <td style="padding:12px; font-weight:600;">{loc['name']}<br><span style="font-size:12px; color:#64748b;">{loc['neighborhood']}</span></td>
            <td style="padding:12px;"><code style="background:#f1f5f9; padding:2px 6px; border-radius:4px;">/r/{slug}</code></td>
            <td style="padding:12px; text-align:center;">{loc.get('total_taps', 0)}</td>
            <td style="padding:12px; text-align:center;">{mode_badge}</td>
            <td style="padding:12px; text-align:right;">
                <button onclick="toggleFunnel('{slug}')" style="background:#f8fafc; border:1px solid #cbd5e1; padding:6px 12px; border-radius:6px; cursor:pointer; font-size:12px; margin-right:6px;">{toggle_btn_text}</button>
                <a href="/api/locations/{slug}/sticker.svg" style="background:#2563eb; color:white; padding:6px 12px; border-radius:6px; text-decoration:none; font-size:12px; font-weight:600;">Download Sticker</a>
            </td>
        </tr>
        """

    feedback_cards = ""
    for fb in reversed(PRIVATE_FEEDBACK_LOGS):
        feedback_cards += f"""
        <div style="background:#fff; border:1px solid #fecaca; border-left:4px solid #ef4444; border-radius:8px; padding:12px 16px; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <strong>{fb.get('customer_name', 'Customer')} ({fb.get('rating', 1)}⭐)</strong>
                <span style="font-size:11px; color:#64748b;">{fb.get('timestamp', '')[:10]}</span>
            </div>
            <p style="font-size:13px; color:#334155; margin-bottom:6px;">"{fb.get('message', '')}"</p>
            <div style="font-size:12px; color:#64748b;">Contact: <strong>{fb.get('customer_contact', '')}</strong> | Status: <span style="color:#15803d; font-weight:600;">{fb.get('status', 'new').upper()}</span></div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YXE Local Reviews | Agency Operating Dashboard</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            body {{ background: #f8fafc; color: #0f172a; padding: 24px; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; }}
            .header h1 {{ font-size: 24px; font-weight: 800; color: #1e293b; }}
            .header a {{ background: #10b981; color: white; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 14px; }}
            .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }}
            .kpi-card {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }}
            .kpi-card .val {{ font-size: 28px; font-weight: 800; color: #2563eb; margin-top: 4px; }}
            .card {{ background: white; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); padding: 24px; margin-bottom: 24px; }}
            .card h2 {{ font-size: 18px; font-weight: 700; margin-bottom: 16px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th {{ text-align: left; padding: 12px; background: #f1f5f9; font-size: 13px; color: #475569; }}
            .grid-2 {{ display: grid; grid-template-columns: 2fr 1fr; gap: 24px; }}
            .form-input {{ width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px; margin-bottom: 10px; font-size: 14px; }}
            .btn-primary {{ background: #2563eb; color: white; border: none; padding: 10px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>
                    <h1>YXE Local Reviews &amp; Business Automation</h1>
                    <p style="color:#64748b; font-size:14px;">Operational Agency Hub • Saskatoon, SK</p>
                </div>
                <div style="display:flex; gap:10px;">
                    <a href="/pitch" target="_blank" style="background:#4f46e5;">Open Sales Walk-in Demo 📱</a>
                    <a href="#addClient" style="background:#2563eb;">+ Add Client</a>
                </div>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card">
                    <div style="font-size:13px; color:#64748b;">Active Saskatoon Clients</div>
                    <div class="val">{total_clients}</div>
                </div>
                <div class="kpi-card">
                    <div style="font-size:13px; color:#64748b;">Total Counter NFC Taps</div>
                    <div class="val">{total_taps}</div>
                </div>
                <div class="kpi-card">
                    <div style="font-size:13px; color:#64748b;">Intercepted Negative Reviews</div>
                    <div class="val" style="color:#ef4444;">{intercepted_count}</div>
                </div>
                <div class="kpi-card">
                    <div style="font-size:13px; color:#64748b;">Monthly Retainer Run-Rate</div>
                    <div class="val" style="color:#10b981;">${total_clients * 149} CAD</div>
                </div>
            </div>

            <div class="card">
                <h2>Active Saskatoon Client Hardware &amp; Redirection</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Business Name &amp; Zone</th>
                            <th>Dynamic Tap URL</th>
                            <th style="text-align:center;">Total Taps</th>
                            <th style="text-align:center;">Shield Status</th>
                            <th style="text-align:right;">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>

            <div class="grid-2">
                <div class="card">
                    <h2>AI Local SEO Review Reply Simulator</h2>
                    <p style="color:#64748b; font-size:13px; margin-bottom:12px;">Test how our NLP engine injects Saskatoon geography and keywords into Google responses.</p>
                    <input class="form-input" id="simBusiness" value="Arisu Korean BBQ" placeholder="Business Name">
                    <input class="form-input" id="simReviewer" value="Jessica Miller" placeholder="Reviewer Name">
                    <select class="form-input" id="simStars">
                        <option value="5">5 Stars (Positive)</option>
                        <option value="3">3 Stars (Neutral)</option>
                        <option value="1">1 Star (Negative)</option>
                    </select>
                    <textarea class="form-input" id="simText" rows="2" placeholder="Review text">Unbelievable Korean fried chicken and friendly service on 8th Street!</textarea>
                    <button class="btn-primary" onclick="simulateReply()">Generate SEO Reply</button>
                    <div id="replyOutput" style="margin-top:16px; padding:12px; background:#f8fafc; border-radius:8px; font-size:14px; display:none; border:1px solid #e2e8f0;"></div>
                </div>

                <div class="card">
                    <h2>Negative Feedback Intercept Inbox</h2>
                    <p style="color:#64748b; font-size:13px; margin-bottom:12px;">Customer complaints captured privately before reaching Google:</p>
                    {feedback_cards if feedback_cards else '<p style="color:#94a3b8; font-size:13px;">No complaints recorded yet.</p>'}
                </div>
            </div>
        </div>

        <script>
            async function toggleFunnel(slug) {{
                await fetch('/api/locations/' + slug + '/toggle-funnel', {{ method: 'POST' }});
                window.location.reload();
            }}

            async function simulateReply() {{
                const res = await fetch('/api/reviews/generate-reply', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        tag_slug: 'yxe-korean-bbq',
                        reviewer_name: document.getElementById('simReviewer').value,
                        star_rating: parseInt(document.getElementById('simStars').value),
                        review_text: document.getElementById('simText').value
                    }})
                }});
                const data = await res.json();
                const out = document.getElementById('replyOutput');
                out.style.display = 'block';
                out.innerHTML = '<strong>Generated SEO Reply:</strong><br>' + data.generated_seo_reply;
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/pitch", response_class=HTMLResponse)
def serve_sales_pitch_tool():
    """Mobile Walk-In Sales Pitch & Hormozi ROI Demonstration Tool."""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Saskatoon 5-Star Reputation Engine | Owner Demo</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
            body { background: #0f172a; color: #f8fafc; padding: 16px; }
            .container { max-width: 480px; margin: 0 auto; }
            .badge { display: inline-block; background: #38bdf8; color: #082f49; font-size: 12px; font-weight: 800; padding: 4px 10px; border-radius: 999px; margin-bottom: 8px; }
            h1 { font-size: 26px; font-weight: 800; margin-bottom: 8px; color: #ffffff; }
            p.sub { font-size: 14px; color: #94a3b8; margin-bottom: 20px; }
            .card { background: #1e293b; border-radius: 16px; padding: 20px; margin-bottom: 16px; border: 1px solid #334155; }
            h2 { font-size: 18px; font-weight: 700; margin-bottom: 12px; color: #38bdf8; }
            .calc-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
            .calc-input { background: #0f172a; border: 1px solid #475569; color: white; padding: 8px; border-radius: 8px; width: 100px; text-align: right; font-size: 15px; }
            .roi-box { background: #064e3b; border: 1px solid #059669; border-radius: 12px; padding: 16px; text-align: center; margin-top: 12px; }
            .roi-val { font-size: 32px; font-weight: 900; color: #34d399; }
            .btn-tap { width: 100%; background: #2563eb; color: white; border: none; padding: 16px; border-radius: 12px; font-size: 18px; font-weight: 800; cursor: pointer; box-shadow: 0 4px 15px rgba(37,99,235,0.4); }
            .guarantee-box { background: #451a03; border: 1px solid #b45309; border-radius: 12px; padding: 16px; font-size: 13px; line-height: 1.5; color: #fed7aa; }
        </style>
    </head>
    <body>
        <div class="container">
            <span class="badge">SASKATOON LOCAL BUSINESS ENGINE</span>
            <h1>The 5-Star Velocity Demo</h1>
            <p class="sub">Show the owner this exact screen on your phone or tablet.</p>

            <div class="card">
                <h2>1. The 1-Second Tap Demonstration</h2>
                <p style="font-size:13px; color:#cbd5e1; margin-bottom:16px;">"Have the owner unlock their phone, then tap your card to their phone. Or click below to simulate the instant customer review dialog:"</p>
                <button class="btn-tap" onclick="window.open('/r/yxe-korean-bbq', '_blank')">📱 Tap Phone Here (Live Demo)</button>
            </div>

            <div class="card">
                <h2>2. Hormozi ROI Value Calculator</h2>
                <p style="font-size:13px; color:#cbd5e1; margin-bottom:16px;">Calculate the exact financial return for their specific business:</p>
                
                <div class="calc-row">
                    <span style="font-size:14px;">Average Customer Ticket:</span>
                    <input class="calc-input" id="ticketVal" type="number" value="65" oninput="calculateROI()">
                </div>
                <div class="calc-row">
                    <span style="font-size:14px;">Monthly Customers:</span>
                    <input class="calc-input" id="custVal" type="number" value="450" oninput="calculateROI()">
                </div>
                <div class="calc-row">
                    <span style="font-size:14px;">Est. New Reviews/Mo (5% tap):</span>
                    <strong id="newReviews" style="color:#38bdf8;">22 Reviews</strong>
                </div>

                <div class="roi-box">
                    <div style="font-size:12px; color:#a7f3d0; text-transform:uppercase; font-weight:700;">Projected New Monthly Revenue</div>
                    <div class="roi-val" id="revGain">+$1,950 CAD</div>
                    <div style="font-size:11px; color:#a7f3d0; margin-top:4px;">From ranking top 3 on 8th Street &amp; Broadway</div>
                </div>
            </div>

            <div class="card">
                <h2>3. The Unconditional Guarantee</h2>
                <div class="guarantee-box">
                    <strong>⭐️ The 30-Day "More Reviews or We Pay You" Promise:</strong><br>
                    "If this smart stand doesn't generate at least 15 verified 5-star Google reviews in the next 30 days, we refund 100% of your $97, let you keep the hardware free, and buy you a $50 gift card to a local Saskatoon restaurant."
                </div>
            </div>
        </div>

        <script>
            function calculateROI() {
                const ticket = parseFloat(document.getElementById('ticketVal').value) || 0;
                const cust = parseFloat(document.getElementById('custVal').value) || 0;
                const reviews = Math.round(cust * 0.05);
                document.getElementById('newReviews').innerText = reviews + " Reviews";
                
                // Conservatively: each 10 reviews brings ~15 new high-intent customers
                const newCustomers = Math.round((reviews / 10) * 14);
                const extraRevenue = newCustomers * ticket;
                document.getElementById('revGain').innerText = "+$" + extraRevenue.toLocaleString() + " CAD";
            }
            calculateROI();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

