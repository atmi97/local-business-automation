# NFC Card & Smart Stand Hardware Setup Guide

This guide walks you step-by-step through configuring NFC chips (NTAG215/216) and QR codes so that when a customer taps or scans, their smartphone immediately pops open the Google Review submission dialog in under 2 seconds.

---

## 1. Extracting the Exact Direct Google Review Link

Never send a customer to a business's generic Google Maps profile where they have to scroll, find the "Reviews" tab, and click "Write a review". Every extra tap reduces conversion by 40%.

### Method 1: The Official Google Business Profile Shortlink (Preferred)
If the owner has access to their Google Business Profile dashboard:
1. Go to [business.google.com](https://business.google.com).
2. Click on their business location.
3. On the main dashboard, look for the card titled **"Get more reviews"** or click the **"Ask for reviews"** button.
4. Google generates a verified shortlink in the format:
   ```text
   https://g.page/r/[13-digit-alphanumeric-code]/review
   ```
   *Example*: `https://g.page/r/CZZ_0QZ64vDVEBM/review`
5. Test the link in an incognito window: it should immediately trigger the 5-star modal overlay.

### Method 2: The Universal Place ID Review URL (No Owner Access Needed)
If you are prospecting or preparing a card before meeting the owner, you can generate their direct review link using their **Google Place ID**:
1. Go to Google's official [Place ID Finder](https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder).
2. Enter the business name and city (e.g., `"Keo's Kitchen Saskatoon"`).
3. Copy the alphanumeric Place ID (e.g., `ChIJQ9...`).
4. Append it to Google's direct review intent URL:
   ```text
   https://search.google.com/local/writereview?placeid=[PLACE_ID]
   ```
   *Example*:
   `https://search.google.com/local/writereview?placeid=ChIJ3V8eYnTYBFMR8o9V29xZ1-E`

---

## 2. The Golden Rule: The Dynamic Redirect Architecture

> [!CAUTION]
> **NEVER write the raw `g.page` or `google.com` URL directly onto the physical NFC chip!**

### Why Static Links Ruin Your Business:
- If a business cancels their subscription, changes their name, relocates, or changes their Place ID, the physical card becomes a useless brick.
- You cannot track analytics (daily taps, staff performance, conversion rates).
- You cannot upsell the **Smart Sentiment Funnel** (filtering negative reviews) later without physically visiting them and re-writing every card.

### The Solution: Your Dynamic Redirector
Always program the card with your custom branded redirect URL:
```text
https://tap.youragencydomain.ca/r/[business-slug]?source=nfc_counter
```
*Example flow:*
1. Customer taps card encoded with `https://tap.yxeagency.ca/r/korean-bbq-8th`
2. Your server records: Timestamp, Device (iOS/Android), Location ID.
3. Server instantly returns an HTTP `302 Found` redirecting to the direct Google Review URL (Latency: <30ms).
4. When the client upgrades to your software subscription, you simply toggle a switch in your dashboard: now that same URL routes to your interactive Sentiment Funnel!

---

## 3. Step-by-Step NFC Card Programming (Using Free Mobile Apps)

You do not need a desktop RFID reader. You can program cards anywhere in 15 seconds using your phone.

### App Setup
- **iOS**: Download **NFC Tools** by wakdev from the App Store (Free).
- **Android**: Download **NFC Tools** or **NXP TagWriter** from Google Play (Free).

### Programming Instructions (NFC Tools):
1. Open **NFC Tools** on your smartphone.
2. Select the **Write** tab.
3. Tap **Add a record**.
4. Select **URL / URI**.
5. Choose protocol `https://` and paste your dynamic redirect URL (e.g., `tap.youragency.ca/r/saskatoon-korean-bbq`).
6. Tap **OK**.
7. Tap **Write / [X] Bytes**.
8. **Position the card**:
   - **iPhone**: Hold the top edge of the iPhone directly over the center of the NFC card/stand.
   - **Android**: Hold the center-back of the Android device against the card (NFC antenna location varies by Android manufacturer).
9. You will see a green checkmark and hear a confirmation chime: **"Write complete!"**

### Optional: Write-Protection (Tag Locking)
- In high-traffic public venues, a tech-savvy customer could technically use NFC Tools to overwrite an unlocked tag.
- Under NFC Tools $\to$ **Other** $\to$ **Lock tag**, you can lock the chip to read-only mode.
- *Warning*: Only lock the tag if you are using dynamic URLs! Once locked, you can never change the URL on that chip.

---

## 4. Testing & Verification Checklist

Before delivering the card or stand to the client, verify across both major operating systems:

| Test Item | iPhone Verification | Android Verification | Pass/Fail |
| :--- | :--- | :--- | :--- |
| **Antenna Placement** | Top edge of iPhone (next to camera bump) within 2–3 cm. | Center-back or upper-back of Android. | [ ] |
| **Screen State** | Phone screen must be **ON / Awake** (doesn't need to be unlocked on newer iOS/Android). | Screen must be **ON / Unlocked**. | [ ] |
| **Prompt Response** | iOS banner notification appears: *"Open in Safari"*. Tap to open. | Android automatically opens default browser directly (no banner tap needed). | [ ] |
| **Review Dialog** | Direct 5-star rating overlay displays immediately. | Direct 5-star rating overlay displays immediately. | [ ] |
| **Redirect Speed** | < 2 seconds from tap to Google Review dialog. | < 2 seconds from tap to Google Review dialog. | [ ] |

---

## 5. High-Resolution QR Code Print Standards

Every physical NFC stand or card must also display a high-contrast QR code as a visual backup for customers with older phones or NFC disabled.

1. **Error Correction Level**: Use **Level M (15%)** or **Level Q (25%)**. This ensures the QR code scans reliably even if the acrylic surface gets scratched or smudged with fingerprints.
2. **Color & Contrast**: High contrast is mandatory. Dark elements (`#000000` or `#1A1A1A`) on a pure white background (`#FFFFFF`). Never use light pastel QR codes on white.
3. **Minimum Print Size**:
   - On Countertop Stands (4x6 inch): QR code should be at least **3.5 cm × 3.5 cm**.
   - On Pocket Cards (Credit card size): QR code should be at least **2.0 cm × 2.0 cm**.
4. **Resolution**: Always generate vector files (**SVG**) or **300+ DPI PNG** for physical printing to prevent pixelation blur.
