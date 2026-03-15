import { TestBed } from '@angular/core/testing';

import { AdminDashboardPageComponent } from './admin-dashboard-page.component';

describe('AdminDashboardPageComponent', () => {
  it('renders the admin scaffold cards', () => {
    const fixture = TestBed.configureTestingModule({
      imports: [AdminDashboardPageComponent]
    }).createComponent(AdminDashboardPageComponent);

    fixture.detectChanges();

    const host = fixture.nativeElement as HTMLElement;

    expect(host.textContent).toContain('Admin scaffold');
    expect(host.textContent).toContain('Operational workspace');
    expect(host.textContent).toContain('Review and audit entrypoints');
    expect(host.querySelectorAll('.placeholder-card')).toHaveLength(2);
  });
});
