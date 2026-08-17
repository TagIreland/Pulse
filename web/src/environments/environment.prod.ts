// Used by `ng build` (the production configuration), which is what Vercel runs.
// angular.json swaps this file in for environment.ts at build time — look up
// "fileReplacements" if you want to see how.
//
// Why this still points at localhost:
//
// The Spring API is not deployed during this sprint. The JavaScript in this page runs
// in the browser of whoever is looking at it — so when you demo the deployed dashboard
// from your own laptop with the API running, "localhost:8080" is your laptop, and it
// works. Browsers make a deliberate exception for http://localhost so an HTTPS page is
// allowed to call it.
//
// Two consequences worth understanding rather than discovering:
//   1. It only works for whoever has the API running. Anyone else sees your error state.
//      That is a real limitation and worth saying out loud at the presentation.
//   2. CORS is per origin, so once the dashboard is on a Vercel URL, that URL has to be
//      allowed by the API as well as localhost:4200.
//
// If you get ahead of schedule, host the API somewhere and put its address here instead.
export const environment = {
  apiBaseUrl: 'http://localhost:8080',
};
