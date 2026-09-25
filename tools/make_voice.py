#!/usr/bin/env python3
"""Record every phrase in voice/phrases.txt with a neural Hebrew voice and pack
the clips into voice/voice.js, which the game plays instead of the device's
built-in text-to-speech.

Microsoft neural voices (free, no account):
    pip install edge-tts
    python tools/make_voice.py                             # Hila (female)
    python tools/make_voice.py --voice he-IL-AvriNeural    # Avri (male)

Google Cloud Text-to-Speech (needs an API key in GOOGLE_TTS_API_KEY):
    python tools/make_voice.py --provider google --list-voices
    python tools/make_voice.py --provider google --voice he-IL-Chirp3-HD-Aoede --rate 0.9

Clips are cached in voice/clips/, so re-running only records phrases that are
new or changed. --strip-nikud sends the text without vowel marks, which some
voices pronounce better.
"""
import argparse
import asyncio
import base64
import hashlib
import json
import os
import pathlib
import re
import ssl
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHRASES = ROOT / "voice" / "phrases.txt"
CLIPS = ROOT / "voice" / "clips"
OUT = ROOT / "voice" / "voice.js"


def read_phrases():
    """Return (phrase, spoken) pairs. A line 'phrase | spoken' records the
    right-hand spelling under the left-hand key, to fix a pronunciation."""
    pairs = []
    for line in PHRASES.read_text(encoding="utf8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, spoken = line.partition("|")
        pairs.append((key.strip(), (spoken or key).strip()))
    return pairs


GOOGLE_API = "https://texttospeech.googleapis.com/v1"


def google_request(path, body=None):
    key = os.environ.get("GOOGLE_TTS_API_KEY")
    if not key:
        sys.exit("GOOGLE_TTS_API_KEY is not set")
    ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE"))
    req = urllib.request.Request(
        f"{GOOGLE_API}/{path}",
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Content-Type": "application/json", "X-Goog-Api-Key": key},
    )
    with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
        return json.load(r)


def google_list_voices():
    for v in google_request("voices?languageCode=he-IL").get("voices", []):
        print(f"{v['name']:32} {v['ssmlGender']}")


def google_synth(text, voice, rate):
    body = {
        "input": {"text": text},
        "voice": {"languageCode": "he-IL", "name": voice},
        "audioConfig": {"audioEncoding": "MP3", "speakingRate": float(rate)},
    }
    return base64.b64decode(google_request("text:synthesize", body)["audioContent"])


async def record_google(pairs, voice, rate, jobs):
    CLIPS.mkdir(parents=True, exist_ok=True)
    sem = asyncio.Semaphore(jobs)
    done = 0

    async def one(key, spoken):
        nonlocal done
        name = hashlib.sha1(f"google|{voice}|{rate}|{spoken}".encode()).hexdigest()[:16] + ".mp3"
        path = CLIPS / name
        if not path.exists() or path.stat().st_size == 0:
            async with sem:
                for attempt in range(4):
                    try:
                        path.write_bytes(await asyncio.to_thread(google_synth, spoken, voice, rate))
                        break
                    except Exception as e:
                        if attempt == 3:
                            raise RuntimeError(f"could not record {key!r}: {e}") from e
                        await asyncio.sleep(2 ** attempt)
        done += 1
        print(f"\r{done}/{len(pairs)}", end="", flush=True)
        return key, path

    results = await asyncio.gather(*(one(k, s) for k, s in pairs))
    print()
    return results


async def record(pairs, voice, rate, jobs):
    # Work behind corporate / sandbox proxies that use their own CA bundle.
    ca = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if ca:
        import certifi
        certifi.where = lambda: ca
    import edge_tts

    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    CLIPS.mkdir(parents=True, exist_ok=True)
    sem = asyncio.Semaphore(jobs)
    done = 0

    async def one(key, spoken):
        nonlocal done
        name = hashlib.sha1(f"{voice}|{rate}|{spoken}".encode()).hexdigest()[:16] + ".mp3"
        path = CLIPS / name
        if not path.exists() or path.stat().st_size == 0:
            async with sem:
                for attempt in range(4):
                    try:
                        await edge_tts.Communicate(spoken, voice, rate=rate, proxy=proxy).save(str(path))
                        break
                    except Exception as e:  # network hiccup: retry with backoff
                        if attempt == 3:
                            raise RuntimeError(f"could not record {key!r}: {e}") from e
                        await asyncio.sleep(2 ** attempt)
        done += 1
        print(f"\r{done}/{len(pairs)}", end="", flush=True)
        return key, path

    results = await asyncio.gather(*(one(k, s) for k, s in pairs))
    print()
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--provider", choices=["edge", "google"], default="edge")
    ap.add_argument("--voice", help="edge: he-IL-HilaNeural / he-IL-AvriNeural; google: see --list-voices")
    ap.add_argument("--rate", help="speed. edge: e.g. -10%% (default); google: e.g. 0.9 (default)")
    ap.add_argument("--strip-nikud", action="store_true", help="send the text without vowel marks")
    ap.add_argument("--list-voices", action="store_true", help="google: list the Hebrew voices and exit")
    ap.add_argument("--jobs", type=int, default=6, help="phrases recorded at the same time")
    args = ap.parse_args()

    if args.list_voices:
        return google_list_voices()
    google = args.provider == "google"
    args.voice = args.voice or ("he-IL-Chirp3-HD-Aoede" if google else "he-IL-HilaNeural")
    args.rate = args.rate or ("0.9" if google else "-10%")

    pairs = read_phrases()
    if args.strip_nikud:  # keep the lookup key, change only what is spoken
        pairs = [(k, re.sub(r"[\u0591-\u05C7]", "", s)) for k, s in pairs]
    rec = record_google if google else record
    results = asyncio.run(rec(pairs, args.voice, args.rate, args.jobs))
    clips = {key: base64.b64encode(path.read_bytes()).decode() for key, path in results}
    OUT.write_text(
        f"// Generated by tools/make_voice.py ({args.provider} {args.voice}, rate {args.rate}"
        f"{', no nikud' if args.strip_nikud else ''}). Do not edit by hand.\n"
        "window.VOICE_CLIPS = " + json.dumps(clips, ensure_ascii=False, indent=0) + ";\n",
        encoding="utf8",
    )
    print(f"wrote {OUT.relative_to(ROOT)}: {len(clips)} clips, {OUT.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    sys.exit(main())
