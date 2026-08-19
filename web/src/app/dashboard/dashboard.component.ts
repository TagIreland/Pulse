import { Component, OnInit, inject, ChangeDetectionStrategy } from '@angular/core';

import { ApiService, Session } from '../api.service';
import { environment } from '../../environments/environment';

type TileState = 'loading' | 'ready' | 'empty' | 'error';

/**
 * The example tile. Copy this pattern for the other three.
 *
 * The part worth copying is not the table — it is the four states. Every tile that
 * reads from a network has them, and the difference between a product and a demo is
 * whether somebody thought about the three that are not "ready".
 */
@Component({
  selector: 'app-dashboard',
  changeDetection: ChangeDetectionStrategy.Eager,
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent implements OnInit {
  private readonly api = inject(ApiService);

  readonly apiBaseUrl = environment.apiBaseUrl;

  sessions: Session[] = [];
  state: TileState = 'loading';

  ngOnInit(): void {
    this.api.getSessions().subscribe({
      next: (sessions) => {
        this.sessions = sessions;
        this.state = sessions.length > 0 ? 'ready' : 'empty';
      },
      error: (err) => {
        // Look in the browser console, not just at the screen. On Day 1 this will
        // almost certainly be CORS, and the fix is in the Spring API.
        console.error('GET /api/sessions failed', err);
        this.state = 'error';
      },
    });
  }
}
