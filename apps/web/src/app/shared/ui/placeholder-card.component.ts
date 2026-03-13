import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { NgFor } from '@angular/common';

import type { ScaffoldCard } from '../types/scaffold-card';

@Component({
  selector: 'palio-placeholder-card',
  standalone: true,
  imports: [NgFor],
  template: `
    <article class="placeholder-card" [attr.data-surface]="card.surface">
      <span class="placeholder-card__surface">{{ card.surface }}</span>
      <div>
        <h3>{{ card.title }}</h3>
        <p>{{ card.description }}</p>
      </div>
      <p><code>{{ card.endpoint }}</code></p>
      <ul>
        <li *ngFor="let bullet of card.bullets">{{ bullet }}</li>
      </ul>
    </article>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlaceholderCardComponent {
  @Input({ required: true }) card!: ScaffoldCard;
}
