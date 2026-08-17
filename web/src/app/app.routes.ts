import { Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },

  // TODO: add a route per page. If a tile deserves its own page, give it one —
  // and think about whether the filter state should live in the URL, so the client
  // can send somebody a link to what they are looking at.

  { path: '**', redirectTo: '' },
];
