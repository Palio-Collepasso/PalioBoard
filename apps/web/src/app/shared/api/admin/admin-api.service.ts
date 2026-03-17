import { Injectable } from '@angular/core';

import type { ScaffoldCard } from '../../types/scaffold-card';
import { joinUrlSegments } from '../../utils/join-url-segments';

@Injectable({ providedIn: 'root' })
export class AdminApiService {
  readonly basePath = joinUrlSegments('/api', 'admin');

  describeSurface(): readonly ScaffoldCard[] {
    return [
      {
        title: 'Operational workspace',
        description: 'Private command/query surface for judges and admins, ready for feature-local state and authenticated flows.',
        endpoint: joinUrlSegments(this.basePath, 'season-setup'),
        bullets: [
          'Shell is lazy-loaded from the root SPA router.',
          'Feature code stays under features/admin and does not depend on other shells.',
          'Auth remains bearer-token based when Supabase wiring lands.'
        ],
        surface: 'admin'
      },
      {
        title: 'Review and audit entrypoints',
        description: 'Placeholder surface for post-completion review, audit views, and future operator tooling.',
        endpoint: joinUrlSegments(this.basePath, 'audit'),
        bullets: [
          'No global store is introduced in the scaffold.',
          'Shared UI stays generic and import-safe.',
          'Api ownership remains in Python only.'
        ],
        surface: 'admin'
      }
    ];
  }
}
