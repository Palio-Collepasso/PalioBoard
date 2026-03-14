import { Router } from '@angular/router';

export async function navigateSafely(router: Router, path: string): Promise<void> {
  try {
    const didNavigate = await router.navigate([path]);
    if (!didNavigate) {
      console.error(`Navigation cancelled for path: ${path}`);
    }
  } catch (error) {
    console.error(`Navigation failed for path: ${path}`, error);
  }
}
