### 起動システム設定 ###

# 起動させるシステムの種類[必須]
# scraping(データ取得) or analysis(データ分析) [現在はscrapingのみ使用可能]
SCRIPT_TYPE = 'scraping'

# 取得するデータの種類[SCRIPT_TYPE=scraping選択時は必須]
# race(レースデータ) or odds(オッズデータ)
DATA_TYPE = 'race'

# 取得するデータの期間[SCRIPT_TYPE=scraping選択時は必須]
# past(過去データ) or now(現在データ)
DATA_TIME = 'past'

# 対象の開催
# JRA(中央) or NAR(地方)
ASSOSIATION = 'JRA'

### 他 ###

# システムの起動結果をLINE Notifyへ通知を行いたい場合は設定[任意]
LINE_TOKEN = ''


