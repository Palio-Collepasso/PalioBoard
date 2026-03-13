import { NgFor } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

import { SHELL_LINKS } from '../core/navigation/shell-links';

@Component({
  selector: 'palio-public-shell',
  standalone: true,
  imports: [NgFor, RouterLink, RouterOutlet],
  template: `
    <section class="shell shell-public">
      <header class="shell__hero">
        <div>
          <p class="eyebrow">Public shell</p>
          <h1>Read-only public scaffold</h1>
          <p>Anonymous routes reserve space for Palio, Prepalio, and Giocasport views without pulling admin code.</p>
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
export class PublicShellComponent {
  readonly shellLinks = SHELL_LINKS.filter((link) => link.surface !== 'public');
}
