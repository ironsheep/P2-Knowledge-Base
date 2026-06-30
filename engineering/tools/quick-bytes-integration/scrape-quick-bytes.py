#!/usr/bin/env python3
"""
Build the Quick Bytes served catalog for the P2 Knowledge Base.

For each of the 42 Quick Bytes in the discovery manifest this:
  - fetches the WordPress/Elementor page (polite ~1s delay, one retry),
  - saves the raw HTML (for a downstream format-donor task),
  - extracts: JSON-LD poster author, "Source Code Author", body /tag/ slugs,
    YouTube embed(s), source-code download packages (link-not-adopt),
    external reference links, OBEX cross-references,
  - merges with manifest + capability classification (the spine), and
  - emits one catalog YAML per Quick Byte mirroring the OBEX serving style.

Source code is NOT downloaded — we record has_code + the page URL to get it from
(Parallax WP Download Manager). Classification follows
engineering/standards/p2-capability-taxonomy.md (QB-tag -> domain table); the
per-QB primary domain/leaf + secondary + type are curated below in QB_DATA.

Output:  deliverables/ai/P2/community/quick-bytes/<slug>.yaml
Raw HTML: <scratchpad>/qb-raw/<slug>.html
"""

import sys
import re
import time
import json
import html as ihtml
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import yaml

SCRAPED_DATE = "2026-06-29"  # hardcoded per task; do not call datetime.now()

REPO = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO / "deliverables/ai/P2/community/quick-bytes"
RAW_HTML_DIR = Path(
    "/tmp/claude-1000/-workspaces-P2-Knowledge-Base/"
    "206005c3-82d4-4bc5-9ef1-bd75dbadfbea/scratchpad/qb-raw"
)

# Package slugs that are generic Parallax tools, never the QB's own source code.
GENERIC_PACKAGE_FRAGMENTS = [
    "propeller-tool", "simpleide", "flexprop", "basic-stamp",
    "propeller-c-software", "blocklyprop", "pnut", "parallax-ide",
    "software-for-windows", "propeller-1", "propworks", "spin-tool",
    "propeller-2-software",
]

# Reference-link host blocklist (toolchain/lang-doc boilerplate repeated on every QB).
REF_BLOCK_HOSTS = ["docs.google.com", "patreon.com", "youtube.com", "youtu.be"]

# A generic "Propeller 2" promo video re-embedded (as og:video / iframe) on several
# pages that have no demo video of their own — never the QB's own demo.
PROMO_VIDEO_IDS = {"K-pGbQD_biE"}

YT_RE = re.compile(
    r"(?:youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=|v/)|youtu\.be/)"
    r"([A-Za-z0-9_-]{6,})"
)

# Re-fetch from the network even when a cached raw HTML file exists.
FORCE_REFETCH = "--refetch" in sys.argv


