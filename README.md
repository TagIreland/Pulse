# Pulse — TAG Build Sprint

A three-day build sprint. One client, one dashboard, two teams.

Grid Insights — a small analytics company (simulated) — wants a Formula 1 dashboard.
There is a free public API full of race timing data, nobody has ever put it in a database,
and there is no engineering team. That is you.

Everything in this repository already runs. Nothing in it is finished. Read `AGREEMENT.md`
first thing on Day 1 — until that is filled in, neither team knows what they are building.

The TODO comments in the code are the map. Search the repository for `TODO` on the first
morning and you have your backlog.

---

## Who does what

|  | Development team | Data team |
|---|---|---|
| **Builds** | A Spring Boot REST API in Java, and an Angular dashboard that consumes it. | A Postgres database, a Python job that fills it, and one prediction published to Firebase. |
| **Owns the platforms** | GitHub, GitHub Actions, Vercel. | Supabase (Postgres), Firebase, the OpenF1 API. |
| **Skills you will use** | Java, Spring Boot, REST. Angular, TypeScript, components and services. Git — branches, pull requests, reviews. GitHub Actions — build and deploy on push. Layered architecture and why the layers exist. | SQL — joins, aggregates, views. Postgres — tables, keys, indexes. Reading and paging a REST API. Normalisation — turning messy JSON into proper tables. Python and scikit-learn for one ML prediction. |
| **By Friday you can say** | I built and shipped a Java API and an Angular front end, in a real Git workflow, deployed by a pipeline I set up. | I sourced live data, designed and normalised the database it lives in, wrote the queries the application runs on, and put a ML prediction of my own on the screen. |

Roles inside each team: split the work on the first morning and write it on the whiteboard.
With two people in a team, one takes the back end and one the front end (development), or
one takes ingestion and one takes the model and queries (data). Everyone runs a standup at
least once.

---

## The data

You are building on OpenF1 — a free, open API of Formula 1 timing data at openf1.org. It
returns plain JSON, and no key is needed for the historical data you will be using.

**Roughly what is in it:**

- **Meetings and sessions** — which race weekend, which circuit, whether a session was practice, qualifying or the race.
- **Drivers** — car number, name, team.
- **Laps** — lap number, lap time and sector times, per driver per session. This is the big one.
- **Pit stops and stints** — when a driver stopped, for how long, and which tyre compound they went out on.
- **Position and intervals** — the running order as it changed through a session.
- **Weather** — air and track temperature, humidity, rainfall, trackside.
- **Race control** — flags, safety cars, penalties, as messages.
- **Car telemetry** — speed, throttle, brake and gear, sampled several times a second for every car. One race is millions of rows. Take a small slice or leave it alone — filling your free database on Day 1 is an annoying way to lose an afternoon.

**First job, before you write anything:** read the documentation at openf1.org and get one
real response back in Postman. Find out what the endpoints are actually called, what
parameters they take, how you page through a large response, and what one record looks like.

```bash
# check these against the live docs rather than trusting this file
curl "https://api.openf1.org/v1/sessions?year=2024"
curl "https://api.openf1.org/v1/laps?session_key=<key>&driver_number=1"
curl "https://api.openf1.org/v1/stints?session_key=<key>"
```

**Then decide what the dashboard shows.** Four tiles — take four of these, or invent better ones:

- Lap time progression through a session, one line per driver.
- Tyre strategy — a stint timeline showing compound and laps for each driver.
- Pit stops — who stopped, on which lap, and for how long.
- Weather against pace — did track temperature move lap times?
- Race control — the flags and safety cars, against where they fell in the session.
- **Predicted against actual lap time.** This is the data team's ML prediction tile, so make it one of your four.

**Then agree three things, together, and write them down:**

1. Which four tiles.
2. What tables the database needs to answer them.
3. What the API endpoints are called and what shape they return.

On paper and in `AGREEMENT.md`. That is the only agreement the two teams need.

---

## How it fits together

Three architecture rules, and the reason for each:

- **The Angular app never talks to the database.** Only to the API. If the front end holds a database password, you have just published your database to every visitor.
- **The API reads views, not raw tables.** The data team publishes a view for each thing the dashboard needs. If the API has to join five tables to answer a question, that logic belongs in the database where there is one copy of it.
- **The ML prediction goes to Firebase, not through the API.** It is calculated once by a Python job and published as a small document the Angular app reads directly. This is a real pattern — pre-compute the expensive thing, serve it cheaply — and it gives the data team its own route to the screen.

---

## Nobody waits for anybody

Two teams building two halves of one thing usually means one team sitting idle. Four
deliberate choices stop that happening here.

1. **The shapes are agreed in the first hour.** Table names and endpoint shapes, written down. That is the only dependency between the teams and it is settled before lunch on Day 1.
2. **The development team starts with hardcoded responses.** Your first endpoint returns a fixed example in the agreed shape. The Angular app is built, styled and deployed against that while the database is still being designed. Swapping in the real query later is a one-line change.
3. **The data team starts with raw tables and plain SQL.** You need nobody's API to load data and query it. You will be running real queries on real data on Day 1 afternoon.
4. **Firebase is the data team's own lane to the dashboard.** You publish your ML prediction there and it appears on screen without going through anyone else's code.

If you are ever blocked for more than ten minutes waiting on the other team, that is a
standup item, not something to sit with.

---

## Day 1 setup

Nothing is installed. Work through this from the top; it takes about ninety minutes and
a facilitator will be circulating the whole time. If an installer is blocked by your
laptop or the network, say so straight away rather than fighting it.

### Accounts — both teams

- **GitHub** — create an account using your Accenture email (one person forks the repository and sends an invitation to the rest of the group).
- **Your licensed AI assistant**, signed into your IDE. Check it actually responds before you move on.

### Accounts — development team

- **Vercel** — one person signs in with GitHub and creates the project (nominate this person as a group). The free Hobby plan is personal, so only one account owns the deployment. Everyone else contributes by pushing to the repo — Vercel picks up the push via GitHub and deploys automatically. The others do not need a Vercel account.

### Accounts — data team

- **Supabase** — one person signs in with GitHub and creates the project, then invites the rest of the team: Project Settings → Team → Invite. Everyone gets their own login and access to the SQL editor and connection string.
- **Firebase** — one person signs in with a Google account, creates the project, and enables Firestore in test mode, then invites the rest of the team: Project Settings → Users and permissions → Add member (Editor role). Everyone else signs in with their own Google account.

### Installing on a new Accenture laptop

Run PowerShell as a normal user throughout — you do not need admin, and the installs
below do not require it.

**1. Check Software Center first.** Some cohorts get Git and Python pre-approved there;
if yours does, install from there rather than bypassing the managed channel.

**2. Install via winget:**

```powershell
# Everyone
winget install --id Git.Git -e
winget install --id Microsoft.VisualStudioCode -e
winget install --id Postman.Postman -e

# Development team
winget install --id EclipseAdoptium.Temurin.21.JDK -e
winget install --id OpenJS.NodeJS.22 -e
winget install --id JetBrains.IntelliJIDEA.Community -e

# Data team
winget install --id Python.Python.3.12 -e
```

After each install, **close and reopen PowerShell** — winget writes to `PATH` but the
running shell does not pick it up until restarted.

**3. Verify:**

```powershell
git --version
java -version      # must say 21
node -v            # must say v22.x.x
python --version   # must say 3.12.x
```

> **If winget is not available:** it ships with Windows 11 but some managed images
> remove it. Try downloading the zip from each corresponding website and adding to PATH, raise a ticket with IT or ask your facilitator otherwise.

