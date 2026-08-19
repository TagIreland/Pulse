# Facilitator setup — do this before you push

This project was written without a network connection, so **it has never been built.**
Two of the steps below are not optional: without them the new joiners hit a broken
repository in their first hour, which is the one thing this starter is meant to prevent.

Budget an hour.

---

## 1. Generate the Maven wrapper  — REQUIRED

The brief promises new joiners do not need to install Maven. That is only true if the
wrapper is committed. You need Maven installed once, to create it:

```bash
cd api
mvn -N wrapper:wrapper
git add mvnw mvnw.cmd .mvn && git commit -m "add maven wrapper"
```

Then confirm the new joiner path works:

```bash
./mvnw spring-boot:run
curl http://localhost:8080/api/sessions
```

## 2. Install and build the front end  — REQUIRED

```bash
cd web
npm install
npm start          # check http://localhost:4200 loads, and that the tile renders
                   # and reports a CORS error
npm run build      # check the production build passes
git add package-lock.json && git commit -m "add lockfile"
```

The CORS error is the correct result, not a fault you should fix here.
`WebConfig.addCorsMappings` in the API is deliberately empty — making that call succeed
is the joiners' Day 1 exercise, and if you fix it now and commit, you have removed the
exercise. What you are checking is that the tile renders, reaches the API, and fails for
the one reason you expect.

To see it properly, start the API in another terminal first (`cd api && ./mvnw
spring-boot:run`). A `200` on `curl http://localhost:8080/api/sessions` with no
`Access-Control-Allow-Origin` header in the response is exactly right: the API is
healthy and the browser is the thing refusing. If the tile instead reports that it
cannot reach the API at all, that is a real failure — check the API is up on 8080 and
that `apiBaseUrl` in `web/src/environments/environment.ts` still points at it.

Committing `package-lock.json` matters: without it every new joiner resolves slightly
different dependency versions, and you will spend Wednesday afternoon on it.

## 3. Consider bumping the versions

`web/package.json` pins Angular 19 and `api/pom.xml` pins Spring Boot 3.4. Both work,
and both may be a release or two behind by the time you run this. If you are bumping:

```bash
cd web && ng update @angular/core @angular/cli
```

The Angular code here uses standalone components, `provideRouter`, `provideHttpClient`
and the built-in `@if` / `@for` control flow, all of which have been stable for several
major versions — so the upgrade is usually clean. Change the Spring Boot parent version
in `pom.xml` and rebuild.

> Whoever owns the version floor: no pinned version should be older than the current
> long-term-support release minus one. The reason the old pack still teaches Angular
> 8.3.9 is that nobody owned that number.

## 4. Check the Python side

```bash
cd data
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python fetch.py --endpoint sessions --year 2024 --dry-run
```

**Verify the OpenF1 endpoint names and parameters against the current documentation at
openf1.org.** `fetch.py` assumes `https://api.openf1.org/v1/<endpoint>` with
`session_key` and `year` as filters. If that has changed, fix `fetch.py` and the two
`curl` examples in the brief before the sprint, not during it.

## 5. Take the fallback snapshot  — REQUIRED

All three sprint documents promise a snapshot to fall back on if OpenF1 is slow, rate
limiting, or down on the day. Pull one race weekend now and drop the CSVs into
`data/snapshot/`:

```bash
cd data
python fetch.py --endpoint sessions --year 2024        # find a session_key
python fetch.py --endpoint drivers --session <key> --to-csv snapshot/drivers.csv
python fetch.py --endpoint laps    --session <key> --to-csv snapshot/laps.csv
python fetch.py --endpoint stints  --session <key> --to-csv snapshot/stints.csv
python fetch.py --endpoint pit     --session <key> --to-csv snapshot/pit.csv
python fetch.py --endpoint weather --session <key> --to-csv snapshot/weather.csv
```

Do **not** snapshot `car_data`. It is sampled several times a second per car and one
race is millions of rows.

## 6. Reference branches

Work the sprint through yourself, and leave the result on two branches:

- `day1-done` — API and dashboard running and connected with hardcoded data; real data
  in raw tables.
- `day2-done` — normalised tables, views, the API reading them, the dashboard deployed,
  the prediction in Firebase.

A team that loses a morning to something environmental can pull a branch and stay in
the sprint. You can also see instantly who did.

## 7. First push

```bash
git remote add origin git@github.com:<your-org>/pulse.git
git push -u origin main
```

Then, on GitHub: protect `main` (require a pull request and one approving review), and
check the Actions run is green. Add the new joiners with write access, not admin.

## 8. Delete this file

It is for you, not for them.
