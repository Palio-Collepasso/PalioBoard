import { NgFor } from '@angular/common';
import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';

import { PublicApiService } from '../../../shared/api/public/public-api.service';
import { PlaceholderCardComponent } from '../../../shared/ui/placeholder-card.component';

@Component({
  selector: 'palio-public-home-page',
  standalone: true,
  imports: [NgFor, PlaceholderCardComponent],
  template: `
    <section>
      <p class="eyebrow">Public read shell</p>
      <h2>Public scaffold</h2>
      <p>Anonymous routes are split from admin concerns and reserve distinct competition sections.</p>
      <div class="card-grid">
        <palio-placeholder-card *ngFor="let card of cards()" [card]="card" />
      </div>
    </section>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PublicHomePageComponent {
  private readonly publicApi = inject(PublicApiService);

  readonly cards = signal(this.publicApi.describeSurface());
}