**4. Configure Git:**

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.name@accenture.com"
```

Authenticate to GitHub with a personal access token (classic, `repo` scope):
GitHub → Settings → Developer settings → Personal access tokens → Generate new token.
When Git first asks for a password, paste the token. Windows Credential Manager saves it.

**5. Angular CLI (development team) and Vercel CLI (one person only):**

```powershell
npm install -g @angular/cli   # everyone on the dev team
npm install -g vercel         # only the person who will run the deployment
```

You do not need to install Maven — the project comes with a wrapper that downloads its own.

**6. Before you go to lunch on Day 1:**

- Development team: `java -version` says 21, `ng version` works, and you can open a Spring project in VsCode.
- Data team: `python --version` works, your virtual environment activates, and you can run a SELECT in the Supabase SQL editor.
- Everyone: you can clone the repository, make a branch, and push it.

If any of that is not true, tell a facilitator now. It does not get cheaper to fix this afternoon.

---

## Running the three pieces

### 1. The API — `api/`

```bash
cd api
./mvnw spring-boot:run
```

Check it answers:

```bash
curl http://localhost:8080/api/sessions
```

You should get a small JSON array of hardcoded example sessions. That is deliberate:
the dashboard is built against this shape on Day 1 while the database is still being
designed, and on Day 2 the same endpoint starts returning real data without the
dashboard changing at all.

### 2. The dashboard — `web/`

```bash
cd web
npm install
npm start
```

Open <http://localhost:4200>. One tile, reading `/api/sessions` over HTTP.

The first time it calls the API the browser will refuse the request. That is CORS —
the browser blocking a cross-origin call. The fix is in the Spring API, not in Angular.
`api/.../config/WebConfig.java` is where you will end up. Read about what you are
allowing before you allow it.

### 3. The data jobs — `data/`

```bash
cd data
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then fill it in. Never commit it.

python fetch.py --endpoint sessions --year 2024 --dry-run
```

`--dry-run` prints what it found and writes nothing. Drop it once you have a `DATABASE_URL`.

A fallback snapshot of a 2024 race weekend is in `data/snapshot/` — if OpenF1 is slow
or rate-limiting on the day, ask your facilitator how to load it.

---

## The three days

Standup at 09:00 each morning — fifteen minutes, standing up, run by a different person
each day. Three things each: what I finished, what I am doing today, what is in my way.

End-of-day check-in at 17:00 — fifteen minutes. Each team shows the other what actually
runs. Not slides, not a description. This is where you find out that your endpoint
returns a string where the dashboard expects a number, on Day 1 rather than Day 3.

|  | Development team | Data team |
|---|---|---|
| **Day 1** | Setup. Create the repo. Get the Spring API and Angular app running. One endpoint returning hardcoded data, one Angular page showing it. | Setup. Explore OpenF1 by hand in Postman. Create the Supabase project. Write the Python script that pulls data into raw tables. Sketch the normalised schema on paper. |
| **Day 2** | Connect Spring to Postgres and replace hardcoded data with real queries. Build out the endpoints and the dashboard: charts, a filter, routing. Get GitHub Actions building both apps. Deploy the Angular app to Vercel. | Build the normalised tables and load them properly. Add keys, relationships and an index. Write the views the API needs. Then the Python ML prediction, published to Firebase. |
| **Day 3** | Finish the tiles, read the ML prediction from Firebase, handle the cases where things are slow or missing. Freeze at 14:00. Rehearse. | Tidy the queries, document where the data came from, check your numbers against the source. Freeze at 14:00. Rehearse. |

**Day 3, 16:00 — presentation.** Twelve minutes plus questions, to a panel from the
Software Engineering and Data & AI practices.

| By the end of | This should exist |
|---|---|
| Day 1 | A repository both teams can push to. A running Spring endpoint and a running Angular page, connected, with fake data. A Supabase database with real data in raw tables, and a SELECT that returns rows. |
| Day 2 | The Angular app deployed to a Vercel URL. The API reading real data from normalised tables through views. GitHub Actions building on every push. A ML prediction in Firebase. |
| Day 3, 14:00 | Everything above, working together, with the four dashboard tiles finished. No new features after this point. |

---

## Tasks — development team

You get the commands for the parts that are just typing. Everything else is a goal, a
nudge towards the right concepts, and a definition of done. Most issues should be able to be worked out from the
documentation and with your AI assistant beside you.

### D1 — Repository and Git workflow

```bash
# the starter project is already in your organisation — clone it
git clone https://github.com/TagIreland/Pulse.git
cd Pulse
git checkout -b feature/api-skeleton
# ... work ...
git add -A && git commit -m "add sessions endpoint" && git push -u origin HEAD
# then open a pull request and have someone from the other team approve it
```

Three rules, agreed now, held to for three days: nobody pushes to `main`, every change
goes through a pull request, and every pull request gets read by one person from the
other team.

### D1 — Get the API running, then make it yours

The project is already in `api/` — Spring Boot 4, Java 21, one endpoint returning a
hardcoded example. Open it in VSCode and run it.

```bash
cd api
./mvnw spring-boot:run
curl http://localhost:8080/api/sessions
```

Read the three files in `api/src/main/java/.../session/` before you change anything,
then add the endpoints you agreed. Copy the shape of the example one.

**Done when:** your own endpoints return the agreed JSON shapes from hardcoded objects,
and the other team has seen them.

**Hints:**
- Understand the layers before you fill them in: controller handles HTTP, service holds logic, repository talks to the database. Putting a SQL query in a controller works, and is the thing you will be asked to justify.
- Return objects, not strings. Let Spring turn them into JSON.
- A hardcoded response is not a shortcut — it is what lets the front end be built today instead of tomorrow.

### D1 — Get the dashboard running, then build a tile

The project is already in `web/`, with routing, one component, one service and chart.js
installed. Read the example tile before you add your own — it shows the four states every
tile needs, and you will copy that pattern three more times.

```bash
cd web
npm install
npm start                              # http://localhost:4200