# ---------------------------------------------------------------------------
# Manifest + capability classification (the single source of curated metadata).
# date is ISO; capability per p2-capability-taxonomy.md; type = reusable-object
# | procedural; boards = add-on board codes the manifest cross-references.
# ---------------------------------------------------------------------------
QB_DATA = {
    "1-wire-driver-with-ds18b20-temperature-sensor-demo": {
        "title": "1-Wire Driver with DS18B20 Temperature Sensor Demo",
        "date": "2023-01-18", "type": "reusable-object",
        "domain": "E", "leaf": "1-wire",
        "secondary": [{"domain": "F", "leaf": "temperature-humidity"}],
        "boards": [],
    },
    "32-channel-adc-object": {
        "title": "32-Channel ADC Object",
        "date": "2021-01-19", "type": "reusable-object",
        "domain": "B", "leaf": "adc", "secondary": [], "boards": [],
    },
    "320x240-lcd-driver-for-ili9341-controller-and-xpt2046-touch-screen": {
        "title": "320x240 LCD Driver for ILI9341 Controller and XPT2046 Touch Screen",
        "date": "2021-03-03", "type": "reusable-object",
        "domain": "G", "leaf": "lcd-eink",
        "secondary": [{"domain": "F", "leaf": "touch-capacitive"},
                      {"domain": "E", "leaf": "spi"}],
        "boards": [],
    },
    "arlo-conversion-to-p2-with-the-universal-motor-controller": {
        "title": "Arlo Conversion to P2 with the Universal Motor Controller",
        "date": "2022-01-24", "type": "reusable-object",
        "domain": "H", "leaf": "robotics", "secondary": [], "boards": [],
    },
    "breakout-board-options-for-p2": {
        "title": "Breakout Board Options for P2 Edge Modules",
        "date": "2023-03-15", "type": "procedural",
        "domain": "K", "leaf": "project-template", "secondary": [], "boards": [],
    },
    "brushless-dc-motor-control-demo": {
        "title": "Brushless DC Motor Control Demo",
        "date": "2022-08-25", "type": "reusable-object",
        "domain": "H", "leaf": "brushless-bldc", "secondary": [], "boards": [],
    },
    "colorful-terminal-output-with-ansi-escape-sequences": {
        "title": "Colorful Terminal Output with ANSI Escape Sequences",
        "date": "2021-02-06", "type": "reusable-object",
        "domain": "G", "leaf": "terminal-ansi", "secondary": [], "boards": [],
    },
    "visual-studio": {
        "title": "Configuring Visual Studio Code for Programming the P2 on Mac, Windows, and Linux",
        "date": "2021-03-14", "type": "procedural",
        "domain": "K", "leaf": "toolchain-editor", "secondary": [], "boards": [],
    },
    "dht11-dht22-cm2302-object": {
        "title": "DHT11, DHT22, CM2302 Humidity and Temperature Sensor Object",
        "date": "2021-01-22", "type": "reusable-object",
        "domain": "F", "leaf": "temperature-humidity", "secondary": [], "boards": [],
    },
    "digital-sample-adc-to-dac-analog-frequency-to-dac": {
        "title": "Digital Sample ADC to DAC + Analog Frequency to DAC",
        "date": "2022-11-01", "type": "reusable-object",
        "domain": "B", "leaf": "adc",
        "secondary": [{"domain": "B", "leaf": "dac"},
                      {"domain": "J", "leaf": "dac-audio"}],
        "boards": [],
    },
    "ds3231-real-time-clock-i2c-demo": {
        "title": "DS3231 Real Time Clock I2C Demo",
        "date": "2021-01-23", "type": "reusable-object",
        "domain": "F", "leaf": "rtc",
        "secondary": [{"domain": "E", "leaf": "i2c"}], "boards": [],
    },
    "dvi-vga-text-driver-demo": {
        "title": "DVI/VGA Text Driver Demo",
        "date": "2021-02-15", "type": "reusable-object",
        "domain": "G", "leaf": "vga-dvi-hdmi-driver",
        "secondary": [{"domain": "D", "leaf": "hdmi-dvi-vga-signal"}],
        "boards": ["64006H"],
    },
    "e-ink-display-demo": {
        "title": "E-Ink Display Demo",
        "date": "2022-08-22", "type": "reusable-object",
        "domain": "G", "leaf": "lcd-eink", "secondary": [], "boards": [],
    },
    "five-buttons-on-one-pin": {
        "title": "Five Buttons On One Pin",
        "date": "2021-02-21", "type": "reusable-object",
        "domain": "F", "leaf": "human-input",
        "secondary": [{"domain": "B", "leaf": "adc"}], "boards": ["64006A"],
    },
    "floating-point-math": {
        "title": "Floating Point Math: DEBUG and Terminal Display Example",
        "date": "2022-01-16", "type": "reusable-object",
        "domain": "C", "leaf": "fixed-floating-point",
        "secondary": [{"domain": "K", "leaf": "debug-windows"}], "boards": [],
    },
    "goertzel-operation-with-ultrasonic-transducers": {
        "title": "Goertzel Operation with Ultrasonic Transducers",
        "date": "2021-02-20", "type": "reusable-object",
        "domain": "C", "leaf": "goertzel",
        "secondary": [{"domain": "F", "leaf": "distance-ultrasonic"}],
        "boards": ["64006G"],
    },
    "i2c-device-bus-scanner": {
        "title": "I2C Device Bus Scanner Utility",
        "date": "2021-01-11", "type": "reusable-object",
        "domain": "E", "leaf": "i2c", "secondary": [], "boards": [],
    },
    "i-o-test-utility-with-led-matrix": {
        "title": "LED Matrix used as an I/O Test Utility",
        "date": "2021-01-15", "type": "reusable-object",
        "domain": "G", "leaf": "led-matrix-neopixel",
        "secondary": [{"domain": "K", "leaf": "debug-windows"}],
        "boards": ["64006C"],
    },
    "leds-beyond-the-basics": {
        "title": "LEDs - Beyond the Basics",
        "date": "2021-02-17", "type": "reusable-object",
        "domain": "B", "leaf": "pwm-nco",
        "secondary": [{"domain": "G", "leaf": "led-matrix-neopixel"}],
        "boards": ["64006A"],
    },
    "max7219-led-display-spi-demo": {
        "title": "MAX7219 LED Display SPI Demo",
        "date": "2021-01-28", "type": "reusable-object",
        "domain": "G", "leaf": "led-matrix-neopixel",
        "secondary": [{"domain": "E", "leaf": "spi"}], "boards": ["64006C"],
    },
    "multiple-serial-port-16-object": {
        "title": "Multiple Serial Port (8 UART - 16 Tx/Rx) Object",
        "date": "2021-01-28", "type": "reusable-object",
        "domain": "E", "leaf": "uart-serial", "secondary": [], "boards": [],
    },
    "multiple-servo-control-up-to-64-object": {
        "title": "Multiple Servo Control (up to 64) Object",
        "date": "2021-01-26", "type": "reusable-object",
        "domain": "H", "leaf": "servo", "secondary": [], "boards": ["64006D"],
    },
    "nmea-gps-string-parsing": {
        "title": "NMEA GPS String Parsing",
        "date": "2023-01-19", "type": "reusable-object",
        "domain": "F", "leaf": "gps-nmea", "secondary": [], "boards": [],
    },
    "p2-edge-16-mb-flash-reader-and-explorer-utility": {
        "title": "P2 Edge 16 MB Flash Reader and Explorer Utility",
        "date": "2021-01-31", "type": "reusable-object",
        "domain": "I", "leaf": "flash",
        "secondary": [{"domain": "E", "leaf": "spi"}], "boards": [],
    },
    "p2-rtc-add-on-board-demo": {
        "title": "P2 RTC Add-on Board Demo",
        "date": "2023-01-26", "type": "reusable-object",
        "domain": "F", "leaf": "rtc", "secondary": [], "boards": [],
    },
    "p2-rtc-add-on-with-gps-module": {
        "title": "P2 RTC Add-on with GPS Module",
        "date": "2023-01-26", "type": "reusable-object",
        "domain": "F", "leaf": "rtc",
        "secondary": [{"domain": "F", "leaf": "gps-nmea"}], "boards": [],
    },
    "pcf8574-i2c-lcd-demo": {
        "title": "PCF8574 I2C LCD Demo",
        "date": "2021-02-01", "type": "reusable-object",
        "domain": "G", "leaf": "lcd-eink",
        "secondary": [{"domain": "E", "leaf": "i2c"}], "boards": [],
    },
    "ping-ultrasonic-distance-sensor-with-graphical-debug-demo": {
        "title": "Ping))) Ultrasonic Distance Sensor with Graphical Debug Demo",
        "date": "2021-03-21", "type": "reusable-object",
        "domain": "F", "leaf": "distance-ultrasonic",
        "secondary": [{"domain": "K", "leaf": "debug-windows"}], "boards": [],
    },
    "rotary-encoder": {
        "title": "Quadrature Encoder Object",
        "date": "2021-01-15", "type": "reusable-object",
        "domain": "B", "leaf": "quadrature-decode",
        "secondary": [{"domain": "F", "leaf": "human-input"},
                      {"domain": "H", "leaf": "quadrature-encoder"}],
        "boards": [],
    },
    "send-email-from-the-propeller-2-using-the-iot-gateway-on-raspberry-pi": {
        "title": "Send Email from the Propeller 2 Using the IoT Gateway on Raspberry Pi",
        "date": "2022-02-24", "type": "reusable-object",
        "domain": "E", "leaf": "iot-gateway",
        "secondary": [{"domain": "K", "leaf": "host-integration"}], "boards": [],
    },
    "simple-analog-input": {
        "title": "Simple Analog Input",
        "date": "2021-01-11", "type": "reusable-object",
        "domain": "B", "leaf": "adc", "secondary": [], "boards": [],
    },
    "simple-sound-engine-demo": {
        "title": "Simple Sound Engine Demo",
        "date": "2021-02-13", "type": "reusable-object",
        "domain": "J", "leaf": "sound-engine", "secondary": [], "boards": ["64006H"],
    },
    "p2-simple-video-driver-using-images-intro-to-using-video-2-of-3": {
        "title": "Simple Video Driver - Using Images (Intro to Using Video 2 of 3)",
        "date": "2022-08-22", "type": "reusable-object",
        "domain": "G", "leaf": "vga-dvi-hdmi-driver",
        "secondary": [{"domain": "D", "leaf": "pixel-scanline"}],
        "boards": ["64006H"],
    },
    "solar-panel-monitoring-demo-intro-to-using-video-3-of-3": {
        "title": "Solar Panel Monitoring Demo (Intro to Using Video 3 of 3)",
        "date": "2022-08-22", "type": "reusable-object",
        "domain": "G", "leaf": "vga-dvi-hdmi-driver",
        "secondary": [{"domain": "F", "leaf": "light-optical"},
                      {"domain": "E", "leaf": "iot-gateway"}],
        "boards": [],
    },
    "starting-your-p2-project-with-a-spin2-template": {
        "title": "Starting Your P2 Project with a Spin2 Template",
        "date": "2021-02-05", "type": "procedural",
        "domain": "K", "leaf": "project-template", "secondary": [], "boards": [],
    },
    "tetris": {
        "title": "Tetris",
        "date": "2021-02-14", "type": "reusable-object",
        "domain": "G", "leaf": "gui",
        "secondary": [{"domain": "J", "leaf": "sound-engine"}], "boards": [],
    },
    "smart-pins-tsl235r": {
        "title": "Using Smart Pins to Measure Frequency Output of TSL235R Light-to-Frequency Sensor",
        "date": "2021-03-14", "type": "reusable-object",
        "domain": "B", "leaf": "frequency-measurement",
        "secondary": [{"domain": "F", "leaf": "light-optical"}], "boards": [],
    },
    "video-hardware-character-map": {
        "title": "Video Hardware with Character Map Demo (Intro to Using Video 1 of 3)",
        "date": "2022-08-22", "type": "reusable-object",
        "domain": "G", "leaf": "vga-dvi-hdmi-driver",
        "secondary": [{"domain": "D", "leaf": "pixel-scanline"}],
        "boards": ["64006H"],
    },
    "web-page-control-of-ws2811-leds-using-the-iot-gateway-on-raspberry-pi": {
        "title": "Web Page Control of WS2811 LEDs Using the IoT Gateway on Raspberry Pi",
        "date": "2022-09-01", "type": "reusable-object",
        "domain": "E", "leaf": "iot-gateway",
        "secondary": [{"domain": "G", "leaf": "led-matrix-neopixel"},
                      {"domain": "K", "leaf": "host-integration"}],
        "boards": [],
    },
    "wireless-programming": {
        "title": "Wireless Programming with the ESP8266 WX Module",
        "date": "2021-01-17", "type": "procedural",
        "domain": "K", "leaf": "programming-loading",
        "secondary": [{"domain": "E", "leaf": "wireless"}], "boards": [],
    },
    "ws2811-ws2812-ws2812b-ws2813-sk6812x-neopixel-object": {
        "title": "WS2811, WS2812, WS2812b, WS2813, SK6812x NeoPixel Object",
        "date": "2021-01-20", "type": "reusable-object",
        "domain": "G", "leaf": "led-matrix-neopixel", "secondary": [], "boards": [],
    },
    "xbee-rf-transparent-and-api-mode-demo": {
        "title": "XBee RF Transparent and API Mode Demo",
        "date": "2021-02-28", "type": "reusable-object",
        "domain": "E", "leaf": "wireless", "secondary": [], "boards": [],
    },
}


