```python
# None bool int float
# List tuple dict set frozenset deque
# datetime.date datetime.time datetime.datetime UUID bytes Decimal



```

# dependency-injector

# Lagom

```shell
APP_ENV=prod uvicorn run:app  --workers 5   --reload 
```

```shell
lefthook run pre-commit  --all-files 
```

```shell
APP_ENV=prod celery -A celery_app.celery_app worker  -Q send_email,generate_report --loglevel=info
```

```shell
APP_ENV=prod  celery -A celery_app.celery_app beat --loglevel=info
```

```shell
APP_ENV=prod celery -A celery_app.celery_app flower
```
