import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CondensedPostCardComponent } from './condensed-post-card.component';

describe('CondensedPostCardComponent', () => {
  let component: CondensedPostCardComponent;
  let fixture: ComponentFixture<CondensedPostCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CondensedPostCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CondensedPostCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
