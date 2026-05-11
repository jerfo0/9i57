#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Maverick 博客的 src/*.md 读取 front matter，生成微信小程序用的全量清单。
用法（在博客仓库「根目录」，且已安装 PyYAML）：
  pip install pyyaml
  python tools/gen_mp_articles_manifest.py

环境变量（可选）：
  MP_MANIFEST_SRC   默认 src
  MP_MANIFEST_OUT   默认 dist/mp-articles-manifest.json
  MP_SITE_ORIGIN    默认 https://recall.9i57.com
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit("请先安装: pip install pyyaml")

FM_RE = re.compile(r"^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n", re.MULTILINE)


def _norm_date(val) -> str:
    if val is None:
        return ""
    if hasattr(val, "strftime"):
        return val.strftime("%Y-%m-%d")
    s = str(val).strip()
    return s[:10] if len(s) >= 10 else s


def _summary(fm: dict) -> str:
    ex = fm.get("excerpt")
    if ex is None:
        return ""
    s = str(ex).strip().replace("\n", " ")
    return s[:500] if len(s) > 500 else s


def collect_posts(src: Path, site: str) -> list[dict]:
    site = site.rstrip("/")
    posts: list[dict] = []
    for path in sorted(src.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        m = FM_RE.match(text)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(fm, dict):
            continue
        if fm.get("layout") != "post":
            continue
        st = str(fm.get("status") or "publish").lower()
        if st in ("draft", "hidden", "private"):
            continue
        title = (fm.get("title") or "").strip()
        if not title:
            continue
        slug = (fm.get("slug") or "").strip()
        if not slug:
            slug = path.stem
        date = _norm_date(fm.get("date"))
        if not date:
            continue
        link = f"{site}/archives/{slug}/"
        posts.append(
            {
                "title": title,
                "link": link,
                "date": date,
                "summary": _summary(fm),
            }
        )
    posts.sort(key=lambda x: (x["date"], x["title"]), reverse=True)
    return posts


def main() -> None:
    root = Path(os.environ.get("MP_MANIFEST_ROOT", ".")).resolve()
    src = Path(os.environ.get("MP_MANIFEST_SRC", "src"))
    if not src.is_absolute():
        src = root / src
    out = Path(os.environ.get("MP_MANIFEST_OUT", "dist/mp-articles-manifest.json"))
    if not out.is_absolute():
        out = root / out
    site = os.environ.get("MP_SITE_ORIGIN", "https://recall.9i57.com")

    if not src.is_dir():
        raise SystemExit(f"找不到文章目录: {src}")

    posts = collect_posts(src, site)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(posts, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"已写入 {len(posts)} 条 → {out}")


if __name__ == "__main__":
    main()
