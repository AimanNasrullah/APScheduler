# Serialization (APScheduler Context)

**Serialization** = converting a Python object into a simple format (string/bytes) so it can be saved in a database or file.  
**Deserialization** = converting that stored data back into the original Python object.

---

## Example 1: Python Object → JSON String

### A. Original Python object

```python
person = {
    "name": "Aiman",
    "age": 25,
    "skills": ["python", "sql", "etl"]
}
```

Databases cannot store this as a raw Python object, so we **serialize** it.

### B. Serialize using JSON

```python
import json

serialized = json.dumps(person)
print(serialized)
```

Output:

```text
{"name": "Aiman", "age": 25, "skills": ["python", "sql", "etl"]}
```

✔️ Now the data is simple text → easy to save in a database.

---

## Example 2: How APScheduler Serializes a Job

### A. Your job function

```python
def send_email(user_id):
    print("Sending email to user:", user_id)
```

APScheduler **cannot store the actual function object** in the database.

### B. APScheduler stores the *serialized* job like this:

```json
{
    "func": "path.to.module.send_email",
    "args": [123],
    "trigger": "...",
    "next_run_time": "..."
}
```

This is serialization — APScheduler stores only the instructions needed to rebuild the job later.

---

## Deserialization (When APScheduler Loads Jobs Back)

When APScheduler restarts or loads jobs from the job store, it:

1. **Imports the function** using the string path `"path.to.module.send_email"`.
2. **Rebuilds the trigger**.
3. **Restores the job object** in memory.

This fully reconstructs the original Python job.


# EVENT (in general)
- an event is a structured notification that something happened in the system. It usually contains what happened, when it happened, and extra data. Other parts of the system can listen for these events and react to them.”
