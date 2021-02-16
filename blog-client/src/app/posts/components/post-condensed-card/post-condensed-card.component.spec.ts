import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostCondensedCardComponent } from './post-condensed-card.component';

describe('PostCondensedCardComponent', () => {
  let component: PostCondensedCardComponent;
  let fixture: ComponentFixture<PostCondensedCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PostCondensedCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PostCondensedCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
