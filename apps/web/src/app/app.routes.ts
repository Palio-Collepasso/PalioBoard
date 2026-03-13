import { Routes } from '@angular/router';

export const appRoutes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'public'
  },
  {
    path: 'admin',
    loadChildren: () => import('./shell-admin/admin.routes').then((module) => module.ADMIN_ROUTES)
  },
  {
    path: 'public',
    loadChildren: () => import('./shell-public/public.routes').then((module) => module.PUBLIC_ROUTES)
  },
  {
    path: 'maxi',
    loadChildren: () => import('./shell-maxi/maxi.routes').then((module) => module.MAXI_ROUTES)
  },
  {
    path: '**',
    redirectTo: 'public'
  }
];
