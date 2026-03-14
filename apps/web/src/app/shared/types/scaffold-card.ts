export type ShellSurface = 'admin' | 'public' | 'maxi';

export interface ScaffoldCard {
  readonly title: string;
  readonly description: string;
  readonly endpoint: string;
  readonly bullets: readonly string[];
  readonly surface: ShellSurface;
}
