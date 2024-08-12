import logging
from pathlib import Path
from migration_backend.processes.models import UploadedFile, ProcessChunk

import polars as pl
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.conf import settings
from sqlalchemy import create_engine
import psycopg2
import io
from django.utils import timezone


@shared_task(bind=True, max_retries=3)
def process_chunk(self, file_path, start_row, end_row, uploaded_file_id):
    uploaded_file = UploadedFile.objects.get(id=uploaded_file_id)

    chunk_df = pl.read_csv(file_path, skip_rows=start_row, n_rows=end_row - start_row)

    print(chunk_df.head())

    table_name = clean_file_name(file_path)

    csv_buffer = io.BytesIO()
    csv_data = chunk_df.write_csv(csv_buffer)

    csv_buffer.seek(0)

    conn = psycopg2.connect(
        dbname="migration_backend",
        user="developerjusinvestments",
        password="",
        host="127.0.0.1",
        port="5432",
    )
    cursor = conn.cursor()

    try:
        if table_name == "ratings":
            cursor.copy_expert(f"COPY ratings(userId, movieId, rating, timestamp) FROM STDIN WITH CSV HEADER", csv_buffer)
        if table_name == "tags":
            cursor.copy_expert(f"COPY tags(userId, movieId, tag, timestamp) FROM STDIN WITH CSV HEADER", csv_buffer)
        if table_name == "movies":
            cursor.copy_expert(f"COPY movies(movieId, title, genres) FROM STDIN WITH CSV HEADER", csv_buffer)
        if table_name == "links":
            cursor.copy_expert(f"COPY links(movieId, imdbId, tmdbId) FROM STDIN WITH CSV HEADER", csv_buffer)
        if table_name == "genome_scores":
            cursor.copy_expert(f"COPY genome_scores(movieId, tagId, relevance) FROM STDIN WITH CSV HEADER", csv_buffer)
        if table_name == "genome_tags":
            cursor.copy_expert(f"COPY genome_tags(tagId, tag) FROM STDIN WITH CSV HEADER", csv_buffer)

        conn.commit()
        uploaded_file.success_count += 1

    except Exception as e:
        conn.rollback()
        uploaded_file.error_count += 1
        try:
            raise self.retry(exc=e, countdown=5)
        except MaxRetriesExceededError as exc:
            ProcessChunk.objects.create(
                process_id=uploaded_file_id,
                start_row=start_row,
                end_row=end_row,
                status="failed",
                errors=str(exc),
            )
            logging.exception(f"Task failed after maximum retries: {e}")
    finally:
        cursor.close()
        conn.close()
        end_time = timezone.now()
        uploaded_file.end_time = end_time
        uploaded_file.processing_duration = end_time - uploaded_file.start_time
        uploaded_file.save()


@shared_task
def stream_csv_in_chunks(file_path, uploaded_file_id, chunk_size=30000):

    with Path.open(file_path) as f:
        total_lines = sum(1 for line in f)

        f.seek(0)

        total_chunks = total_lines // chunk_size
        if total_chunks < 12:
            chunk_size = total_lines // 12
            total_chunks = total_lines // chunk_size

        for start_row in range(0, total_lines, chunk_size):
            end_row = min(start_row + chunk_size, total_lines)
            process_chunk.delay(str(file_path), start_row, end_row, uploaded_file_id)


def clean_file_name(file_path):
    file_name = file_path.split("/")[-1]
    file_name = file_name.replace(".csv", "")
    file_name = file_name.replace("-", "_")
    return file_name


@shared_task
def all_files():
    files = [
        "tags.csv",
        "movies.csv",
        "links.csv",
        "genome-scores.csv",
        "genome-tags.csv",
        "ratings.csv",
    ]
    for file in files:
        stream_csv_in_chunks(f"{settings.BASE_DIR}/files/{file}", 1)
