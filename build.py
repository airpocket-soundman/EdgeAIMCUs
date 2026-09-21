"""原稿 (src/chapters/*.html) にヘッダー・目次・ページ送りを付けて docs/ に書き出す。

使い方:  python build.py
docs/ は GitHub Pages の公開フォルダ。手で編集せず、src/ を直してからビルドする。
"""
import html
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"

BOOK_TITLE = "エッジAIマイコンのすすめ"

# (出力ファイル名, 部, 章番号ラベル, タイトル, 下書きか)
TOC = [
    ("index.html", None, "", "はじめに", False),
    ("ch01-edge-ai.html", "第1部 基礎編", "1章", "エッジAIってなに？", False),
    ("ch02-mcu.html", "第1部 基礎編", "2章", "マイコン（MCU）ってなに？", False),
    ("ch03-ai-on-mcu.html", "第1部 基礎編", "3章", "マイコンでAIを動かすしくみ", False),
    ("ch04-ai-mcus.html", "第1部 基礎編", "4章", "エッジAIを動かせるマイコンたち", False),
    ("ch05-esp32s3.html", "第2部 ボード＆実例編", "5章", "ESP32-S3（M5Stack AtomS3 / CoreS3 ほか）", False),
    ("ch06-esp32p4.html", "第2部 ボード＆実例編", "6章", "ESP32-P4（M5Stack Tab5）", False),
    ("ch07-mcxn947.html", "第2部 ボード＆実例編", "7章", "NXP MCX N947（FRDM-MCXN947）", False),
    ("ch08-solist-ai.html", "第2部 ボード＆実例編", "8章", "ROHM Solist-AI（ML63Q2557）", False),
    ("ch09-spresense.html", "第2部 ボード＆実例編", "9章", "Sony Spresense（CXD5602）", False),
    ("ch10-uno-q.html", "第2部 ボード＆実例編", "10章", "Arduino UNO Q（STM32U585 ＋ QRB2210）", False),
    ("ch11-microbit.html", "第2部 ボード＆実例編", "11章", "micro:bit（nRF52833）", False),
    ("ch12-rp2040.html", "第2部 ボード＆実例編", "12章", "RP2040 / RP2350（Raspberry Pi Pico）", False),
    ("ch13-others.html", "第2部 ボード＆実例編", "13章", "まだまだいる！ほかのマイコンたち", False),
    ("appendix-candidates.html", "付録", "付録A", "作者のリポジトリに登場したマイコン一覧", False),
]

HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="マイコンで小さなAIを動かして遊ぶための入門書『{book}』">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22><rect width=%2232%22 height=%2232%22 rx=%228%22 fill=%22%23ff7a2f%22/><text x=%2216%22 y=%2222%22 font-size=%2216%22 text-anchor=%22middle%22 fill=%22white%22 font-family=%22sans-serif%22 font-weight=%22bold%22>AI</text></svg>">
<script>
try {{ const t = localStorage.getItem("theme"); if (t) document.documentElement.dataset.theme = t; }} catch (e) {{}}
</script>
</head>
<body>
<header class="site-header">
  <a class="brand" href="index.html"><span class="brand-chip">AI</span>{book}</a>
  <span class="spacer"></span>
  <button class="toc-toggle" type="button" onclick="document.body.classList.toggle('show-toc')">目次</button>
  <button type="button" onclick="toggleTheme()" aria-label="明るさの切り替え">◐</button>
</header>
<div class="layout">
<nav class="sidebar" aria-label="目次">
{sidebar}
</nav>
<main>
"""

FOOT = """
{pager}
</main>
</div>
<footer class="site-footer">{book} ／ airpocket-soundman ／ 執筆中の原稿です。内容は予告なく変わります。</footer>
<script>
function toggleTheme() {{
  const root = document.documentElement;
  const dark = root.dataset.theme ? root.dataset.theme === "dark"
    : matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = dark ? "light" : "dark";
  try {{ localStorage.setItem("theme", root.dataset.theme); }} catch (e) {{}}
}}
</script>
</body>
</html>
"""


def sidebar(current: str) -> str:
    out, part = [], "__start__"
    for fname, p, num, title, draft in TOC:
        if p != part:
            if part != "__start__":
                out.append("</ol>")
            if p:
                out.append(f"<h2>{html.escape(p)}</h2>")
            out.append("<ol>")
            part = p
        cls = ' class="current"' if fname == current else ""
        n = f'<span class="num">{num}</span>' if num else ""
        d = ' <span class="draft">（下書き）</span>' if draft else ""
        out.append(f'<li><a href="{fname}"{cls}>{n}{html.escape(title)}{d}</a></li>')
    out.append("</ol>")
    return "\n".join(out)


def pager(i: int) -> str:
    links = []
    if i > 0:
        f, _, n, t, _ = TOC[i - 1]
        links.append(f'<a class="prev" href="{f}"><small>← まえへ</small>{n} {html.escape(t)}</a>')
    else:
        links.append("<span style='flex:1'></span>")
    if i < len(TOC) - 1:
        f, _, n, t, _ = TOC[i + 1]
        links.append(f'<a class="next" href="{f}"><small>つぎへ →</small>{n} {html.escape(t)}</a>')
    return '<nav class="pager">' + "".join(links) + "</nav>"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    shutil.copy(SRC / "style.css", OUT / "style.css")
    (OUT / ".nojekyll").write_text("")
    for i, (fname, _, num, title, _) in enumerate(TOC):
        src = SRC / "chapters" / fname
        body = src.read_text(encoding="utf-8")
        page_title = BOOK_TITLE if fname == "index.html" else f"{num} {title}｜{BOOK_TITLE}"
        page = (
            HEAD.format(title=html.escape(page_title), book=BOOK_TITLE, sidebar=sidebar(fname))
            + body
            + FOOT.format(pager=pager(i), book=BOOK_TITLE)
        )
        (OUT / fname).write_text(page, encoding="utf-8")
        print("wrote", fname)


if __name__ == "__main__":
    main()
