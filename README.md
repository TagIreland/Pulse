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
| Node | 22 or newer | `node -v` |
| Python | 3.11 or newer | `python --version` |

The development team also needs IntelliJ IDEA (Community is fine) and the Angular CLI
(`npm install -g @angular/cli`). Both teams want Postman. Nobody needs to install
Postgres — the database is hosted on Supabase.

---

## Installing on a new Accenture laptop

These are the first steps on a machine that has nothing on it yet. Run PowerShell as a
normal user throughout — you do not need admin, and the installs below do not require it.

### 1. Check what Software Center already has

Open **Software Center** (search in the Start menu). Some cohorts get Git and Python
pre-approved; if yours does, install from there first rather than bypassing the managed
channel.

### 2. Install the tools via winget

Open PowerShell and run the following. Each line is independent — if one fails, skip it
and note it; the tools are available through other routes.

```powershell
# Git
winget install --id Git.Git -e

# Java 21 (Eclipse Temurin LTS)
winget install --id EclipseAdoptium.Temurin.21.JDK -e

# Node.js 22 LTS
winget install --id OpenJS.NodeJS.22 -e

# Python 3.12
winget install --id Python.Python.3.12 -e

# IntelliJ IDEA Community (dev team only)
winget install --id JetBrains.IntelliJIDEA.Community -e

# Postman
winget install --id Postman.Postman -e
```

After each install, **close and reopen PowerShell** before testing. winget writes to
`PATH` but the running shell does not pick it up until restarted.

Verify:

```powershell
git --version
java -version          # must say version 21
node -v                # must say v22.x.x or higher
python --version       # must say 3.12.x
```

> **If winget is not available:** it ships with Windows 11 but some managed images
> remove it. In that case raise a ticket with IT to install the above tools, or ask your
> facilitator — a pre-imaged USB is the backup.

### 3. Configure Git

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.name@accenture.com"
```

Then authenticate to GitHub. The easiest way on a managed laptop is a personal access
token (classic, `repo` scope):

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
2. Copy the token. When Git first asks for a password, paste it.
3. Windows Credential Manager will save it so you are not asked again.

### 4. Clone and run

```powershell
git clone https://github.com/TagIreland/Pulse.git
cd Pulse
```

Then follow the **Running the three pieces** section below.

### 5. Accenture network notes

**TLS interception.** Forcepoint One Endpoint re-signs outbound HTTPS. Windows and most
tools trust it automatically. Two tools that do not:

- **Python** — see the certificate error section in `data/README.md`.
- **npm** — if `npm install` fails with `SELF_SIGNED_CERT_IN_CHAIN`, run this once:

  ```powershell
  # Export Forcepoint's root cert from the Windows store as PEM
  $cert = Get-ChildItem Cert:\LocalMachine\Root |
      Where-Object { $_.Subject -match 'Forcepoint' } |
      Select-Object -First 1
  [IO.File]::WriteAllText("$HOME\corp-ca.pem",
      "-----BEGIN CERTIFICATE-----`n" +
      [Convert]::ToBase64String($cert.RawData, 'InsertLineBreaks') +
      "`n-----END CERTIFICATE-----`n")
  npm config set cafile "$HOME\corp-ca.pem"
  ```

  If you cannot find a Forcepoint cert by that name, export whichever root cert is
  present that is not a standard public CA — your facilitator can confirm which one.

**Proxy.** If you are on the corporate VPN or a wired office connection and a tool
cannot reach the internet at all, set the proxy. The address varies by site; ask IT
or check Internet Options → LAN settings:

```powershell
$proxy = "http://proxy.accenture.com:8080"    # replace with your site's address
$env:HTTP_PROXY  = $proxy
$env:HTTPS_PROXY = $proxy
npm config set proxy $proxy
npm config set https-proxy $proxy
```

Add these to your PowerShell profile (`$PROFILE`) if you want them across all sessions.

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
api/     Spring Boot 4 / Java 21. One endpoint returning a hardcoded example.
web/     Angular. One component, one service, one tile, chart.js installed.
data/    Python. fetch.py pulls from OpenF1; predict.py is the Day 2 prediction.
         sql/ holds the schema you design.
.github/workflows/build.yml   builds all three on every push.
AGREEMENT.md   fill this in on Day 1 morning. It is the contract between the teams.
DATA-NOTES.md  the data team fills this in as they go.
```
