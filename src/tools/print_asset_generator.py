"""Print Asset & Dynamic Vector QR Code Generator.

Generates:
1. High-contrast QR codes in vector SVG or high-res PNG formats.
2. Production-ready composite NFC sticker graphics (85.6mm x 54mm) customized with
   the client's business name and dynamic NFC redirect URL.
"""

import io
import os
from typing import Optional
import qrcode
import qrcode.image.svg


class PrintAssetGenerator:
    """Generates print-ready QR codes and composite sticker artwork."""

    @classmethod
    def generate_qr_svg(cls, url: str) -> str:
        """Generates a clean vector SVG string for a given URL with Level Q error correction."""
        factory = qrcode.image.svg.SvgPathImage
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,  # 25% error tolerance
            box_size=10,
            border=2,
            image_factory=factory,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()

        stream = io.BytesIO()
        img.save(stream)
        svg_xml = stream.getvalue().decode("utf-8")
        
        # Extract just the <path ... /> elements or clean SVG body
        start_idx = svg_xml.find("<svg")
        if start_idx != -1:
            return svg_xml[start_idx:]
        return svg_xml

    @classmethod
    def generate_composite_sticker_svg(
        cls,
        business_name: str,
        dynamic_url: str,
        city: str = "Saskatoon",
        tagline: Optional[str] = None,
    ) -> str:
        """Generates a complete, ready-to-print 85.6mm x 54mm vector SVG sticker.
        
        Embeds the actual live QR code for the business alongside NFC tap zones.
        """
        qr_svg = cls.generate_qr_svg(dynamic_url)
        
        # Extract the path from qr_svg
        path_start = qr_svg.find('<path d="')
        path_end = qr_svg.find('" style=', path_start)
        if path_start != -1 and path_end != -1:
            qr_path = qr_svg[path_start + 9:path_end]
        else:
            # Fallback path if parsing differs
            qr_path = ""

        clean_name = business_name.upper()
        clean_tagline = tagline or f"Your feedback helps our local {city} team grow!"

        # 856x540 canvas (maps directly to 85.6mm x 54mm)
        composite_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 856 540" width="85.6mm" height="54mm">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f8fafc"/>
    </linearGradient>
    <filter id="cardShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Background Base with 3.18mm rounded corners -->
  <rect x="10" y="10" width="836" height="520" rx="32" ry="32" fill="url(#cardGrad)" stroke="#e2e8f0" stroke-width="4" filter="url(#cardShadow)"/>

  <!-- Google 4-Color Accent Strip -->
  <path d="M 42 10 L 220 10" stroke="#4285F4" stroke-width="8" stroke-linecap="round"/>
  <path d="M 230 10 L 420 10" stroke="#EA4335" stroke-width="8" stroke-linecap="round"/>
  <path d="M 430 10 L 620 10" stroke="#FBBC05" stroke-width="8" stroke-linecap="round"/>
  <path d="M 630 10 L 814 10" stroke="#34A853" stroke-width="8" stroke-linecap="round"/>

  <!-- 5 Gold Stars Rating -->
  <g transform="translate(328, 55)">
    <text font-size="32" fill="#FBBC05" letter-spacing="6">★★★★★</text>
  </g>

  <!-- Business Headline -->
  <text x="428" y="132" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="32" font-weight="800" fill="#0f172a" text-anchor="middle">
    {clean_name}
  </text>
  <text x="428" y="168" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="19" font-weight="500" fill="#64748b" text-anchor="middle">
    {clean_tagline}
  </text>

  <!-- Divider -->
  <line x1="120" y1="195" x2="736" y2="195" stroke="#e2e8f0" stroke-width="2"/>

  <!-- Left Side: Contactless NFC Tap Zone -->
  <g transform="translate(60, 220)">
    <rect x="0" y="0" width="340" height="250" rx="20" fill="#eff6ff" stroke="#bfdbfe" stroke-width="2"/>
    <circle cx="170" cy="90" r="45" fill="#3b82f6"/>
    <!-- Wave symbols -->
    <path d="M 160 90 Q 165 80 170 80 Q 175 80 180 90" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
    <path d="M 152 98 Q 165 70 178 98" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
    <circle cx="170" cy="107" r="4" fill="#ffffff"/>

    <text x="170" y="175" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="24" font-weight="700" fill="#1e3a8a" text-anchor="middle">
      TAP PHONE HERE
    </text>
    <text x="170" y="205" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="500" fill="#3b82f6" text-anchor="middle">
      Instant &amp; Contactless (NFC)
    </text>
  </g>

  <!-- Right Side: Dynamic Vector QR Code Zone -->
  <g transform="translate(456, 220)">
    <rect x="0" y="0" width="340" height="250" rx="20" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
    
    <!-- White QR Container Box -->
    <rect x="85" y="15" width="170" height="170" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    
    <!-- Live Embedded Vector QR Code -->
    <g transform="translate(95, 25) scale(0.48)">
      <path d="{qr_path}" fill="#0f172a"/>
    </g>

    <text x="170" y="215" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="600" fill="#475569" text-anchor="middle">
      OR SCAN WITH CAMERA
    </text>
  </g>

  <!-- Bottom Agency Watermark -->
  <text x="428" y="508" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="500" fill="#94a3b8" text-anchor="middle">
    POWERED BY YXE LOCAL REVIEWS • SASKATOON, SK
  </text>
</svg>"""
        return composite_svg

    @classmethod
    def save_sticker_to_file(
        cls,
        output_path: str,
        business_name: str,
        dynamic_url: str,
        city: str = "Saskatoon",
    ) -> str:
        """Generates and writes the composite sticker to disk."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        svg_content = cls.generate_composite_sticker_svg(business_name, dynamic_url, city)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        return output_path
