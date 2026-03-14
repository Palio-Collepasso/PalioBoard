import { NgFor } from '@angular/common';
import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';

import { RealtimeApiService } from '../../../shared/api/realtime/realtime-api.service';
import { PlaceholderCardComponent } from '../../../shared/ui/placeholder-card.component';

@Component({
  selector: 'palio-maxi-board-page',
  standalone: true,
  imports: [NgFor, PlaceholderCardComponent],
  template: `
    <section>
      <p class="eyebrow">Projector route</p>
      <h2>Maxi-screen scaffold</h2>
      <p>The maxi shell stays public, lazy-loaded, and ready for later SSE-driven projection updates.</p>
      <div class="card-grid">
        <palio-placeholder-card *ngFor="let card of cards()" [card]="card" />
      </div>
    </section>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MaxiBoardPageComponent {
  private readonly realtimeApi = inject(RealtimeApiService);

  readonly cards = signal(this.realtimeApi.describeSurface());
}
