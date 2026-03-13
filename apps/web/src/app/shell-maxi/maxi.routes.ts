import { Routes } from '@angular/router';

import { MaxiShellComponent } from './maxi-shell.component';

export const MAXI_ROUTES: Routes = [
  {
    path: '',
    component: MaxiShellComponent,
    children: [
      {
        path: '',
        loadComponent: () =>
          import('../features/maxi/board/maxi-board-page.component').then(
            (module) => module.MaxiBoardPageComponent
          )
      }
    ]
  }
];
