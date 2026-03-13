import { NgFor } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

import { SHELL_LINKS } from '../core/navigation/shell-links';

@Component({
  selector: 'palio-maxi-shell',
  standalone: true,
  imports: [NgFor, RouterLink, RouterOutlet],
  template: `
    <section class="shell shell-maxi">
      <header class="shell__hero">
        <div>
          <p class="eyebrow">Maxi-screen shell</p>
          <h1>Presentation route scaffold</h1>
          <p>Projector-oriented routing is isolated from admin chrome and ready for later realtime presentation work.</p>
        </div>
        <nav class="shell__nav" aria-label="Shell navigation">
          <a *ngFor="let link of shellLinks" [routerLink]="link.path">{{ link.label }}</a>
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
  readonly shellLinks = SHELL_LINKS.filter((link) => link.surface !== 'maxi');
}
