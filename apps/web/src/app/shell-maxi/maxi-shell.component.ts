import { NgFor } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { MaxiNavigationService } from './maxi-navigation.service';

@Component({
  selector: 'palio-maxi-shell',
  standalone: true,
  imports: [NgFor, RouterOutlet],
  template: `
    <section class="shell shell-maxi">
      <header class="shell__hero">
        <div>
          <p class="eyebrow">Maxi-screen shell</p>
          <h1>Presentation route scaffold</h1>
          <p>Projector-oriented routing is isolated from admin chrome and ready for later realtime presentation work.</p>
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
export class MaxiShellComponent {
  readonly shellLinks = [
    { label: 'Admin', navigate: () => this.navigation.goToAdminShell() },
    { label: 'Public', navigate: () => this.navigation.goToPublicShell() }
  ] as const;

  constructor(private readonly navigation: MaxiNavigationService) {}
}
