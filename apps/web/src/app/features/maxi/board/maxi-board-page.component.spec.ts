import { TestBed } from '@angular/core/testing';

import { MaxiBoardPageComponent } from './maxi-board-page.component';

describe('MaxiBoardPageComponent', () => {
  it('renders the maxi-screen scaffold card', () => {
    const fixture = TestBed.configureTestingModule({
      imports: [MaxiBoardPageComponent]
    }).createComponent(MaxiBoardPageComponent);

    fixture.detectChanges();

    const host = fixture.nativeElement as HTMLElement;

    expect(host.textContent).toContain('Maxi-screen scaffold');
    expect(host.textContent).toContain('Live maxi-screen stream');
    expect(host.querySelectorAll('.placeholder-card')).toHaveLength(1);
  });
});
