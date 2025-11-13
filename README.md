# Discord Server Scraper

> This tool collects detailed data about public Discord communities, giving you a clear view of member counts, server structure, categories, features, and overall activity. It helps you uncover niche communities, monitor competitors, and evaluate server trends with clean, structured information.

> If you need accurate and extensive Discord server data for research, analytics, or growth insights, this scraper gives you everything in one place.


<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Discord Server Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

The Discord Server Scraper gathers publicly available information from Discord’s server discovery ecosystem. It lets you search by keywords or browse by category, then returns structured JSON containing server metadata, activity measurements, and configuration details.

It’s built for analysts, community managers, growth strategists, and researchers who need reliable, high-volume server insights.

### How It Helps You Work Smarter

- Finds relevant servers using keyword and category-based search.
- Gathers member counts, presence metrics, server features, and category tags.
- Handles pagination automatically to process thousands of results.
- Structures everything in clean JSON for hassle-free integration.
- Supports large-scale competitive or market research workflows.

## Features

| Feature | Description |
|---------|-------------|
| Complete Server Data | Retrieves names, descriptions, counts, locales, categories, tags, and more. |
| Keyword Search | Locate servers matching specific keywords or interests. |
| Category Filtering | Narrow results to targeted Discord categories like Gaming or Science & Tech. |
| Pagination Automation | Efficiently cycles through large result sets without manual handling. |
| Metadata Extraction | Pulls features, vanity URLs, banners, icons, boosts, and other details. |
| JSON Output | Consistent and parse-ready dataset for analysis or automation. |
| Robust Handling | Uses retries and smart processing to reduce failed requests. |
| Multi-category Discovery | When no category is given, scans all categories for maximum coverage. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|------------|------------------|
| id | Unique identifier for the Discord server. |
| name | Public display name of the server. |
| description | Server’s public description. |
| icon | Hash of the server’s icon image. |
| splash | Server splash image identifier. |
| banner | Banner image identifier. |
| approximate_presence_count | Number of active/online users. |
| approximate_member_count | Total member count. |
| premium_subscription_count | Number of boosts the server has. |
| preferred_locale | Primary language of the server. |
| auto_removed | Whether the server is marked as auto-removed. |
| discovery_splash | Discovery splash background image. |
| primary_category_id | ID of the main category attached to the server. |
| vanity_url_code | Custom invite code if available. |
| is_published | Indicates if the server is published in discovery. |
| keywords | List of keyword tags associated with the server. |
| features | Array of enabled server features. |
| categories | Array describing server categories. |
| primary_category | Full object describing primary category. |
| objectID | Unique object identifier. |

---

## Example Output


    {
        "id": "662267976984297473",
        "name": "Midjourney",
        "description": "The official server for Midjourney, a text-to-image AI where your imagination is the only limit.",
        "icon": "39128f6c9fc33f4c95a27d4c601ad7db",
        "splash": "4798759e115d2500fef16347d578729a",
        "banner": "63249e6867f276efc07d32793b7b3b5a",
        "approximate_presence_count": 1353819,
        "approximate_member_count": 21165793,
        "premium_subscription_count": 569,
        "preferred_locale": "en-US",
        "auto_removed": false,
        "discovery_splash": "4798759e115d2500fef16347d578729a",
        "primary_category_id": 5,
        "vanity_url_code": "midjourney",
        "is_published": true,
        "keywords": ["AI","artificial intelligence","art","creativity","future"],
        "features": [
            "COMMUNITY",
            "DISCOVERABLE",
            "ENABLED_DISCOVERABLE_BEFORE",
            "PREVIEW_ENABLED",
            "VERIFIED",
            "WELCOME_SCREEN_ENABLED"
        ],
        "categories": [
            {"id":3,"is_primary":true,"name":"Entertainment","name_localizations":{}},
            {"id":4,"is_primary":true,"name":"Creative Arts","name_localizations":{}},
            {"id":38,"is_primary":false,"name":"Collaboration","name_localizations":{}},
            {"id":40,"is_primary":false,"name":"Wiki & Guide","name_localizations":{}},
            {"id":5,"is_primary":true,"name":"Science & Tech","name_localizations":{}}
        ],
        "primary_category": {
            "id":5,
            "is_primary":true,
            "name":"Science & Tech",
            "name_localizations":{}
        },
        "objectID": "662267976984297473",
        "_highlightResult": {}
    }

---

## Directory Structure Tree


    Discord Server Scraper/
    ├── src/
    │   ├── main.py
    │   ├── client/
    │   │   ├── discord_api.py
    │   │   └── paginator.py
    │   ├── processors/
    │   │   ├── parser.py
    │   │   └── sanitizer.py
    │   ├── utils/
    │   │   ├── request_handler.py
    │   │   └── logger.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── sample.json
    │   └── keywords.txt
    ├── tests/
    │   ├── test_parser.py
    │   └── test_api.py
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Analysts** use it to research server categories and member statistics, so they can evaluate community size and popularity.
- **Community managers** use it to scout similar or competing servers, so they can improve engagement or structure.
- **Growth strategists** use it to study feature-rich or fast-growing servers, so they can identify what drives success.
- **Researchers** use it to analyze trends in language usage, server topics, or metadata patterns.
- **Marketing teams** use it to discover niche communities, so they can understand audience behavior more accurately.

---

## FAQs

**Does it collect private server data?**
No. It only retrieves information publicly available through Discord’s discovery system.

**How many servers can it gather in one run?**
Up to 3,000 servers per keyword or per category. When no category is specified, it cycles through all categories for broader coverage.

**Can I filter results by topic or niche?**
Yes. You can search by keywords or restrict the scan to a specific category like Gaming or Science & Tech.

**What format is the output in?**
All results are returned as structured JSON for easy parsing, storage, or analysis.

---

## Performance Benchmarks and Results

**Primary Metric:** Processes several hundred servers per minute on average, depending on keyword breadth and category selection.
**Reliability Metric:** Maintains a high success rate thanks to retry logic and resilient request handling.
**Efficiency Metric:** Handles large result sets with minimal overhead by batching requests and managing pagination internally.
**Quality Metric:** Returns consistently complete datasets, including member counts, tags, categories, and feature flags with strong accuracy.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
