import { Injectable } from '@angular/core';

import type { ScaffoldCard } from '../../types/scaffold-card';
import { joinUrlSegments } from '../../utils/join-url-segments';

@Injectable({ providedIn: 'root' })
export class PublicApiService {
  readonly basePath = joinUrlSegments('/api', 'public');

  describeSurface(): readonly ScaffoldCard[] {
    return [
      {
        title: 'Palio standings',
        description: 'Public read-only section placeholder for the main competition leaderboard and official result history.',
        endpoint: joinUrlSegments(this.basePath, 'palio', 'standings'),
        bullets: [
          'Anonymous route area under /public.',
          'Immediate visibility remains a backend/public-read concern.',
          'Projection-backed screens land in later slices.'
        ],
        surface: 'public'
      },
      {
        title: 'Prepalio and Giocasport',
        description: 'Separate public sections are reserved so the SPA does not collapse all competitions into one mixed landing page.',
        endpoint: joinUrlSegments(this.basePath, 'competitions'),
        bullets: [
          'Palio, Prepalio, and Giocasport remain distinct user-facing sections.',
          'Public notes stay visible by product rule.',
          'No auth requirement exists for this shell.'
        ],
        surface: 'public'
      }
    ];
  }
}
