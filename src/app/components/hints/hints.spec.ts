import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Hints } from './hints';

describe('Hints', () => {
  let component: Hints;
  let fixture: ComponentFixture<Hints>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Hints]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Hints);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
