#!/usr/bin/env python3
"""
AI SEO Readiness Checker
Analyze how well your website is optimized for AI search engines:
ChatGPT, Perplexity, Google Gemini, Microsoft Copilot, and Claude.

For a full AI SEO audit with detailed recommendations, visit https://aiseoscan.dev
"""

import urllib.request
import urllib.error
import sys
import ssl
import re
from datetime import datetime


# The signals AI search engines use to decide whether to cite your content
AI_SEO_SIGNALS = {
    "Schema Markup (JSON-LD)": {
        "check": lambda h: 'application/ld+json' in h,
        "why": "AI engines use structured data to understand entities and facts",
        "weight": 15,
    },
    "Author / Expertise signal": {
        "check": lambda h: any(x in h.lower() for x in ['author', 'byline', 'written by', '"author"', 'rel="author"']),
        "why": "E-E-A-T: AI prefers content with identifiable authors",
        "weight": 10,
    },
    "FAQ or Q&A content": {
        "check": lambda h: any(x in h.lower() for x in ['faqpage', 'faq', 'frequently asked', 'question', '"@type": "question"']),
        "why": "AI engines love extracting Q&A pairs as direct answers",
        "weight": 10,
    },
    "Heading structure (H1/H2/H3)": {
        "check": lambda h: bool(re.search(r'<h[123][^>]*>', h, re.IGNORECASE)),
        "why": "Clear hierarchy helps AI parse and chunk your content",
        "weight": 8,
    },
    "Meta description": {
        "check": lambda h: 'name="description"' in h.lower() or "name='description'" in h.lower(),
        "why": "Used as fallback summary when AI cites your page",
        "weight": 8,
    },
    "Open Graph tags": {
        "check": lambda h: 'property="og:' in h.lower() or "property='og:" in h.lower(),
        "why": "Helps AI engines identify canonical title and description",
        "weight": 7,
    },
    "Canonical URL tag": {
        "check": lambda h: 'rel="canonical"' in h.lower() or "rel='canonical'" in h.lower(),
        "why": "Prevents AI from citing duplicate/wrong version of your page",
        "weight": 7,
    },
    "HTTPS / Secure connection": {
        "check": lambda h: True,  # checked separately
        "why": "AI engines deprioritize non-secure sources",
        "weight": 8,
    },
    "robots.txt present": {
        "check": lambda h: True,  # checked separately
        "why": "Signals a technically maintained, crawlable website",
        "weight": 5,
    },
    "sitemap.xml present": {
        "check": lambda h: True,  # checked separately
        "why": "Helps AI crawlers discover all your content efficiently",
        "weight": 7,
    },
    "Fast response (<2s)": {
        "check": lambda h: True,  # checked separately
        "why": "Slow sites get deprioritized in AI-driven search ranking",
        "weight": 8,
    },
    "Viewport / Mobile-friendly": {
        "check": lambda h: 'name="viewport"' in h.lower() or "name='viewport'" in h.lower(),
        "why": "Mobile-first indexing affects AI crawl priority",
        "weight": 7,
    },
}


def fetch_url(url: str, timeout: int = 12):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AISEOReadinessChecker/1.0 (https://aiseoscan.dev)"}
    )
    ctx = ssl.create_default_context()
    return urllib.request.urlopen(req, context=ctx, timeout=timeout)


