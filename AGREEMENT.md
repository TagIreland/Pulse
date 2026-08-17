# The agreement

Fill this in together on Day 1 morning, before either team writes feature code.
Timebox it to thirty minutes. It is the only dependency between the two teams —
once it is written down, both sides can work without waiting for the other.

Raise it as a pull request titled `agreement v1`, have someone from each team
approve it, and merge it.

---

## 1. The four tiles

What four things does the dashboard show? Each one should answer a question a real
person would actually ask.

| # | Tile | The question it answers | Owner |
|---|------|-------------------------|-------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |

One of these should be the prediction tile — predicted against actual, side by side.

## 2. The filter

One filter that visibly changes at least two tiles.

- What is it (a session, a driver, a lap range, something else):
- Which tiles does it change:

## 3. The data we are pulling

Which OpenF1 endpoints, and how much.

| OpenF1 endpoint | Why we need it | Roughly how many rows |
|---|---|---|
| | | |

Race weekend / session we are working with: `________________`

## 4. The tables

What the database needs in order to answer the four questions above.

| Table | One row is… | Primary key |
|---|---|---|
| | | |

## 5. The endpoints

What the API is called and what it returns. Get the names and the shapes right now;
changing them later means changing code in two places.

| Method | Path | Returns | Feeds tile |
|--------|------|---------|-----------|
| GET | `/api/sessions` | list of `{sessionKey, sessionName, circuit, country, year}` | example |
| | | | |

### Conventions — agree these now, they cause the worst bugs later

- Timestamps: stored in **UTC**, converted in the front end only. (Change if you disagree, but write down what you chose.)
- Lap and sector times in: `milliseconds` / `seconds` — **pick one** ______
- A missing value means: ______________________ (it does **not** mean zero)
- Empty result: the API returns `[]` with a 200, not a 404.
- Errors: every failure returns the same JSON shape ______________________

## 6. Changing this document

Either team may propose a change, as a pull request, reviewed by the other. Talk for
five minutes before you write any code. No changes on Day 3.