# add your own as you go
ng generate component tiles/lap-times
ng generate service <name>
```

Fetch from your own endpoints through the service, and display the result in a component.
Do not hardcode data in the component — go through HTTP, because the seam is the point.

**Done when:** the Angular page shows data that came over HTTP from your own API.

**Hints:**
- You will hit CORS on your first request. It is the browser refusing a cross-origin call, and the fix is in the Spring API. Look up `@CrossOrigin` and understand what you are allowing before you allow everything.
- Read about services and dependency injection before you write the second component. Angular is built around it and fighting it is exhausting.
- Use a chart library rather than writing SVG. Pick one, do not spend an hour comparing three.

### D2 — Real data

Point Spring at the Supabase database and replace the hardcoded responses with real
queries against the data team's views. Then build out the remaining endpoints and the
dashboard: four tiles, one filter that changes at least two of them, and routing.

```properties
# api/src/main/resources/application.properties
# values from the data team, and from environment variables — never committed
spring.datasource.url=${DB_URL}
spring.datasource.username=${DB_USER}
spring.datasource.password=${DB_PASSWORD}
```

**Done when:** every tile shows real data, and the connection details are not in the repository.

**Hints:**
- Start with `JdbcTemplate` and plain SQL against the views. It is less to learn than JPA and it makes the data team's work visible.
- Never build SQL by concatenating strings, not even for a filter that "only comes from a dropdown". Use parameters, every time.
- Decide what an error looks like: one consistent JSON shape for every failure. Not a stack trace, and never a 200 with the word `error` inside it.
- Ask the data team for a view rather than writing a five-table join in Java. You will both be glad.

### D2 — GitHub Actions and deployment

The build workflow is already in `.github/workflows/build.yml`. Add a deploy step, then
deploy.

```bash
# one-time Vercel setup from inside web/
vercel link
vercel --prod
```

**Done when:** a red build blocks a pull request, and a public Vercel URL loads the
dashboard on somebody's phone.

**Hints:**
- The API base URL is different on Vercel than on your laptop. Use an Angular environment file, and set the value in the Vercel dashboard — not in your source.
- The Spring API only runs on your laptop unless you host it somewhere. That is fine for this sprint: present the deployed dashboard, and run the API locally during the demo.

### D3 — Finish and harden

- Read the ML prediction from Firebase and put it on the dashboard next to the real number.
- Handle the three states every tile has: loading, no data, and something went wrong. Stop the API and look at your own dashboard.
- Check it at phone width and make sure it can be navigated with a keyboard.

---

## Tasks — data team

### D1 — Explore OpenF1 and decide what you want

Open it in Postman and go looking. What endpoints exist, what does one record look like,
how much of it is there, how do you page through it, and what does it repeat needlessly?
Pick one race weekend and write down which endpoints you are going to pull and why.

**Done when:** you can name the endpoints you need, what one record represents, and
roughly how many records you are dealing with.

**Hints:**
- Save your working requests in a Postman collection and commit it. You will run them again.
- Confirm the terms of use and whether there are rate limits. It is a free service run by volunteers — be a good citizen, pull once, and work from your own copy.
- Be greedy about columns and modest about volume. One race weekend is plenty to build on.

### D1 — Get real data into Postgres

Create the Supabase project, then write a Python script that pulls from the API and loads
it into raw tables — one table per endpoint, columns as they arrive, no cleaning.

```bash
# .env (never committed)
DATABASE_URL=postgresql://postgres:<password>@<host>:5432/postgres

