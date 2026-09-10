"""Google Review Link Generator & NFC Target URL Builder.

Provides utility functions to:
1. Construct direct Google Review write-intent URLs using Google Place IDs or G.Page shortnames.
2. Construct dynamic agency redirect URLs with tracking parameters.
3. Validate URL formats for NFC chip memory limits (NTAG213 vs NTAG215).
"""

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlencode


@dataclass
class BusinessTarget:
    name: str
    slug: str
    place_id: Optional[str] = None
    g_page_shortcode: Optional[str] = None
    agency_domain: str = "tap.yxeagency.ca"


class GoogleReviewLinkBuilder:
    """Builds optimized direct Google review URLs and agency redirect URLs."""

    GOOGLE_PLACE_ID_BASE = "https://search.google.com/local/writereview"
    GOOGLE_GPAGE_BASE = "https://g.page/r"

    @classmethod
    def build_direct_google_url(cls, place_id: Optional[str] = None, g_page_shortcode: Optional[str] = None) -> str:
        """Constructs the fastest direct write-review intent URL.
        
        Args:
            place_id: Google Place ID (e.g. 'ChIJ3V8eYnTYBFMR8o9V29xZ1-E')
            g_page_shortcode: Verified GBP shortcode (e.g. 'CZZ_0QZ64vDVEBM')
            
        Returns:
            Direct URL that pops open the Google 5-star review modal.
        """
        if g_page_shortcode:
            clean_code = g_page_shortcode.strip("/ ")
            return f"{cls.GOOGLE_GPAGE_BASE}/{clean_code}/review"
        
        if place_id:
            clean_id = place_id.strip()
            params = {"placeid": clean_id}
            return f"{cls.GOOGLE_PLACE_ID_BASE}?{urlencode(params)}"
        
        raise ValueError("Either place_id or g_page_shortcode must be provided.")

    @classmethod
    def build_dynamic_nfc_url(
        cls,
        business_slug: str,
        agency_domain: str = "tap.yxeagency.ca",
        placement_source: str = "counter_stand",
        campaign: str = "saskatoon_launch",
    ) -> str:
        """Constructs the dynamic redirect URL to write onto the physical NFC chip.
        
        Always burn this URL onto the card, NEVER the static Google URL.
        """
        clean_domain = agency_domain.strip("/ ")
        clean_slug = business_slug.strip("/ ")
        params = {
            "src": placement_source,
            "cmp": campaign,
        }
        return f"https://{clean_domain}/r/{clean_slug}?{urlencode(params)}"

    @staticmethod
    def check_nfc_capacity_fit(url: str, chip_type: str = "NTAG215") -> dict:
        """Verifies if the URL fits within the designated NFC chip user memory."""
        byte_length = len(url.encode("utf-8"))
        limits = {
            "NTAG213": 144,
            "NTAG215": 504,
            "NTAG216": 888,
        }
        max_bytes = limits.get(chip_type.upper(), 504)
        fits = byte_length <= max_bytes
        return {
            "url": url,
            "byte_length": byte_length,
            "chip_type": chip_type.upper(),
            "max_capacity_bytes": max_bytes,
            "fits": fits,
            "remaining_bytes": max_bytes - byte_length if fits else 0,
        }
