# Automated Cybercrime Profiler

An app to detect suspicious posts (violent and abusive posts) on a Blog and automatically create a cybercriminal profile (age, gender, education level, employment status) of the author.

## Database
- Run MySql 
- See Config file in Blog and Config file in ProfilerApp for DB name.
- Using flask-sqlalchemy 
-- See models.py for DB Tables for Blog and ProfilerApp
- Example for Blog:
```sh
from Blog import db, create_app
from Blog.models import Posts,Users,Comments
app = create_app()
app.app_context().push()
db.create_all()
```

## Blog Website
- Create Database
- Activate Virtual Environment
- Run requirements.txt
- ```sh python3 run.py ```

## Profiler App
- Create Database
- Activate Virtual Environment
- Run requirements.txt
- ```sh python3 run.py ```

##SuspiciousDetector_ML
- ```sh python3 Main.py ``` (optional only to retrain models)
- ```sh python3 SuspiciousDetectorAPI.py ```
