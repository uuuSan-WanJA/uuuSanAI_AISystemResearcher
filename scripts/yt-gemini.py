#!/usr/bin/env python3
"""
yt-gemini.py — YouTube 영상을 Gemini REST API에 file_data.file_uri 로 넘겨 분석한다.

Gemini CLI(`gemini -p "... <URL>"`) 는 URL을 프롬프트 텍스트로만 취급해서
영상을 실제로 처리하지 못한다. 반드시 이 스크립트(또는 동등한 REST 호출) 사용.

Usage:
    python scripts/yt-gemini.py <youtube_url> [prompt]

Env:
    GEMINI_API_KEY  (필수) — 없으면 ~/.gemini/.env 에서 자동 로드
    GEMINI_MODEL    (선택) — 기본 gemini-2.5-pro (짧은 영상·빠른 확인엔 gemini-2.5-flash)
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_PROMPT = (
    "이 영상의 핵심 주장과 근거, 타임스탬프(HH:MM:SS 형식), "
    "언급된 고유명사(툴/논문/인물/회사/제품/수치)를 한국어로 정리. "
    "편향 없이 원본 전달에 집중, 영상에 없는 내용 추측 금지.\n\n"
    "구조:\n"
    "(1) 한 줄 요약\n"
    "(2) 핵심 주장 3-7개 + 근거 + 타임스탬프\n"
    "(3) 언급된 고유명사 리스트\n"
    "(4) 핵심 인용 2-3개 (타임스탬프 포함)"
)


def load_api_key() -> str | None:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    env_file = Path.home() / ".gemini" / ".env"
    if not env_file.exists():
        return None
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        if k.strip() == "GEMINI_API_KEY":
            return v.strip().strip('"').strip("'")
    return None


def main() -> int:
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <youtube_url> [prompt]", file=sys.stderr)
        return 1

    url = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PROMPT
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro")

    api_key = load_api_key()
    if not api_key:
        print("error: GEMINI_API_KEY not set (checked env and ~/.gemini/.env)", file=sys.stderr)
        return 2

    body = {
        "contents": [{
            "parts": [
                {"file_data": {"file_uri": url}},
                {"text": prompt},
            ]
        }]
    }

    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{model}:generateContent?key={api_key}"
    )
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        print(e.read().decode("utf-8", errors="replace"), file=sys.stderr)
        return 3
    except urllib.error.URLError as e:
        print(f"network error: {e.reason}", file=sys.stderr)
        return 3

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        print("error: unexpected response shape", file=sys.stderr)
        print(json.dumps(data, ensure_ascii=False, indent=2), file=sys.stderr)
        return 4

    sys.stdout.reconfigure(encoding="utf-8")
    print(text)

    usage = data.get("usageMetadata", {})
    if usage:
        total = usage.get("totalTokenCount", "?")
        model_used = data.get("modelVersion", model)
        print(f"\n---\n[tokens: {total} | model: {model_used}]", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