def load_html(slug, url):
    """Return raw HTML for the page: use the cached copy if present (and not
    --refetch), otherwise GET with one retry and save it."""
    cache = RAW_HTML_DIR / f"{slug}.html"
    if cache.exists() and cache.stat().st_size > 0 and not FORCE_REFETCH:
        return cache.read_text(encoding="utf-8"), True
    last = None
    for _ in range(2):
        try:
            r = requests.get(url, timeout=20,
                             headers={"User-Agent": "P2KB-quick-bytes-catalog/1.0"})
            r.raise_for_status()
            RAW_HTML_DIR.mkdir(parents=True, exist_ok=True)
            cache.write_text(r.text, encoding="utf-8")
            return r.text, False
        except Exception as e:  # noqa
            last = e
            time.sleep(2)
    raise last


def jsonld_author(html):
    """First JSON-LD author Person name."""
    m = re.search(r'"author":\s*\{[^}]*?"name":\s*"([^"]+)"', html)
    return m.group(1).strip() if m else ""


def extract_tags(soup):
    seen, out = set(), []
    for a in soup.find_all("a", href=re.compile(r"parallax\.com/tag/")):
        m = re.search(r"/tag/([a-z0-9-]+)/", a.get("href", ""))
        if m and m.group(1) not in seen:
            seen.add(m.group(1))
            out.append(m.group(1))
    return out


