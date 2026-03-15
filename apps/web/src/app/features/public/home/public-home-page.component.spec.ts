import { TestBed } from '@angular/core/testing';

import { PublicHomePageComponent } from './public-home-page.component';

describe('PublicHomePageComponent', () => {
  it('renders the public scaffold cards', () => {
    const fixture = TestBed.configureTestingModule({
      imports: [PublicHomePageComponent]
    }).createComponent(PublicHomePageComponent);

    fixture.detectChanges();

    const host = fixture.nativeElement as HTMLElement;

    expect(host.textContent).toContain('Public scaffold');
    expect(host.textContent).toContain('Palio standings');
    expect(host.textContent).toContain('Prepalio and Giocasport');
    expect(host.querySelectorAll('.placeholder-card')).toHaveLength(2);
  });
});
