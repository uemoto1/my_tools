# OverleafからarXivへのアップロード手順

## arXivのアカウント作成（初回のみ）

論文を投稿するにはアカウントが必要です。初めてarXivを利用する場合は、以下の手順でアカウントを作成してください。

1. [arXivのウェブサイト](https://arxiv.org) を開く
1. ページ右上の **`login`** リンクをクリック
1. ページ下部の **`If you've never logged ...`** にある **`Register ...`** ボタンをクリック
1. フォームに入力
   - `Email:` 大学のメールアドレス（stu.kobe-u.ac.jpのもの）
   - `Username:` と `Password:` は覚えやすいものを設定
1. `next` ボタンで次へ進む
1. `I certify ...` にチェックを入れ、`submit` ボタンをクリック
1. 登録確認メールが届くので、受信を確認


## Overleafからソースファイルを取得

1. [Overleaf](https://ja.overleaf.com/) のプロジェクトページを開く
1. ページ右上の **`メニュー`** ボタンをクリック
1. **`ソース`** を選んでLaTeXソースをダウンロード
1. ダウンロードしたzipファイルを展開
   - Mac: ダブルクリックで自動展開
   - Windows: 右クリック → `すべて展開`


## 投稿用ファイルの準備

### 公開時の注意点

- arXivにはLaTeXソース一式をまとめた圧縮ファイルをアップロードします。arXiv側でコンパイルされ、PDFが公開されます。
- 必要なファイル：
  - 本文 `ms.tex`
  - 補足資料（任意） `supplement.tex`
  - 図や表などの画像ファイル
  - その他必要なスタイルファイル等
- **重要:** arXivではコンパイル済みPDFだけでなく、LaTeXソース一式も公開されます。
  → コメントや不要ファイル（未使用のグラフなど）、加工中の下書きなども閲覧可能になるので、必ず削除してください。


### 加工手順

1. 本文のLaTeXファイルを `ms.tex` にリネーム
1. 補足資料がある場合は `supplement.tex` にリネームして同封
1. 不要なファイルを削除
   - 使っていないソースや画像ファイル
   - 下書き、メモ、議論資料
   - 中間データ
   - 雑誌テンプレート
   - Macの場合の `.DS_Store` (Finder の隠しファイル)
   - **外部に公開したくないデータが残っていないか要確認**
1. ソース中のコメント（`%`以降）は削除

### ソースのコンパイル確認

arXivでのコンパイルには`pdflatex`(および`bibtex`)を使うため, 同じ環境で動作するか事前確認の必要

```bash
pdflatex ms.tex
bibtex ms.tex   # 使っているなら
pdflatex ms.tex
pdflatex ms.tex   # 参照エラー防止のため 2 回実行
```

* `ms.pdf` が生成され、エラーが出なければ OK
* 付属資料がある場合は同様に `supplement.tex` をコンパイル


### 生成ファイルの整理

| ファイル | 詳細 | 処理 |
|---|---|---|
| `ms.pdf` | コンパイル済みPDF | 削除(**コピーを手元に保管**) |
| `*.log`, `*.aux`, `*.out` | コンパイル時に作成される一時ファイル | 削除 |
| `*.bbl` | BibTeX の出力 | **残す**（arXiv で再コンパイルする際に必要） |
| `*-eps-converted-to.pdf` | EPS を PDF に変換したファイル | 旧システムで必要なら残す |

### **チェックリスト**
-  コンパイル済みPDFのコピーを閲覧し、図・表・数式・文献番号にエラーがないか確認
-  ファイル名に「draft」「temp」「tmp」などのキーワードが入っていないか確認
-  **残すべきファイル**：`ms.tex`・`supplement.tex`・`.bbl`（BibTeX で生成した場合）と画像ファイル一式が残っているか確認

### ZIP ファイルを作る

1. 上記で残したファイルだけをまとめる
2. フォルダ全体を右クリック → 「圧縮」
3. ZIP ファイル名は「arxiv_submission.zip」など分かりやすく


## arXiv へのアップロード

1.  arXiv トップページ（[https://arxiv.org](https://arxiv.org)）にアクセス
2.  右上の **login** でログイン
3.  **Start Submission** をクリック
4.  **Verify Your Contact Information** で情報を確認、必要に応じて **Change User Information**
    - 未入力か変更がある場合は`Change User Information`を選択
        - `First Name`,`Last Name` は最低限必要
        - `Affiliation`は神戸大工学部電気電子の大学院生の場合 \
        `Department of Electrical and Electronic Engineering, Graduate School of Engineering, Kobe University`
5.  **I certify** のチェックボックスにチェック
6.  **Submission Agreement** の **By submitting** をチェック、下までスクロールして **Accept**
7.  **Authorship** で `I am submitting as an author of this article` を選択
8.  **License Statement** で（特に理由がなければ）`arXiv.org perpetual, non‑exclusive license` を選択
    - 研究テーマや共同研究先によっては別の選択肢が必要になる可能性あり
9.  **Archive and Subject Class** で分野を選択（以下はテーマごとの例）
    - プログラム開発系: `Physics > Computational Physics`
    - 材料・デバイス応用:
        - `Condensed Matter > Mesoscale & Nanoscale Physics`
        - `Condensed Matter > Material Physics`
        - `Physics > Applied Physics`
    - 量子情報: `Quantum Physics`
10.  **Prepare Files** で ZIP ファイルをアップロード
    - エラーが出たらファイルを修正し、**Delete All** で再アップロード
11.  **Check Files** ボタンでファイルを確認
12.  問題がなければ **Accept and Continue**
13.  **Preview your PDF** で自動コンパイル結果を確認
    - PDF が正しく表示されるかチェック（ **手元のコンパイル済みpdfファイルと比較しし式や図表番号、文献番号、フォーマットに問題がないかよく確認する** ）
14.  メタデータ入力
    - Title, Author(s), Abstract は論文原稿の表記を正確に
    - Comments にページ数・図数などを記入
15.  **Check your submission** で最終確認、文字の大文字・小文字**
    - 記号・上付き・下付き
    - 章・節の見出し
    - PDF をダウンロードして最終確認
16.  **Submit** をクリック
17.  登録メールに送信完了通知が届く、公開まで 1〜2 日（休日は除く）

### **重要**
- PDF のレイアウトや内容に問題があると、再提出を求められることがあります。
- 途中で **「投稿内容の差し替えは X 日まで可能」** と表示される場合があります。期限を確認しておきましょう。