def extract_code_author(soup):
    """The 'Source Code Author' metadata column holds one or more icon-list
    value items (multiple = co-authors). Join them with ', '."""
    for el in soup.find_all(string=re.compile(r"Source Code Author")):
        col = el
        # Preferred: the leaf column whose heading is exactly Source Code Author
        node = el
        for _ in range(8):
            node = node.parent
            if node is None:
                break
            if "elementor-column" in " ".join(node.get("class", [])):
                heads = [re.sub(r"\s+", " ", h.get_text(" ", strip=True))
                         for h in node.find_all(class_=re.compile("elementor-widget-heading"))]
                if "Source Code Author" in heads and "Document Author" not in heads:
                    vals = [re.sub(r"\s+", " ", v.get_text(" ", strip=True))
                            for v in node.find_all(class_="elementor-icon-list-text")]
                    vals = [v for v in vals if v]
                    if vals:
                        return ", ".join(vals)
                    txt = re.sub(r"\s+", " ", node.get_text(" ", strip=True))
                    m = re.match(r"Source Code Author\s*(.+)$", txt)
                    if m:
                        return re.split(r"\s{2,}", m.group(1).strip())[0].strip()
                    return ""
        # Fallback: nearest column with icon-list values
        col = el
        for _ in range(8):
            col = col.parent
            if col is None:
                break
            if "elementor-column" in " ".join(col.get("class", [])):
                vals = [re.sub(r"\s+", " ", v.get_text(" ", strip=True))
                        for v in col.find_all(class_="elementor-icon-list-text")]
                vals = [v for v in vals if v]
                if vals:
                    return ", ".join(vals)
                break
    return ""


