import { Routes } from '@angular/router';

import { AdminShellComponent } from './admin-shell.component';

export const ADMIN_ROUTES: Routes = [
  {
    path: '',
    component: AdminShellComponent,
    children: [
      {
        path: '',
        loadComponent: () =>
          import('../features/admin/dashboard/admin-dashboard-page.component').then(
            (module) => module.AdminDashboardPageComponent
          )
      }
    ]
  }
];
