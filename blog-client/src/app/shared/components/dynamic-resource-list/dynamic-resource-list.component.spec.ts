import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DynamicResourceListComponent } from './dynamic-resource-list.component';

describe('DynamicResourceListComponent', () => {
  let component: DynamicResourceListComponent;
  let fixture: ComponentFixture<DynamicResourceListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DynamicResourceListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DynamicResourceListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
