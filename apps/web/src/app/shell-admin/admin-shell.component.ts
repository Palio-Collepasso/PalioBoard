import { NgFor } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

import { SHELL_LINKS } from '../core/navigation/shell-links';

@Component({
  selector: 'palio-admin-shell',
  standalone: true,
  imports: [NgFor, RouterLink, RouterOutlet],
  template: `
    <section class="shell shell-admin">
      <header class="shell__hero">
        <div>
          <p class="eyebrow">Admin shell</p>
          <h1>Operational UI scaffold</h1>
          <p>Private judge and admin routes stay separate from the public and maxi-screen areas.</p>
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
export class AdminShellComponent {
  readonly shellLinks = SHELL_LINKS.filter((link) => link.surface !== 'admin');
}
