import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withXhr } from '@angular/common/http';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    // Without this, anything that injects HttpClient fails at runtime with an
    // error that does not obviously say so.
    provideHttpClient(withXhr()),
  ],
};