python fetch.py --endpoint laps --session 9472
```

```sql
-- then, in the Supabase SQL editor
select count(*), min(date), max(date) from raw_laps;
```

**Done when:** real rows are in Supabase and someone from the other team can run a count
against them.

**Hints:**
- Do not clean anything in the raw tables. Raw is what arrived, including the record with the broken character and the null you did not expect.
- `pandas.read_json` and `DataFrame.to_sql` will get you loaded in about ten lines. Understand what they did afterwards.
- Make the script safe to run twice. Reloading the same session should not double your row count — look up `ON CONFLICT`.
- The database password is a secret. It lives in `.env` and in GitHub Actions secrets, and nowhere else.

### D2 — Normalise it

Turn the repetitive raw tables into a proper relational model: one table per real-world
thing, a primary key on each, foreign keys between them, and no fact stored in two places.

```sql
-- the shape of it, not the answer
create table drivers  ( driver_number int primary key, full_name text not null, team text );
create table sessions ( session_key int primary key, name text, circuit text, started_at timestamptz );
create table laps     ( session_key int references sessions,
                        driver_number int references drivers,
                        lap_number int, lap_time_ms int, tyre_compound text,
                        primary key (session_key, driver_number, lap_number) );

-- then fill them from raw, one table at a time
insert into drivers
select distinct driver_number, driver_name, team from raw_laps;
```

**Done when:**
- Every table has a primary key, and the relationships are declared as foreign keys.
- No fact is stored twice. A driver's name appears in exactly one table.
- A row count on your normalised tables reconciles with the raw tables, and you can explain any difference.
- There is an index on the columns you filter by most.

**Hints:**
- Read about first, second and third normal form before you start — twenty minutes of reading will save two hours of restructuring.
- Do the reconciliation seriously. If raw has 1,247 laps and your laps table has 1,203, find the 44.
- Add the foreign keys and watch them reject rows. That rejection is the database telling you something true about your data.

### D2 — Write the views the API asks for

The development team needs one view per dashboard tile, returning exactly the columns they
agreed to. Everything awkward — the joins, the aggregation, the rounding, the unit
conversion — happens here, once, in SQL, rather than in Java.

```sql
create view v_driver_lap_summary as
select ... from laps l join drivers d on ... group by ...;
```

**Done when:** the other team can select from each view and get exactly the columns and
types they were promised.

**Hints:**
- Agree the units and the timezone explicitly. Milliseconds or seconds. UTC or local. This is the single most common cause of a dashboard that is confidently wrong.
- Decide what a missing value means. A null lap time is not a lap time of zero.
- If a view takes more than a second, look at what it is scanning before you look at anything else.

### D2 — One ML prediction, in Python, on the dashboard

Read from your normalised tables, fit something simple with scikit-learn, and publish the
result to Firestore where the Angular app can read it.

```python
from sklearn.linear_model import LinearRegression
# X = tyre age, compound, track temp    y = lap time

