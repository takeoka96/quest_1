"""
EDINET APIからデータを取得するモジュール
"""
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("EDINET_API_KEY")
BASE_URL = "https://disclosure.edinet-fsa.go.jp/api/v2"


def get_documents_by_date(date: str) -> dict:
    """
    指定した日付の書類一覧を取得する
    date: "YYYY-MM-DD" 形式
    """
    url = f"{BASE_URL}/documents.json"
    params = {
        "date": date,
        "type": 2,
        "Subscription-Key": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()


def filter_annual_reports(result: dict) -> list:
    """
    一般事業会社の有価証券報告書のみを抽出する
    docTypeCode: 120 = 有価証券報告書
    ordinanceCode: 010 = 一般事業会社
    """
    if not result.get('results'):
        return []
    return [
        doc for doc in result['results']
        if doc.get('docTypeCode') == '120'
        and doc.get('ordinanceCode') == '010'
    ]


def get_annual_reports_bulk(start_date: str, end_date: str) -> pd.DataFrame:
    """
    指定期間の有価証券報告書一覧を取得する
    start_date, end_date: "YYYY-MM-DD" 形式
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    all_reports = []
    current = start

    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        try:
            result = get_documents_by_date(date_str)
            reports = filter_annual_reports(result)
            all_reports.extend(reports)
        except Exception as e:
            print(f"{date_str}: エラー {e}")

        time.sleep(1)
        current += timedelta(days=1)

    return pd.DataFrame(all_reports)


def download_document(doc_id: str) -> bytes:
    """
    docIDを指定して書類をZIPでダウンロードする
    """
    url = f"{BASE_URL}/documents/{doc_id}"
    params = {
        "type": 1,
        "Subscription-Key": API_KEY
    }
    response = requests.get(url, params=params)
    return response.content