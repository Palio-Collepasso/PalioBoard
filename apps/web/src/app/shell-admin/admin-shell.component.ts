import { NgFor } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { AdminNavigationService } from './admin-navigation.service';

@Component({
  selector: 'palio-admin-shell',
  standalone: true,
  imports: [NgFor, RouterOutlet],
  template: `
    <section class="shell shell-admin">
      <header class="shell__hero">
        <div>
          <p class="eyebrow">Admin shell</p>
          <h1>Operational UI scaffold</h1>
          <p>Private judge and admin routes stay separate from the public and maxi-screen areas.</p>
        </div>
        <nav class="shell__nav" aria-label="Shell navigation">
          <button type="button" *ngFor="let link of shellLinks" (click)="link.navigate()">{{ link.label }}</button>
        </nav>
      </header>
      <section class="shell__content">
        <router-outlet />
      </section>
    </section>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AdminShellComponent {
  readonly shellLinks = [
    { label: 'Public', navigate: () => this.navigation.goToPublicShell() },
    { label: 'Maxi-screen', navigate: () => this.navigation.goToMaxiShell() }
  ] as const;

  constructor(private readonly navigation: AdminNavigationService) {}
}
