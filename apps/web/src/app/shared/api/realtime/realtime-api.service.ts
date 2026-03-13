import { Injectable } from '@angular/core';

import type { ScaffoldCard } from '../../types/scaffold-card';
import { joinUrlSegments } from '../../utils/join-url-segments';

@Injectable({ providedIn: 'root' })
export class RealtimeApiService {
  readonly basePath = joinUrlSegments('/realtime');

  describeSurface(): readonly ScaffoldCard[] {
    return [
      {
        title: 'Live maxi-screen stream',
        description: 'Placeholder realtime surface for projector-oriented updates without introducing a global client event bus.',
        endpoint: joinUrlSegments(this.basePath, 'maxi', 'stream'),
        bullets: [
          'Realtime handling will stay feature-scoped.',
          'Maxi-screen remains a public route in v1.',
          'Advanced live rotation is explicitly deferred beyond v1.'
        ],
        surface: 'maxi'
      }
    ];
  }
}
