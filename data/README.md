# data — the pipeline and the model

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then fill it in. Never commit it.

python fetch.py --endpoint sessions --year 2024 --dry-run
```

## What is here

```
fetch.py            pulls from OpenF1 into raw_<endpoint> tables
predict.py          Day 2: fit a model, publish the result to Firebase
sql/01_normalised.sql   the schema you design. One worked table, then TODOs
sql/02_views.sql        one view per dashboard tile. The API reads only these
snapshot/           the fallback extract, if OpenF1 misbehaves
```

## The order of work

1. **Explore first.** Use Postman, or `--dry-run`, and look at what one record
   actually contains before you design anything.
2. **Land it raw.** One table per endpoint, columns exactly as they arrived, nothing
   cleaned. Raw is the evidence that you did not invent anything.
3. **Normalise.** `sql/01_normalised.sql`. This is the part that matters.
4. **Publish views.** `sql/02_views.sql`. This is the other team's contract with you.
5. **Predict.** `predict.py`, and publish the result to Firebase.

Get to step 2 on Day 1. Once the data is in your own database you are not dependent on
the API being up, and you are not hammering a free public service from a build that
runs on every push.

## Supabase notes

- Use the **connection pooler** host in `DATABASE_URL`, not the direct one.
- The SQL editor in the Supabase dashboard is the fastest way to iterate. Paste the
  statements you settle on back into the `sql/` files, so the schema lives in Git
  rather than in somebody's browser history.
- A free project pauses after a period of inactivity. Wake it before the presentation.
