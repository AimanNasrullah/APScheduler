# 4 COMPONENTS

## Job

- Represents **what should be run**.
- the task you schedule (what function, when to run, etc.).
- Contains:
  - The callable/function to execute
  - Arguments and keyword arguments
  - A reference to its trigger
  - Some metadata (id, name, next run time, etc.)
- The job itself does **not** decide *when* to run — that is the trigger’s role.

## triggers
- contain the scheduling logic
- where the APScheduler keeps the list of jobs
- each job has its own trigger which determines WHEN the JOB should be run next

## job stores
- house the scheduled jobs
- default job store keeps jobs in memory
- others store in various kind of db
- A job's data is SERIALIZED when it is saved to a job store , and deserialized when its loaded back from it.
- Job stores (other than the default one) dont keep jobs in memory but act as middlemen for saving, loading, updating and searching jobs in the backend.
- Job stores must NEVER be shared between schedulers.

## executors
- HANDLES the running of the jobs
- decide how to actually run the function (in a thread, process, etc)
- typically submitting the designated callable in a job TO a thread or process pool.
- when job is done, it notifies the scheduler which then emits an appropriate event

## schedulers
- BIND the rest together
- decides when a job should run.
- typically have one scheduler running in our application
- Configuring the job stores and executors is done through the scheduler, as is adding, modifying and removing jobs.

## Summary

- **Job Store** = *Where the jobs are stored*  
  (in memory, database, etc.)
- **Job** = *What to run*  
  → “Run this function with these args (and some metadata).”
- **Trigger** = *When to run it*  
  → The rules/schedule, e.g. cron, interval, date  
  → “Given now, when is the next run time?”
- **Executor** = *How/where to execute it*  
  → Runs the job function in a thread or process (ThreadPoolExecutor, ProcessPoolExecutor, etc.)
- **Scheduler** = *The coordinator*  
  → Keeps track of jobs, asks triggers for next run times,  
     and tells executors **which jobs to run and when**.

## Choosing the right scheduler, job store(s), executor(s) and trigger(s)
Your choice of scheduler depends mostly on your programming environment and what you’ll be using APScheduler for.

### APScheduler Scheduler Types

1. **BlockingScheduler**: use when the scheduler is the only thing running in your process.
2. **BackgroundScheduler**: use when you’re not using any of the frameworks below, and want the scheduler to run in the background inside your application
3. **AsyncIOScheduler**: use if your application uses the asyncio module
4. **GeventScheduler**: use if your application uses gevent
5. **TornadoScheduler**: use if you’re building a Tornado application
6. **TwistedScheduler**: use if you’re building a Twisted application
7. **QtScheduler**: use if you’re building a Qt application

# How to Pick the Appropriate Job Store

The key question:

> **Do you need job persistence?**  
> (Persistence = does the job still exist after the app/scheduler restarts or crashes?)

---

## ✅ If you **DO** need persistence

You need jobs to **survive restarts or crashes**.

Typical scenario:

- A user creates a schedule via a UI → this schedule must be **saved** somewhere (e.g. DB).
- When the app starts again, it should **load jobs from storage**, not recreate them manually in code.

In this case, you should use a **persistent job store**, such as:

- `SQLAlchemyJobStore` (backed by a relational DB, e.g. PostgreSQL, MySQL)
- `MongoDBJobStore`
- Other database-backed job stores

With a persistent job store:

- APScheduler **serializes** jobs and saves them into the database.
- On restart, it **deserializes** and restores them back into the scheduler.

---

## ❌ If you **DO NOT** need persistence

You are okay with **recreating all jobs at startup**.

Typical scenario:

- Every time your app starts, your code calls `add_job(...)` again to register all the jobs.
- If the app stops, you don’t care about the old jobs stored anywhere because they will be recreated on startup.

In this case:

- Jobs live **only in memory (RAM)**.
- If the app restarts:
  - APScheduler forgets all jobs (they were only in memory).
  - Your startup code re-adds them.

This is exactly what the default **`MemoryJobStore`** does.

# How to choose Executor
- Has few executors but the main ones are:
1. ThreadPoolExecutor (default)
2. ProcessPoolExecutor

ThreadPoolExecutor vs ProcessPoolExecutor
ThreadPoolExecutor (default)

Runs jobs in threads inside the same Python process.

Good for I/O-bound tasks:

Calling an API

Querying DB

Writing files

Waiting on network, etc.

Cheap to create, low overhead.

ProcessPoolExecutor

Runs jobs in separate processes (multiprocessing).

Good for CPU-bound tasks:

Heavy calculations

Big Pandas transformations

Complex data processing in Python

Uses multiple CPU cores properly (bypasses GIL by using multiple processes).

More overhead (starting processes, serialization of args/results, etc.).

can configure APScheduler to use both, e.g.:

Default = thread pool

Special heavy jobs = process pool

means that if logic directly in the APscheduler executor (and using pandas for transforamtion esp) use ProcessPoolExecutor

# KEY TAKEAWAYS

Q: After creating a schedule via the API, how does APScheduler track and execute jobs at the correct time?

  1. When? - APScheduler checks next_run_time column every second
  2. Which? - APScheduler stores serialized function reference + parameters in database
  3. How? - Background loop continuously queries database for due jobs
  4. Persistence - Everything stored in PostgreSQL, survives restarts
  5. Calculation - After execution, APScheduler calculates next run time based on trigger type (cron/interval)


## NEWSS project architecture (FastAPI + Redis + Celery)
Then Celery worker does:

either heavy Pandas

or call stored procedure in Postgres

So:

APScheduler job itself = very light (just sends a Celery task)

Heavy things happen in:

Celery worker processes

or in Postgres (stored procedure)

In this architecture, APScheduler does not need ProcessPoolExecutor for CPU scaling, because:

The CPU-heavy work is already offloaded to Celery, which uses multiple processes.

APScheduler is just an orchestrator / scheduler, not the worker.

So for you:

ThreadPoolExecutor is enough (and simpler)

# KB WAY:
  ## 1️⃣ Manual Trigger (User-initiated)

  User → POST /api/v1/search/start
      ↓
  FastAPI handler
      ↓
  background_tasks.add_task(run_all_scrapers, ...)  # FastAPI BackgroundTasks
      ↓
  run_all_scrapers() executes in background thread
      ↓
  Database operations (scraping)

  ## 2️⃣ Schedule Creation (One-time setup)

  User → POST /api/v1/schedule/create
      ↓
  FastAPI handler:
      - Save schedule to PostgreSQL
      - scheduler_service.add_schedule()
      ↓
  APScheduler stores job → waits for scheduled time

  ## 3️⃣ Schedule Execution (Happens at scheduled time)

  APScheduler timer fires
      ↓
  execute_scheduled_scraping() function
      ↓
  run_all_scrapers() executes directly
      ↓
  Database operations (scraping)

  ---


