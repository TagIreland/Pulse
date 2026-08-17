import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../environments/environment';

/**
 * These types have to match AGREEMENT.md, which in turn matches what the Java
 * record sends. If the three ever disagree, the agreement is right and the code is
 * wrong.
 */
export interface Session {
  sessionKey: number;
  sessionName: string;
  circuit: string;
  country: string;
  year: number;
}

/**
 * Every HTTP call the dashboard makes goes through here.
 *
 * Components should not know the API's address, and they should not build URLs. Keep
 * that in one place and changing it later is one edit instead of nine.
 */
@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly base = environment.apiBaseUrl;

  getSessions(): Observable<Session[]> {
    return this.http.get<Session[]>(`${this.base}/api/sessions`);
  }

  // TODO one method per endpoint in AGREEMENT.md.
  //
  // Worth reading before you add the second one: Angular's HttpClient returns an
  // Observable, not a Promise. It does nothing at all until something subscribes,
  // which is the single most common reason a new joiner's request "never fires".
}
