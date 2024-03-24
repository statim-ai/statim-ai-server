from model.job import Job
from utils.simple_logger import SimpleLogger
from utils.sqlitedb import SQLiteDB

class JobRepository:

    def __init__(self) -> None:
        self.logger = SimpleLogger()
        self.sqlitedb = SQLiteDB('jobs.db')
        self._create_table()


    def _create_table(self):
        self.logger.info('[JobRepository] _create_table')

        self.sqlitedb.execute_query('''CREATE TABLE IF NOT EXISTS jobs (
                                    id INTEGER PRIMARY KEY,
                                    text TEXT,
                                    status TEXT,
                                    model TEXT,
                                    timestamp TIMESTAMP)''')

    
    def create_job(self, job:Job):
        self.logger.info('[JobRepository] create_job')

        job.id = self.sqlitedb.execute_insert("INSERT INTO jobs (text, status, model, timestamp) VALUES (?, ?, ?, ?)", (job.text, job.status.serialize(), job.model, job.timestamp))
        return job


    def update_job(self, job:Job):
        self.logger.info('[JobRepository] update_job')
        
        job.id = self.sqlitedb.execute_update("UPDATE jobs SET status = ? WHERE id = ?", (job.status.serialize(), job.id))
        return job

    
    def get_by_id(self, id:int):
        self.logger.info('[JobRepository] get_by_id')

        rows = self.sqlitedb.execute_select("SELECT text, status, model, id, timestamp FROM jobs WHERE id=?", (id,))

        if len(rows) == 1:
            row = rows[0]
            return Job(text=row[0], status=row[1], model=row[2], id=row[3], timestamp=row[4])
        else:
            return None

    
    def get_all(self):
        self.logger.info('[JobRepository] get_all')

        rows = self.sqlitedb.execute_select("SELECT text, status, model, id, timestamp FROM jobs")

        return [Job(text=row[0], status=row[1], model=row[2], id=row[3], timestamp=row[4]) for row in rows]
