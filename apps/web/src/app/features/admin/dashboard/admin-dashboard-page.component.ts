import { NgFor } from '@angular/common';
import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';

import { AdminApiService } from '../../../shared/api/admin/admin-api.service';
import { PlaceholderCardComponent } from '../../../shared/ui/placeholder-card.component';

@Component({
  selector: 'palio-admin-dashboard-page',
  standalone: true,
  imports: [NgFor, PlaceholderCardComponent],
  template: `
    <section>
      <p class="eyebrow">Feature-local state</p>
      <h2>Admin scaffold</h2>
      <p>The admin shell is isolated, lazy-loaded, and ready for authenticated feature slices.</p>
      <div class="card-grid">
        <palio-placeholder-card *ngFor="let card of cards()" [card]="card" />
      </div>
    </section>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AdminDashboardPageComponent {
  private readonly adminApi = inject(AdminApiService);

  readonly cards = signal(this.adminApi.describeSurface());
}
