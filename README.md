<div align="center">プロジェクト名/ロゴ募集中~~</div>

<hr>

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/poi-ai/keibaAI)
![Lines of code](https://img.shields.io/tokei/lines/github/poi-ai/keibaAI)
![Elapsed date](https://img.shields.io/date/1673284347?label=first%20commit)
![GitHub latest commit](https://img.shields.io/github/last-commit/poi-ai/keibaAI)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/poi-ai/keibaAI)<br>
[![Twitter](https://github.com/poi-ai/img/blob/main/twitter.png)](https://twitter.com/intent/tweet?text=poi-ai/keibaAI&url=https://github.com/poi-ai/keibaAI)
[![はてなブックマーク](https://github.com/poi-ai/img/blob/main/hatebu.png)](https://b.hatena.ne.jp/entry/s/github.com/poi-ai/keibaAI)
[![Facebook](https://github.com/poi-ai/img/blob/main/facebook.png)](https://www.facebook.com/sharer/sharer.php?u=https://github.com/poi-ai/keibaAI)

|項目|
| :--- |
| 1. [概要](#anchor1) |
| 2. [開発環境](#anchor2)|
| 3. [初期設定](#anchor3)|
| 4. [実行](#anchor4)|

<!--
| 5. [](#anchor5)| -->

<a id="anchor1"></a>
## 1. 概要🐴
競馬AIを開発するプロジェクトです。旧リポジトリ→[keibaAI_disable](https://github.com/poi-ai/keibaAI_disable)

本リポジトリでは、データスクレイピングからクレンジング、モデル構築、予測まで一通りのソースコードを管理予定です。

学習データは容量の都合上本リポジトリでは扱わず、Google Driveなどで管理を行なっております。
(ある程度完成に近づいたらprivateに変更予定です。)

~~各PGの説明等、詳細は[Wiki](https://github.com/poi-ai/keibaAI/wiki)に記載予定です。~~

<a id="anchor2"></a>
## 2. 開発環境💻

### バージョン
```
Python >= 3.9.13
pip >= 22.3.1
MySQL >= 8.0.31
```

### 外部ライブラリ

[requirements.txt](requirements.txt)に記載<br>
<br>

### 動作確認OS
```
Windows 10 (Python 3.10.2)
CentOS 7 (Python 3.9.13)
```

<a id="anchor3"></a>
## 3. 初期設定⚙
### clone

#### HTTPS
```
$ git clone https://github.com/poi-ai/keibaAI.git
```

#### SSH
```
$ git clone git@github.com:poi-ai/keibaAI.git
```

### pipのアップデート
```
$ python -m pip install pip==22.3.1
```

### 外部ライブラリのインストール
```
$ pip install -r requirements.txt
```

### 共通ディレクトリをモジュールパスに追加
プログラムが実行される際は、共通ディレクトリをモジュールパスへ追加する処理が含まれているため、この手順を踏まなくても実行時にimportエラーは起こりませんが、<br>
開発環境によってはコーディングの際に警告が出る場合が出るため、それを避けるための手順です。<br>
[Wiki](https://github.com/poi-ai/keibaAI/wiki/%E5%85%B1%E9%80%9A%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA%E3%82%92%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB%E3%83%91%E3%82%B9%E3%81%AB%E8%BF%BD%E5%8A%A0%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95)に記載しています。
<br>
<br>
<a id="anchor4"></a>
## 4. 実行🤖

### 4.1 パラメータ設定

#### 必須
* `/config/config.py.sample`をコピーし、同階層に`config.py`という名前で保存
* `config.py`へ起動させるシステムや設定値の記載

#### 任意(データベースを使用する場合のみ設定)
* `/config/dbconfig.py.sample`をコピーし、同階層に`dbconfig.py`という名前で保存
* `dbconfig.py`へデータベースの接続設定の記載


### 4.2 プログラム実行

```
$ cd <ローカルリポジトリのパス>
$ python main.py
```

で実行！