import firebase_admin
from firebase_admin import credentials, firestore
db = firestore.client()
db.collection('predictions').document('lap_time').set({
    'driver': 'VER', 'predicted_ms': 91340, 'actual_ms': 91502,
    'r2': 0.71, 'generated_at': '...'
})
```

**Done when:** a prediction document exists in Firestore, with the predicted value, the
real value beside it, and a number describing how good the model is.

**Hints:**
- Keep it small. A linear regression you can explain beats a model you cannot.
- Publish the actual value alongside the prediction. A prediction that cannot be checked is decoration.
- Split your data before you fit it, and report the score on the part the model never saw. Otherwise your model has simply memorised the answers.
- If the prediction is bad, publish it anyway and say why it is bad. That is a genuine finding.

### D3 — Make it trustworthy

- Write down, in the repo, which OpenF1 endpoints you used, what the terms of use are, when you pulled the data and what you know is wrong with it.
- Check three numbers on the finished dashboard against the source by hand. Actually do this. Dashboards are wrong far more often than anyone expects.
- Make sure the Python job can be run again by somebody else from a clean checkout.

---

## What finished looks like

- Four tiles on one screen, each answering a question a person would actually ask, one of them showing your ML prediction against reality.
- One filter that visibly changes at least two tiles.
- The dashboard on a public Vercel URL, working on a phone.
- The API reading real data from normalised tables through views.
- Every tile behaving properly when data is loading, missing, or broken.
- GitHub Actions building both applications on every push, and no passwords anywhere in the repository.
- A README a stranger could follow, and a page saying where the data came from.

---

## The presentation

Day 3 at 16:00. Ten minutes and five for questions, to a panel from both practices.
Live, from the deployed URL. Five slides at most — the product is the presentation, and
everybody speaks about their own work.

1. What it does and who would use it. Thirty seconds. Do not open with the architecture.
2. The demo. Someone answering a real question. Use the filter. Break something on purpose and show that it fails gracefully.
3. The database. Show the schema. Explain one normalisation decision you made and what it would have cost you to skip it.
4. The application. One slide on how the pieces fit, and what you would do differently.
5. The ML prediction. What it predicts, how well, and how you know.
6. One thing that went wrong, and one thing your AI assistant got wrong. Both are more interesting than the parts that worked.

**Before you present:** wake everything up thirty minutes beforehand — free-tier services
go to sleep and take longer to wake than you have. Rehearse twice, standing, from the
deployed URL rather than from localhost.

---

## Working with an AI assistant

Use it constantly — for scaffolding, for SQL you have not written before, for explaining
a stack trace, for the Angular syntax you cannot remember. That is how the job is done
now. Four rules come with it.

1. **You have to be able to explain any line in your work without it.** A facilitator may point at anything and ask why it is there. If nobody on the team can answer, it is not finished.
2. **Nothing sensitive goes into a prompt.** No client data, no internal material, no passwords or connection strings, ever, for any reason.
3. **Assume it is confidently wrong about something.** It will build SQL by string concatenation, use an inner join where you needed a left join and silently lose rows, and occasionally invent a method that does not exist. Check, do not skim.
4. **Once a day, close it for twenty minutes and write something by hand** — a join, a component, a stack trace read from top to bottom. Your ability to judge what it produces rests entirely on understanding what it is producing.

---

## Things that will bite you

- **CORS, on your first request from Angular.** The browser blocks the call, the terminal looks fine, and the error names none of the real causes. It is fixed in the API.
- **Timezones and units.** Store timestamps in UTC and convert once, at the edge. Decide milliseconds or seconds and write it down. This is the most common reason a dashboard is quietly wrong.
- **Secrets in the repository.** A database password pushed to GitHub is found by strangers within minutes. Use environment variables and Actions secrets. If it happens, tell a facilitator, rotate the password, then worry about the history.
- **Environment variables set on your laptop are not set in Vercel or in Actions.** This is behind most of the "but it works locally" hours you will lose.
- **Free tiers go to sleep, and public APIs rate-limit you.** Do not hammer the source from a build that runs on every push. Pull once, store it, and work from your own database.
- **Never force-push the branch everyone is working on.** Especially not twenty minutes before the presentation.
- **"It works" means it works for somebody else, from the deployed URL, without you in the room.** Until then it has merely not failed in front of you yet.

---

## Layout

```
api/     Spring Boot 4 / Java 21. One endpoint returning a hardcoded example.
         Run with ./mvnw spring-boot:run
web/     Angular. One component, one service, one tile, chart.js installed.
         Run with npm install && npm start
data/    Python. fetch.py pulls from OpenF1; predict.py is the Day 2 prediction.
         sql/ holds the schema you design.
         snapshot/ is the fallback extract if OpenF1 misbehaves.
.github/workflows/build.yml   builds all three on every push.
AGREEMENT.md   fill this in on Day 1 morning — the tiles, the tables, the endpoints.
DATA-NOTES.md  the data team fills this in as they go, not on Day 3.
```
