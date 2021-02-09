import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LikeSectionComponent } from './like-section.component';

describe('LikeSectionComponent', () => {
  let component: LikeSectionComponent;
  let fixture: ComponentFixture<LikeSectionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LikeSectionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LikeSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
