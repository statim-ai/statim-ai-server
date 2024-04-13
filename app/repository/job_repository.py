import os

from model.job import Job
from utils.simple_logger import SimpleLogger
from utils.sqlitedb import SQLiteDB

for key, value in os.environ.items():
    print(f"{key}: {value}")

JOBS_DB_FILE = os.environ["SQLITE_FILE_JOBS"]


class JobRepository:
    def __init__(self) -> None:
        self.logger = SimpleLogger()
        self.sqlitedb = SQLiteDB(JOBS_DB_FILE)
        self.__create_table()

    def __create_table(self):
        self.logger.debug("[JobRepository] __create_table")

        self.sqlitedb.execute_query("""CREATE TABLE IF NOT EXISTS jobs (
                                    id INTEGER PRIMARY KEY,
                                    prompt TEXT,
                                    status TEXT,
                                    model TEXT,
                                    result TEXT,
                                    result_type TEXT,
                                    timestamp TIMESTAMP)""")

    def create_job(self, job: Job):
        self.logger.debug("[JobRepository] create_job")

        job.id = self.sqlitedb.execute_insert(
            "INSERT INTO jobs (prompt, status, model, timestamp) VALUES (?, ?, ?, ?)",
            (job.prompt, job.status.serialize(), job.model, job.timestamp),
        )
        return job

    def update_job(self, job: Job):
        self.logger.debug("[JobRepository] update_job")

        job.id = self.sqlitedb.execute_update(
            "UPDATE jobs SET status = ?, result = ?, result_type = ? WHERE id = ?",
            (job.status.serialize(), job.result, job.result_type.serialize(), job.id),
        )
        return job

    def get_by_id(self, id: int):
        self.logger.debug("[JobRepository] get_by_id")

        rows = self.sqlitedb.execute_select(
            "SELECT prompt, status, model, result, result_type, id, timestamp FROM jobs WHERE id=?",
            (id,),
        )

        if len(rows) == 1:
            return self.map_row_to_job(rows[0])
        else:
            return None

    def get_all(self):
        self.logger.debug("[JobRepository] get_all")

        rows = self.sqlitedb.execute_select(
            "SELECT prompt, status, model, result, result_type, id, timestamp FROM jobs"
        )

        return [self.map_row_to_job(row) for row in rows]

    @staticmethod
    def map_row_to_job(row):
        return Job(
            prompt=row["prompt"],
            status=row["status"],
            model=row["model"],
            result=row["result"],
            result_type=row["result_type"],
            id=row["id"],
            timestamp=row["timestamp"],
        )
