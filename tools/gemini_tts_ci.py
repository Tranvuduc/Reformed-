#!/usr/bin/env python3
"""Gemini TTS helper for CI (GitHub Actions).

Same request/response handling as the connector helper
(workspace/custom-connectors/custom.gemini/bin/gemini_tts.py), except the
API key comes from the GEMINI_API_KEY environment variable (a GitHub
repository secret on the runner) instead of the local credential vault.
The key is sent as the x-goog-api-key header and is NEVER printed or
written to any log or file.

Usage:
    GEMINI_API_KEY=... python3 tools/gemini_tts_ci.py \
        --model gemini-3.8-flash-tts --text-file text.txt \
        --voice Kore --out out.wav [--max-attempts 5]

POSTs generateContent with responseModalities ["AUDIO"] and a prebuilt
voice. The API returns base64 PCM (24 kHz, 16-bit mono) or a WAV file;
this script writes a .wav file and prints duration / sample rate /
levels to stdout.
"""

import argparse
import base64
import json
import os
import struct
import sys
import time
import urllib.error
import urllib.request
import wave

HOST = "generativelanguage.googleapis.com"
BASE = f"https://{HOST}/v1beta"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


def _request(url, api_key, data=None):
    request = urllib.request.Request(url, data=data)
    request.add_header("x-goog-api-key", api_key)
    if data is not None:
        request.add_header("Content-Type", "application/json")
    opener = urllib.request.build_opener(NoRedirect())
    return opener.open(request, timeout=180)


def cmd_tts(model, text_file, voice, out_path, max_attempts, api_key):
    with open(text_file, encoding="utf-8") as handle:
        text = handle.read().strip()
    body = json.dumps(
        {
            "contents": [{"parts": [{"text": text}]}],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {"voiceName": voice}
                    }
                },
            },
        }
    ).encode("utf-8")
    url = f"{BASE}/models/{model}:generateContent"
    waits = [60, 120, 180, 240, 300]
    start = time.time()
    last_error = None
    payload = None
    for attempt in range(1, max_attempts + 1):
        try:
            with _request(url, api_key, data=body) as response:
                payload = json.loads(response.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            print(f"attempt={attempt} status=HTTP {exc.code}: {raw[:500]}", file=sys.stderr)
            last_error = (exc.code, raw)
            if exc.code in (429, 503) and attempt < max_attempts:
                wait = waits[min(attempt - 1, len(waits) - 1)]
                print(f"retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            return 1
        except Exception as exc:
            print(f"attempt={attempt} error: {exc}", file=sys.stderr)
            return 1
    else:
        print(f"FAILED after {max_attempts} attempts: {last_error}", file=sys.stderr)
        return 1

    elapsed = time.time() - start
    audio_b64 = None
    mime = None
    for cand in payload.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                audio_b64 = inline["data"]
                mime = inline.get("mimeType", "")
                break
    if not audio_b64:
        print("FAILED: no inline audio data in response:", json.dumps(payload)[:800], file=sys.stderr)
        return 1
    pcm = base64.b64decode(audio_b64)
    rate = 24000
    if pcm[:4] == b"RIFF":
        with open(out_path, "wb") as handle:
            handle.write(pcm)
        with wave.open(out_path, "rb") as wav:
            n = wav.getnframes()
            rate = wav.getframerate()
            duration = n / rate
            frames = wav.readframes(n)
        peak = 0
        if n:
            samples = struct.unpack(f"<{n}h", frames)
            peak = max(abs(s) for s in samples) / 32768.0
        usage = payload.get("usageMetadata", {})
        print(f"attempt={attempt} status=ok model={model} voice={voice}")
        print(f"mime={mime} (container wav, written as-is)")
        print(f"render_seconds={elapsed:.1f}")
        print(f"audio_seconds={duration:.2f} sample_rate={rate} channels=1 peak={peak:.3f}")
        print(f"prompt_tokens={usage.get('promptTokenCount')} total_tokens={usage.get('totalTokenCount')}")
        print(f"out={out_path}")
        return 0
    with wave.open(out_path, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(pcm)
    n = len(pcm) // 2
    duration = n / rate
    peak = 0
    if n:
        samples = struct.unpack(f"<{n}h", pcm)
        peak = max(abs(s) for s in samples) / 32768.0
    usage = payload.get("usageMetadata", {})
    print(f"attempt={attempt} status=ok model={model} voice={voice}")
    print(f"mime={mime}")
    print(f"render_seconds={elapsed:.1f}")
    print(f"audio_seconds={duration:.2f} sample_rate={rate} channels=1 peak={peak:.3f}")
    print(f"prompt_tokens={usage.get('promptTokenCount')} total_tokens={usage.get('totalTokenCount')}")
    print(f"out={out_path}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Gemini TTS helper (CI, key from env)")
    parser.add_argument("--model", required=True)
    parser.add_argument("--text-file", required=True)
    parser.add_argument("--voice", default="Kore")
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-attempts", type=int, default=5)
    args = parser.parse_args()
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("FAILED: GEMINI_API_KEY is not set (add it as a repository secret)", file=sys.stderr)
        return 1
    return cmd_tts(args.model, args.text_file, args.voice, args.out, args.max_attempts, api_key)


if __name__ == "__main__":
    sys.exit(main())