def extract_youtube(soup):
    """The QB demo video. Primary source is the Elementor video widget
    (data-settings youtube_url); a few older pages embed it as an in-content
    iframe. Returns (primary_id_or_'', all_ids_found). The recurring promo
    video is excluded from the iframe fallback. Supplementary 'Live Forum'
    <a> links are intentionally ignored."""
    ds_ids = []
    for tag in soup.find_all(attrs={"data-settings": True}):
        d = ihtml.unescape(tag["data-settings"])
        m = re.search(r'"youtube_url":"([^"]+)"', d)
        if m:
            mm = YT_RE.search(m.group(1).replace("\\/", "/"))
            if mm and mm.group(1) not in ds_ids:
                ds_ids.append(mm.group(1))
        else:
            for mm in YT_RE.finditer(d):
                if mm.group(1) not in ds_ids:
                    ds_ids.append(mm.group(1))
    if ds_ids:
        return ds_ids[0], ds_ids
    ifr = []
    for f in soup.find_all("iframe"):
        for a in ("src", "data-lazy-src", "data-src"):
            mm = YT_RE.search(f.get(a, "") or "")
            if mm and mm.group(1) not in ifr:
                ifr.append(mm.group(1))
    ifr = [i for i in ifr if i not in PROMO_VIDEO_IDS]
    if ifr:
        return ifr[0], ifr
    return "", []


