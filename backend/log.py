from datetime import date
import logging
from pathlib import Path

log_path = Path('./log/')
today_date = date.today().isoformat()

def create_log():
    log_path.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=log_path / f'{today_date} change.txt',
        encoding='utf-8',
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def clean_log():
    today_year, today_month = date.today().year, date.today().month

    for log in log_path.iterdir():
        if log.is_file():
            log_year, log_month = int(log.stem[:4]), int(log.stem[5:7])
            if log_year < today_year or (log_year == today_year and log_month < today_month):
                log.unlink()