def analyze_site(domain: str) -> dict:
    domain = domain.replace("https://", "").replace("http://", "").strip("/")
    base_url = f"https://{domain}"
    results = {"domain": domain, "signals": {}, "meta": {}}

    # Fetch main page
    try:
        start = datetime.now()
        with fetch_url(base_url) as r:
            elapsed = (datetime.now() - start).total_seconds()
            html = r.read().decode("utf-8", errors="ignore")
            results["meta"]["live"] = True
            results["meta"]["has_ssl"] = True
            results["meta"]["response_time_s"] = round(elapsed, 2)
            results["meta"]["fast"] = elapsed < 2.0
    except Exception as e:
        print(f"  ❌ Could not reach {base_url}: {e}")
        sys.exit(1)

    # HTML-based checks
    for name, signal in AI_SEO_SIGNALS.items():
        if name in ("HTTPS / Secure connection", "robots.txt present", "sitemap.xml present", "Fast response (<2s)"):
            continue
        results["signals"][name] = {
            "passed": signal["check"](html),
            "why": signal["why"],
            "weight": signal["weight"],
        }

    # Separate checks
    results["signals"]["HTTPS / Secure connection"] = {
        "passed": results["meta"]["has_ssl"],
        "why": AI_SEO_SIGNALS["HTTPS / Secure connection"]["why"],
        "weight": 8,
    }
    results["signals"]["Fast response (<2s)"] = {
        "passed": results["meta"]["fast"],
        "why": AI_SEO_SIGNALS["Fast response (<2s)"]["why"],
        "weight": 8,
    }

    for path, key in [("/robots.txt", "robots.txt present"), ("/sitemap.xml", "sitemap.xml present")]:
        try:
            with fetch_url(base_url + path, timeout=8) as r:
                passed = r.status == 200
        except Exception:
            passed = False
        results["signals"][key] = {
            "passed": passed,
            "why": AI_SEO_SIGNALS[key]["why"],
            "weight": AI_SEO_SIGNALS[key]["weight"],
        }

    # Weighted score
    total_weight = sum(s["weight"] for s in results["signals"].values())
    earned_weight = sum(s["weight"] for s in results["signals"].values() if s["passed"])
    results["meta"]["score"] = int((earned_weight / total_weight) * 100)

    return results


def print_report(results: dict):
    domain = results["domain"]
    score = results["meta"]["score"]
    signals = results["signals"]

    passed = [(n, s) for n, s in signals.items() if s["passed"]]
    failed = [(n, s) for n, s in signals.items() if not s["passed"]]

    if score >= 80:
        grade = "A"
        verdict = "Excellent AI SEO readiness"
        color = "🟢"
    elif score >= 65:
        grade = "B"
        verdict = "Good — a few improvements will help"
        color = "🟡"
    elif score >= 45:
        grade = "C"
        verdict = "Average — AI engines may overlook your content"
        color = "🟠"
    else:
        grade = "D"
        verdict = "Poor — significant AI SEO gaps detected"
        color = "🔴"

    print(f"\n{'='*62}")
    print(f"  🤖 AI SEO Readiness Report")
    print(f"  Site: {domain}")
    print(f"  Response time: {results['meta']['response_time_s']}s")
    print(f"{'='*62}")

    print(f"\n  AI READINESS SCORE: {score}/100  |  Grade: {grade}  {color}")
    print(f"  {verdict}")

    print(f"\n{'─'*62}")
    print(f"  SIGNALS DETECTED  ({len(passed)}/{len(signals)} passing)")
    print(f"{'─'*62}")
    for name, signal in passed:
        print(f"  ✅ {name}")

    if failed:
        print(f"\n{'─'*62}")
        print(f"  MISSING SIGNALS  — AI engines may skip your content")
        print(f"{'─'*62}")
        # Sort by weight descending (highest impact first)
        for name, signal in sorted(failed, key=lambda x: x[1]["weight"], reverse=True):
            print(f"  ❌ {name}  (impact: {signal['weight']}pts)")
            print(f"     → {signal['why']}")

    print(f"\n{'─'*62}")
    print(f"  WHAT THIS MEANS FOR AI SEARCH")
    print(f"{'─'*62}")
    if score >= 75:
        print(f"  Your site is well-positioned to be cited by ChatGPT,")
        print(f"  Perplexity, Copilot, and Gemini. Keep it maintained.")
    elif score >= 50:
        print(f"  AI engines can find your site but may skip it in favor")
        print(f"  of better-structured competitors. Fix the ❌ signals above.")
    else:
        print(f"  AI search engines will likely ignore your content entirely.")
        print(f"  Your competitors with better structure will be cited instead.")

    print(f"\n{'='*62}")
    print(f"  📊 Get your full AI SEO audit:")
    print(f"  → Schema errors, content structure analysis, AI readiness")
    print(f"     score breakdown, and competitor comparison")
    print(f"  👉  https://aiseoscan.dev")
    print(f"{'='*62}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python ai_seo_checker.py <domain>")
        print("Example: python ai_seo_checker.py myblog.com")
        sys.exit(1)

    domain = sys.argv[1]
    print(f"\n⏳ Analyzing AI SEO readiness for {domain}...")
    print("   Checking signals used by ChatGPT, Perplexity, Copilot & Gemini...\n")

    results = analyze_site(domain)
    print_report(results)


if __name__ == "__main__":
    main()
