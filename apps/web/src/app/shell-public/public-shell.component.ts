import { NgFor } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { PublicNavigationService } from './public-navigation.service';

@Component({
  selector: 'palio-public-shell',
  standalone: true,
  imports: [NgFor, RouterOutlet],
  template: `
    <section class="shell shell-public">
      <header class="shell__hero">
        <div>
          <p class="eyebrow">Public shell</p>
          <h1>Read-only public scaffold</h1>
          <p>Anonymous routes reserve space for Palio, Prepalio, and Giocasport views without pulling admin code.</p>
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
export class PublicShellComponent {
  readonly shellLinks = [
    { label: 'Admin', navigate: () => this.navigation.goToAdminShell() },
    { label: 'Maxi-screen', navigate: () => this.navigation.goToMaxiShell() }
  ] as const;

  constructor(private readonly navigation: PublicNavigationService) {}
}
