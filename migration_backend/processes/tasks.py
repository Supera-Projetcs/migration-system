import logging
from pathlib import Path

import polars as pl
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.conf import settings
from sqlalchemy import create_engine


@shared_task(bind=True, max_retries=3)
def process_chunk(self, file_path, start_row, end_row):
    try:
        headers_df = pl.read_csv(file_path, n_rows=1)
        headers = headers_df.columns

        chunk_df = pl.read_csv(
            file_path,
            skip_rows=start_row,
            n_rows=end_row - start_row,
        )
        chunk_df.columns = headers

        chunk_df = chunk_df.to_pandas()

        engine = create_engine(
            "postgresql://developerjusinvestments@127.0.0.1:5432/migration_backend",
        )

        chunk_df.to_sql(clean_file_name(file_path), engine, if_exists="append", index=False)

    except Exception as exc:
        try:
            raise self.retry(exc=exc)
        except MaxRetriesExceededError as e:
            logging.exception(f"Task failed after maximum retries: {e}")


@shared_task
def stream_csv_in_chunks(file_path, chunk_size=10000):

    with Path.open(file_path) as f:
        total_lines = sum(1 for line in f)

        f.seek(0)

        for start_row in range(0, total_lines, chunk_size):
            end_row = min(start_row + chunk_size, total_lines)
            process_chunk.delay(str(file_path), start_row, end_row)

def clean_file_name(file_path):
    file_name = file_path.split("/")[-1]
    file_name = file_name.replace(".csv", "")
    file_name = file_name.replace("-", "_")
    return file_name

@shared_task
def all_files():
    files = ["tags.csv", "ratings.csv", "movies.csv", "links.csv", "genome-scores.csv", "genome-tags.csv"]
    for file in files:
        stream_csv_in_chunks(f"{settings.BASE_DIR}/files/{file}")