def extract_packages(soup):
    """QB source-code download packages (generic tool packages filtered out)."""
    out, seen = [], set()
    for a in soup.find_all("a", href=re.compile(r"parallax\.com/package/")):
        href = a["href"]
        slug = re.search(r"/package/([^/]+)/?", href)
        slug = slug.group(1) if slug else ""
        if any(frag in slug for frag in GENERIC_PACKAGE_FRAGMENTS):
            continue
        if href in seen:
            continue
        seen.add(href)
        out.append(href)
    return out


def extract_obex_ids(soup):
    ids = set()
    for a in soup.find_all("a", href=re.compile(r"obex\.parallax\.com")):
        m = re.search(r"OB(\d+)", a["href"]) or re.search(r"/obex/([a-z0-9-]+)", a["href"])
        if m:
            ids.add(m.group(1))
    return sorted(ids)


def extract_reference_links(soup):
    out, seen = [], set()
    content = soup.select_one(".elementor-widget-theme-post-content") or soup
    for a in content.find_all("a", href=True):
        h = a["href"].strip()
        if not h.startswith("http"):
            continue
        if "parallax.com" in h:
            continue
        if any(host in h for host in REF_BLOCK_HOSTS):
            continue
        # Guard against malformed hrefs (e.g. a BOM line accidentally
        # hyperlinked): the host must be a real domain.
        m = re.match(r"https?://([^/]+)", h)
        host = m.group(1) if m else ""
        if "." not in host or "%" in host or " " in host or "," in host:
            continue
        if h in seen:
            continue
        seen.add(h)
        out.append(h)
    return out


def detect_auth_gated(html):
    patterns = [
        r"must be logged in to download",
        r"log ?in to (?:your account to )?download",
        r"login (?:is )?required to download",
        r"please log in to download",
    ]
    low = html.lower()
    return any(re.search(p, low) for p in patterns)


