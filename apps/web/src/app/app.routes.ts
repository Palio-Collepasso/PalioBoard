import { Routes } from '@angular/router';

import { AdminPaths } from './shell-admin/admin-paths';
import { MaxiPaths } from './shell-maxi/maxi-paths';
import { PublicPaths } from './shell-public/public-paths';

export const appRoutes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: PublicPaths.root
  },
  {
    path: AdminPaths.root,
    loadChildren: () => import('./shell-admin/admin.routes').then((module) => module.ADMIN_ROUTES)
  },
  {
    path: PublicPaths.root,
    loadChildren: () => import('./shell-public/public.routes').then((module) => module.PUBLIC_ROUTES)
  },
  {
    path: MaxiPaths.root,
    loadChildren: () => import('./shell-maxi/maxi.routes').then((module) => module.MAXI_ROUTES)
  },
  {
    path: '**',
    redirectTo: PublicPaths.root
  }
];
