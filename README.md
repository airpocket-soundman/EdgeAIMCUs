# エッジAIマイコンのすすめ

マイコンで小さなAIを動かして、ライトに楽しむための入門書の原稿です。

- 公開ページ: https://airpocket-soundman.github.io/EdgeAIMCUs/

## 構成

```
EdgeAIMCUs/
├─ build.py          原稿にヘッダー・目次・ページ送りを付けて docs/ に書き出す
├─ src/
│  ├─ style.css      全ページ共通のスタイル
│  └─ chapters/      章ごとの原稿（HTML の本文だけ）
└─ docs/             GitHub Pages の公開フォルダ（build.py が生成。手で編集しない）
```

## 原稿を直すとき

1. `src/chapters/` の該当ファイルを編集する（章を足すときは `build.py` の `TOC` にも追加）
2. `python build.py` で `docs/` を作り直す
3. `src/` と `docs/` をまとめてコミットする

原稿の中の「執筆メモ」の枠は、実験や計測をして埋める予定の場所です。
