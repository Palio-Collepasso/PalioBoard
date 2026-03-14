import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { AppPaths } from '../core/navigation/app-paths';
import { PublicPaths } from './public-paths';
import { navigateSafely } from '../core/navigation/safe-navigation';

@Injectable({ providedIn: 'root' })
export class PublicNavigationService {
  constructor(private readonly router: Router) {}

  goToPublicShell(): Promise<void> {
    return this.navigateTo(PublicPaths.root);
  }

  goToAdminShell(): Promise<void> {
    return this.navigateTo(AppPaths.admin);
  }

  goToMaxiShell(): Promise<void> {
    return this.navigateTo(AppPaths.maxi);
  }

  private navigateTo(path: string): Promise<void> {
    return navigateSafely(this.router, path);
  }
}
