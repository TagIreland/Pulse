# snapshot

A frozen extract of one race weekend, committed so that a slow, rate-limited or
offline OpenF1 does not cost anyone the sprint.

Your facilitator should have put CSVs here before the sprint started. If the folder is
empty and the API is misbehaving, ask them for it rather than losing an hour.

Load one like this:

```bash
psql "$DATABASE_URL" -c "\copy raw_laps from 'snapshot/laps.csv' with (format csv, header true)"
```

Note there is deliberately no `car_data` snapshot. It is sampled several times a second
for every car, so one race is millions of rows.