def build(slug, meta, report):
    url = f"https://www.parallax.com/{slug}/"
    html, from_cache = load_html(slug, url)

    soup = BeautifulSoup(html, "html.parser")

    author = jsonld_author(html)
    code_author = extract_code_author(soup)
    page_tags = extract_tags(soup)
    video_id, all_video_ids = extract_youtube(soup)
    packages = extract_packages(soup)
    obex_ids = extract_obex_ids(soup)
    refs = extract_reference_links(soup)
    auth_gated = detect_auth_gated(html)

    has_code = len(packages) > 0
    video_watch = f"https://www.youtube.com/watch?v={video_id}" if video_id else ""

    # report-worthy anomalies
    if len(all_video_ids) > 1:
        report["multi_video"].append((slug, all_video_ids))
    if not video_id:
        report["no_video"].append(slug)
    if len(packages) > 1:
        report["multi_download"].append((slug, len(packages)))
    if auth_gated:
        report["auth_gated"].append(slug)
    report["tags"][slug] = page_tags

    cap = {"domain": meta["domain"], "leaf": meta["leaf"]}
    if meta["secondary"]:
        cap["secondary"] = meta["secondary"]

    doc = {
        "quick_byte": {
            "title": meta["title"],
            "slug": slug,
            "url": url,
            "published_date": meta["date"],
            "author": author,
            "code_author": code_author,
            "capability": cap,
            "type": meta["type"],
            "tags": page_tags,
            "modalities": {
                "article": url,
                "video": video_watch,
                "source_code": {
                    "has_code": has_code,
                    "download_count": len(packages),
                    "download_mechanism": "parallax-download-manager" if has_code else "",
                    "auth_gated": auth_gated,
                    "get_from": url,
                },
                "reference_links": refs,
            },
            "cross_links": {
                "obex_object_ids": obex_ids,
                "related_boards": meta["boards"],
            },
            "metadata": {
                "source": "parallax-quick-bytes",
                "scraped": SCRAPED_DATE,
            },
        }
    }
    return doc, {
        "author": author, "code_author": code_author, "has_code": has_code,
        "dl": len(packages), "video": bool(video_id), "auth": auth_gated,
        "all_videos": all_video_ids, "from_cache": from_cache,
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "multi_video": [], "no_video": [], "multi_download": [],
        "auth_gated": [], "failures": [], "tags": {},
    }
    written = 0
    rows = []
    for slug, meta in QB_DATA.items():
        try:
            doc, summ = build(slug, meta, report)
        except Exception as e:  # noqa
            print(f"FAIL {slug}: {e}", file=sys.stderr)
            report["failures"].append((slug, str(e)))
            time.sleep(1)
            continue
        out = OUTPUT_DIR / f"{slug}.yaml"
        with open(out, "w", encoding="utf-8") as fh:
            yaml.safe_dump(doc, fh, default_flow_style=False, sort_keys=False,
                           allow_unicode=True, width=100)
        written += 1
        rows.append((slug, meta["domain"], meta["leaf"], meta["type"],
                     summ["has_code"], summ["dl"], summ["auth"], summ["video"],
                     summ["author"], summ["code_author"]))
        print(f"OK  {slug}  author={summ['author']!r} code_author={summ['code_author']!r} "
              f"has_code={summ['has_code']} dl={summ['dl']} video={summ['video']}")
        if not summ["from_cache"]:
            time.sleep(1)  # polite delay only on real network fetches

    print("\n==== REPORT ====")
    print(f"written: {written}/{len(QB_DATA)}")
    print(f"failures: {report['failures']}")
    print(f"no_video: {report['no_video']}")
    print(f"multi_video: {report['multi_video']}")
    print(f"multi_download: {report['multi_download']}")
    print(f"auth_gated: {report['auth_gated']}")

    # cross-check page tags vs manifest tags handled by caller; dump tags
    import csv
    tblpath = RAW_HTML_DIR.parent / "qb-catalog-rows.csv"
    with open(tblpath, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["slug", "domain", "leaf", "type", "has_code", "dl",
                    "auth", "video", "author", "code_author"])
        w.writerows(rows)
    # dump tags json for manifest cross-check
    (RAW_HTML_DIR.parent / "qb-page-tags.json").write_text(json.dumps(report["tags"], indent=2))
    print(f"\nrows -> {tblpath}")


if __name__ == "__main__":
    main()
