import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { AppPaths } from '../core/navigation/app-paths';
import { MaxiPaths } from './maxi-paths';
import { navigateSafely } from '../core/navigation/safe-navigation';

@Injectable({ providedIn: 'root' })
export class MaxiNavigationService {
  constructor(private readonly router: Router) {}

  goToMaxiShell(): Promise<void> {
    return this.navigateTo(MaxiPaths.root);
  }

  goToAdminShell(): Promise<void> {
    return this.navigateTo(AppPaths.admin);
  }

  goToPublicShell(): Promise<void> {
    return this.navigateTo(AppPaths.public);
  }

  private navigateTo(path: string): Promise<void> {
    return navigateSafely(this.router, path);
  }
}
