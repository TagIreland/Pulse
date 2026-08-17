# Pulse — TAG Build Sprint starter project

A three-day build sprint. Two teams, one dashboard, one client.

- **Development team** — the Spring Boot API in `api/` and the Angular dashboard in `web/`.
- **Data team** — the Python jobs and SQL in `data/`.

Everything in this repository already runs. Nothing in it is finished. Read
`AGREEMENT.md` first thing on Day 1 — until that is filled in, neither team knows
what they are building.

---

## What you need installed

| | Version | Check with |
|---|---|---|
| Git | any recent | `git --version` |
| Java | 21 | `java -version` |
| Node | 20 or newer | `node -v` |
| Python | 3.11 or newer | `python3 --version` |

The development team also needs IntelliJ IDEA (Community is fine) and the Angular CLI
(`npm install -g @angular/cli`). Both teams want Postman. Nobody needs to install
Postgres — the database is hosted on Supabase.

---

## Running the three pieces

### 1. The API — `api/`

```bash
cd api
./mvnw spring-boot:run
```

Then check it answers:

```bash
curl http://localhost:8080/api/sessions
```

You should get a small JSON array of hardcoded example sessions. That is deliberate:
the dashboard is built against this shape on Day 1 while the database is still being
designed, and on Day 2 the same endpoint starts returning real data without the
dashboard changing at all.

> If `./mvnw` is missing, someone skipped a setup step. Run `mvn -N wrapper:wrapper`
> once inside `api/` and commit what it generates.

### 2. The dashboard — `web/`

```bash
cd web
npm install
npm start
```

Open <http://localhost:4200>. One tile, reading `/api/sessions` over HTTP.

The first time it calls the API the browser will refuse the request. That is CORS,
it is fixed in the API rather than in Angular, and `api/.../config/WebConfig.java`
is where you will end up. Read about what you are allowing before you allow it.

### 3. The data jobs — `data/`

```bash
cd data
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then fill it in. Never commit it.

python fetch.py --endpoint sessions --year 2024 --dry-run
```

`--dry-run` prints what it found and writes nothing. Drop it once you have a
`DATABASE_URL`.

---

## The rules

1. **Nobody pushes to `main`.** Branch, open a pull request, get it reviewed by
   somebody from the *other* team.
2. **No secrets in the repository.** Connection strings and service-account keys live
   in `.env` and in GitHub Actions secrets. `.gitignore` already covers the obvious
   cases; it will not save you from a password pasted into a source file.
3. **The dashboard talks to the API. The API talks to the database. Neither skips a
   step.** If the front end holds a database password you have published your
   database to every visitor.
4. **The API reads views, not raw tables.** If the API needs something that is not in
   a view, that is a request to the data team, not a five-table join in Java.

---

## Layout

```
api/     Spring Boot 3 / Java 21. One endpoint returning a hardcoded example.
web/     Angular. One component, one service, one tile, chart.js installed.
data/    Python. fetch.py pulls from OpenF1; predict.py is the Day 2 prediction.
         sql/ holds the schema you design.
.github/workflows/build.yml   builds all three on every push.
AGREEMENT.md   fill this in on Day 1 morning. It is the contract between the teams.
DATA-NOTES.md  the data team fills this in as they go.
```
