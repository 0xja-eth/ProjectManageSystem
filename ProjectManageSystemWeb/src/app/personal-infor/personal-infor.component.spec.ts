import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PersonalInforComponent } from './personal-infor.component';

describe('PersonalInforComponent', () => {
  let component: PersonalInforComponent;
  let fixture: ComponentFixture<PersonalInforComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PersonalInforComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PersonalInforComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
