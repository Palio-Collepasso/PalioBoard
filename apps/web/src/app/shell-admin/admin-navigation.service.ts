import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { AppPaths } from '../core/navigation/app-paths';
import { AdminPaths } from './admin-paths';
import { navigateSafely } from '../core/navigation/safe-navigation';

@Injectable({ providedIn: 'root' })
export class AdminNavigationService {
  constructor(private readonly router: Router) {}

  goToAdminShell(): Promise<void> {
    return this.navigateTo(AdminPaths.root);
  }

  goToPublicShell(): Promise<void> {
    return this.navigateTo(AppPaths.public);
  }

  goToMaxiShell(): Promise<void> {
    return this.navigateTo(AppPaths.maxi);
  }

  private navigateTo(path: string): Promise<void> {
    return navigateSafely(this.router, path);
  }
}
