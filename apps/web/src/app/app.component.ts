import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'palio-root',
  standalone: true,
  imports: [RouterOutlet],
  template: '<main class="app-shell"><router-outlet /></main>',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppComponent {}
