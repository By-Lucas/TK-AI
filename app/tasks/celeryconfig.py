from celery.schedules import crontab

beat_schedule = {
    "treinar_ia_diariamente": {
        "task": "app.tasks.fetch_new_articles_task.fetch_and_train_from_api_task",
        "schedule": crontab(hour=3, minute=0),
    }
}
