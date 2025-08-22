# OverleafからarXivへのアップロード手順について

## arXivの新規アカウントを作成

投稿のためにはまずアカウントが必要, はじめてarXivに投稿する場合は下記の手順でアカウント作成から開始.

1. arXivのウェブサイトを開く \
https://arxiv.org

1. ページ右上の`login`リンクをクリック

1. ページ下側の`If you've never logged 略`にある`Register 略`ボタンをクリック

1. フォームに記入する
    - `Email:` 大学のメールアドレス (stu.kobe-u.ac.jpのほう)
    - `Username:` , `Password:`  覚えやすいものをつけておく

1. `next`ボタンで次のページに移動

1. `I certify 略`にチェックを入れ, `submit`ボタンをクリック

1. メールが届くので受信できるか確認

## Overleafからソースファイルを入手

1. [Overleaf](https://ja.overleaf.com/) にあるプロジェクトページを開く

1. ページ右上の`メニュー`ボタンをクリック

1. `ソース`ボタンをクリックしてLaTeXソースをダウンロード

1. ダウンロード済みのzipファイルを開く
    - Macの場合はダブルクリックで自動で展開
    - Windowsの場合は右クリックのメニューから`すべて展開`で圧縮ファイルを展開

## 投稿用の原稿ファイルの加工

### arXiv公開の注意点

- arXivにLaTeXソース一式をまとめた圧縮ファイル(zipなど)を投稿するとコンパイルされてpdfをWeb公開

- ソースコード`ms.tex`（本文）と`supplement.tex`（付属資料・任意）、画像ファイル、その他の必須ファイルを含める

- arXivでのコンパイルにはpdflatex(およびbibtex)を使うため, 同じ環境で動作するか事前確認の必要

- **arXivではコンパイル済みPDFだけでなくLaTeXのソースファイル一式がWebで公開される**ので、ソースコード中のコメント、編集中の画像ファイルも丸見えになる (**不要なデータは手作業で削除する！**)

### 加工手順

1. 本文のLaTeXソースファイルは`ms.tex`というファイル名に変更

1. (資料を付属する場合は`supplement.tex`というファイル名に変更して同封)

1. 不要なファイルの削除
    - 使っていないソースファイル
    - 使っていない画像ファイル
    - 下書きやメモ、議論用の資料
    - 途中計算データ
    - 雑誌テンプレート
    - (Macの場合は`.DS_Store`というFinderの隠しファイル)
    - **ほか流出するとまずいものが残っていないかよく確認！**

1. ソースコード中のコメント(`%`で始まるものを行末まで削除)

1. `pdflatex`で`ms.tex`のコンパイルを試す
    - `$ pdflatex ms.tex`
    - `$ bibtex ms.tex` \
    (もしbibtexを使っている場合は必要)
    - `$ pdflatex ms.tex`\
     (参照エラーを防ぐため１〜２回実行)
    - 資料が付属する場合は`supplement.tex`についても同様にテスト
    - 出来上がったpdfファイルをチェックしてエラーが無いことを確認
        - 図・表・数式番号などの参照エラー、文献番号が一致しないエラーなどが多い

1. 先程のコンパイル時に生成されたファイルから不要なものを削除, **拡張子`.bbl`ファイルは残すこと**(arXivでのコンパイルに必要)
    - `ms.pdf`（および`supplement.pdf`）コンパイル後のpdfファイル
    - `略.log`, `略.aux`, `略.out`, `略Nodes.bib` 一時ファイルなので削除
    - `略-eps-converted-to.pdf` (epsファイルを画像に使う場合)
        - 旧バージョンの投稿システムでは`-eps-converted-to.pdf`を使うため残しておく必要あり

1. 上記のファイルが入ったフォルダを圧縮

## arXivへのアップロード

1. [arXiv](https://arxiv.org/)のウェブサイトにアクセス

1. 右上の`login`リンクをクリック、アカウントとパスワードを入力しログイン

1. `Start Submission`ボタンをクリック

1. `Verify Your Contact Information`で自分の所属情報を確認
    - 未入力か変更がある場合は`Change User Information`を選択
        - `First Name`,`Last Name` は最低限必要
        - `Affiliation`
            - 神戸大小野研の大学院生の場合は`Department of Electrical and Electronic Engineering, Graduate School of Engineering, Kobe University`
    - 問題ない場合は`I certify 略`をチェック

1. `Submission Agreement`にある`By submitting 略`をチェック
    - 注意書きが表示されるので一番下までスクロールで読み`Accept and return to Submission`ボタンをクリック

1. `Authorship`で著者種別を選択
    - 通常は`I am submitting as an author of this article`（投稿者自身が論文の著者）を選択

1. `License Statement`で著作権ライセンスを選択
    - 特にこだわり(or 縛り)がなければ`arXiv.org perpetual, non-exclusive license`
    - 共同研究だと相手方やプロジェクト次第で選択できないものがあるかも（要確認）

1. `Archive and Subject Class`で分野を選択する（小野研の関連研究であれば下記のものが候補？）
    - プログラム開発関係
        - `Physics` > `Computational Physics` 
    - デバイス材料応用関係：
        - `Condensed Matter` > `Mesoscale & Nanoscale Physics` 
        - `Condensed Matter` > `Material Physics` 
        - `Physics` > `Applied Physics`
    - 量子情報処理関係
        - `Quantum Physics`

1. `Prepare Files`から先程作成した圧縮ファイルを選択し`upload`ボタンをクリック
    - エラーが発生した場合は原稿ファイルを適宜修正する, `Delete All`でアップロード済みファイルを消去した上で再度アップロード

1. `Check Files`ボタンを押してファイルをチェックする

1. 問題がなければ`Accept and Continue`ボタンをクリック

1. 正常にコンパイルができれば`Submission Processing`の`Preview your PDF`ボタンでファイルをチェックできる
    - **内容に問題がないか確認すること！**

1. メタデータの入力
    - `Title`, `Author(s)`, `Abstract`は論文原稿の表記を正確にコピー
    - `Comments`はページ数や画像ファイル数を記入
        * 例: `10 pages, 5 figures`
    - 他の欄は記入不要

1. `Check your submission`で投稿前の最終確認
    - `Preview Abstract`タイトル、著者リスト、アブストラクトに間違いはないか
        - 大文字・小文字などは論文本文とまったく同じか？
        - 記号、上付き・下付きの添字、数式に誤りはないか？
        - おかしなところで段落が変わっていないか？
    - `Preview Document`でPDFファイルをダウンロードして内容をチェック
        - （ダウンロードしたファイルは手元に残しておくこと）

1. `Submit`ボタンをクリック

1. メールが届くので確認
    - arXiv側で内容の簡易チェックが行われ, 通常は投稿から公開まで１〜２日程度必要（休日は除く）
    - **公開予定日時と原稿差し替えのタイムリミットを要確認！**
