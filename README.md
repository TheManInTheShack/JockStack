# JockStack

Explore the algebra of Jocks' names. Inspired by the Nac Mac Feegle, with thanks to Sir Terry Pratchett.

## Architecture

```
backend/    FastAPI app — algorithm, API endpoints, SQLite persistence
frontend/   Godot 4 project — HTML5 export served as the web UI
deploy/     Nginx config, systemd unit, setup and deploy scripts
data/       SQLite database (not committed to git, lives on the server)
archive/    Original v1 Dash/Python implementation
```

---

## Local Development — Testing Procedure

### First-time setup

- [ ] Clone the repo and switch to the working branch
  ```
  git clone https://github.com/TheManInTheShack/JockStack.git
  cd JockStack
  git checkout claude/general-session-pZg44
  ```

- [ ] Create a Python virtual environment in the repo root
  ```
  python -m venv venv
  ```

- [ ] Activate the venv
  - **Windows:** `venv\Scripts\activate`
  - **Linux/Mac:** `source venv/bin/activate`
  - Your prompt should change to show `(venv)`

- [ ] Install backend dependencies
  > **Important:** Use `python -m pip`, not `pip` directly — on Windows, bare `pip` can resolve to the system Python and install in the wrong place.
  ```
  python -m pip install -r backend\requirements.txt
  ```

### Running the dev server

- [ ] From the repo root, start FastAPI with auto-reload
  ```
  python -m uvicorn main:app --app-dir backend --reload
  ```
  > **Note:** Use `python -m uvicorn`, not `uvicorn` directly — same reason as above.
  > `--app-dir backend` tells uvicorn to resolve imports from the `backend/` folder.

- [ ] Confirm the server is running — you should see:
  ```
  INFO:     Uvicorn running on http://127.0.0.1:8000
  ```

### Verifying the API

- [ ] Open `http://localhost:8000/docs` in a browser — FastAPI's interactive docs should load

- [ ] Test `POST /api/generate`:
  - Click the endpoint → **Try it out** → set `num_jocks` to any number 1–1000 → **Execute**
  - Response should contain a sorted list of Jocks with names and a stats block

- [ ] Confirm a run was saved — check the summary endpoint:
  ```
  http://localhost:8000/api/stats/summary
  ```
  `total_runs` should be 1 (or more if you've run multiple tests)

- [ ] Optional curl test (from a second terminal with the venv active):
  ```
  curl -X POST http://localhost:8000/api/generate -H "Content-Type: application/json" -d "{\"num_jocks\": 7}"
  ```

### Stopping

- [ ] Stop the server: `Ctrl+C`
- [ ] Deactivate the venv: `deactivate`

### Updating after a pull

Run `update.bat` (Windows) from the repo root — it pulls latest, ensures the venv exists, reinstalls dependencies, and prints the correct run command.

---

## Running Tests

_Test suite to be added in a future phase._

---

## Deployment

See `deploy/README.md` (coming in a future phase).
