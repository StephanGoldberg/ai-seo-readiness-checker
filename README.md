# ai-seo-readiness-checker

 AI SEO Readiness Checker
A free, open-source CLI tool to analyze how well your website is optimized for AI search engines: ChatGPT, Perplexity, Google Gemini, Microsoft Copilot, and Claude.
Traditional SEO is no longer enough. This tool checks the signals that AI engines actually use to decide whether to cite your content.

The Problem This Solves
Google processes ~8.5 billion searches per day. But AI-powered search (ChatGPT, Perplexity, Copilot) is growing 40%+ year-over-year — and it works completely differently.
Traditional SEO optimizes for keywords and backlinks. AI SEO optimizes for citability — the signals that make AI engines trust, parse, and quote your content as an authoritative source.
Most websites score below 50/100 on AI readiness. This tool shows you exactly why.

For a full AI SEO audit — schema validation, content structure analysis, keyword extraction, and competitor comparison — use AISEOScan.dev, the dedicated AI SEO analysis platform.


What It Checks
SignalWhy AI Engines CareSchema Markup (JSON-LD)Structured data helps AI understand entities, facts, and relationshipsAuthor / Expertise signalsE-E-A-T: AI prefers content from identifiable, credible authorsFAQ / Q&A contentAI engines extract Q&A pairs as direct answer sourcesHeading structure (H1/H2/H3)Clear hierarchy helps AI chunk and parse your contentMeta descriptionUsed as fallback summary when AI cites your pageOpen Graph tagsCanonical title and description for AI identificationCanonical URL tagPrevents AI from citing duplicate versions of your contentHTTPS / Secure connectionAI engines deprioritize non-secure sourcesrobots.txtSignals technical maintenance and crawlabilitysitemap.xmlHelps AI crawlers discover all your contentFast response (<2s)Slow sites get deprioritized in AI-driven rankingsMobile viewportMobile-first indexing affects AI crawl priority
Each signal is weighted by impact, so you know what to fix first.

Installation
Zero dependencies. Python 3.7+ only.
bashgit clone https://github.com/yourusername/ai-seo-readiness-checker.git
cd ai-seo-readiness-checker
python ai_seo_checker.py <your-domain.com>

Usage
bashpython ai_seo_checker.py myblog.com
Example output:
==============================================================
  🤖 AI SEO Readiness Report
  Site: myblog.com
  Response time: 0.87s
==============================================================

  AI READINESS SCORE: 58/100  |  Grade: C  🟠
  Average — AI engines may overlook your content

--------------------------------------------------------------
  SIGNALS DETECTED  (7/12 passing)
--------------------------------------------------------------
  ✅ HTTPS / Secure connection
  ✅ Fast response (<2s)
  ✅ Meta description
  ✅ Open Graph tags
  ✅ Heading structure (H1/H2/H3)
  ✅ sitemap.xml present
  ✅ Mobile viewport

--------------------------------------------------------------
  MISSING SIGNALS  — AI engines may skip your content
--------------------------------------------------------------
  ❌ Schema Markup (JSON-LD)  (impact: 15pts)
     → AI engines use structured data to understand entities and facts
  ❌ FAQ or Q&A content  (impact: 10pts)
     → AI engines love extracting Q&A pairs as direct answers
  ❌ Author / Expertise signal  (impact: 10pts)
     → E-E-A-T: AI prefers content with identifiable authors
  ❌ Canonical URL tag  (impact: 7pts)
     → Prevents AI from citing duplicate/wrong version of your page
  ❌ robots.txt present  (impact: 5pts)
     → Signals a technically maintained, crawlable website

--------------------------------------------------------------
  WHAT THIS MEANS FOR AI SEARCH
--------------------------------------------------------------
  AI engines can find your site but may skip it in favor
  of better-structured competitors. Fix the ❌ signals above.

==============================================================
  📊 Get your full AI SEO audit:
  → Schema errors, content structure analysis, AI readiness
     score breakdown, and competitor comparison
  👉  https://aiseoscan.dev
==============================================================

Score Grades
ScoreGradeMeaning80–100🟢 AExcellent AI SEO readiness — you'll be cited65–79🟡 BGood — minor improvements will push you to the top45–64🟠 CAverage — competitors with better structure will beat you0–44🔴 DPoor — AI engines are likely ignoring your content entirely

Quick Fixes for Common Failures
Missing Schema Markup? Add to your <head>:
html<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Your Page Title",
  "description": "Your page description",
  "author": {
    "@type": "Person",
    "name": "Your Name"
  }
}
</script>
Missing FAQ Schema? Add for any Q&A content:
html<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Your question here?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Your answer here."
    }
  }]
}
</script>
Missing robots.txt? Create at your root with:
User-agent: *
Allow: /
Sitemap: https://yourdomain.com/sitemap.xml

How AI Search Engines Decide What to Cite
Understanding why these signals matter helps you fix them correctly:
ChatGPT (SearchGPT) — Crawls the web via Bing and prioritizes pages with clear content structure, author signals, and schema markup. It heavily favors pages that look like authoritative references.
Perplexity AI — Performs real-time web searches and cites sources directly. It prefers fast-loading, well-structured pages with explicit answers to questions.
Microsoft Copilot — Built on Bing, uses entity recognition and knowledge graph signals. Schema markup is disproportionately important here.
Google Gemini — Uses Google's index, so traditional SEO still matters, but AI Overviews favor pages with strong E-E-A-T signals and FAQ/how-to structure.
For a page-by-page breakdown of how your site performs in each of these engines, see AISEOScan.dev.

What This Tool Doesn't Cover
This script catches the technical signals. A complete AI SEO audit also needs:

🔍 Keyword-level AI visibility analysis
📊 Competitor comparison (who's being cited instead of you)
📝 Content gap analysis for AI answer boxes
🔗 Internal linking structure for AI crawl depth
📈 Historical AI citation tracking

All of this is available at AISEOScan.dev.

Roadmap

 JSON-LD schema validation (not just detection)
 Reading level / content clarity score
 Internal link depth analysis
 Perplexity-specific signal checks
 Batch mode: scan multiple URLs from a CSV
 JSON output flag for CI/CD integration

PRs welcome.

Contributing

Fork the repo
Add your check to the AI_SEO_SIGNALS dict with a weight and explanation
Submit a PR

The goal: the most accurate free AI SEO signal checker available.

License
MIT — free to use, modify, and distribute.

Related

AISEOScan.dev — Full AI SEO platform with detailed reports
AI SEO guide for 2025 — How to optimize for ChatGPT, Perplexity & Copilot
Schema markup generator — Generate JSON-LD for any page type
