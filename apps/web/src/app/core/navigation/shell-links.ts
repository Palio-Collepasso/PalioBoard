import type { ShellSurface } from '../../shared/types/scaffold-card';

export interface ShellLink {
  readonly label: string;
  readonly path: string;
  readonly surface: ShellSurface;
}

export const SHELL_LINKS: readonly ShellLink[] = [
  { label: 'Admin', path: '/admin', surface: 'admin' },
  { label: 'Public', path: '/public', surface: 'public' },
  { label: 'Maxi-screen', path: '/maxi', surface: 'maxi' }
];
