"""Module with the repository class for Jobs."""

import os

from model.job import Job
from utils.simple_logger import SimpleLogger
from utils.sqlitedb import SQLiteDB

JOBS_DB_FILE = os.environ["SQLITE_FILE_JOBS"]


class JobRepository:
    """Repository pattern class to abstract the persistance an retrieve of Jobs."""

    def __init__(self) -> None:
        """Initialzes the database."""
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
        """Creates a new database entry for the given Job."""
        self.logger.debug("[JobRepository] create_job")

        job.job_id = self.sqlitedb.execute_insert(
            "INSERT INTO jobs (prompt, status, model, timestamp) VALUES (?, ?, ?, ?)",
            (job.prompt, job.status.serialize(), job.model, job.timestamp),
        )
        return job

    def update_job(self, job: Job):
        """Updates a Job on the database."""
        self.logger.debug("[JobRepository] update_job")

        job.job_id = self.sqlitedb.execute_update(
            "UPDATE jobs SET status = ?, result = ?, result_type = ? WHERE id = ?",
            (
                job.status.serialize(),
                job.result,
                job.result_type.serialize(),
                job.job_id,
            ),
        )
        return job

    def get_by_id(self, job_id: int):
        """Gets a Job by ID from the database."""
        self.logger.debug("[JobRepository] get_by_id")

        rows = self.sqlitedb.execute_select(
            """SELECT prompt, status, model, result, result_type, id, timestamp
              FROM jobs WHERE id=?""",
            (job_id,),
        )

        if len(rows) == 1:
            return self.map_row_to_job(rows[0])
        else:
            return None

    def get_all(self):
        """Gets all Jobs from the database."""
        self.logger.debug("[JobRepository] get_all")

        rows = self.sqlitedb.execute_select(
            "SELECT prompt, status, model, result, result_type, id, timestamp FROM jobs"
        )

        return [self.map_row_to_job(row) for row in rows]

    @staticmethod
    def map_row_to_job(row):
        """Convert database row in a Job object."""
        return Job(
            prompt=row["prompt"],
            status=row["status"],
            model=row["model"],
            result=row["result"],
            result_type=row["result_type"],
            job_id=row["id"],
            timestamp=row["timestamp"],
        )
