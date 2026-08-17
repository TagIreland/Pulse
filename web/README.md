# web — the Angular dashboard

```bash
npm install
npm start           # http://localhost:4200
npm run build       # production build, which is what Vercel runs
```

## Where things are

```
src/app/api.service.ts               every HTTP call goes through here
src/app/dashboard/                   the example tile, with its four states
src/app/app.routes.ts                routing
src/environments/environment.ts      the API address in development
src/environments/environment.prod.ts the API address in the production build — read it
```

## Deploying

```bash
npm install -g vercel
vercel link
vercel --prod
```

Vercel needs to know this is an Angular build. It usually detects it; if not, the
build command is `npm run build` and the output directory is `dist/pulse-web/browser`.

`vercel --prod` from your laptop is fine for the sprint. Wiring the deploy into
GitHub Actions instead, so a merge to `main` ships it, is the better answer and is
the stretch goal.

## Two things that will cost you an hour if nobody says them

1. **The browser will block your first API call.** That is CORS, and it is fixed in
   the Spring API, not here.
2. **An Observable does nothing until you subscribe.** If your request "never fires",
   this is why.
