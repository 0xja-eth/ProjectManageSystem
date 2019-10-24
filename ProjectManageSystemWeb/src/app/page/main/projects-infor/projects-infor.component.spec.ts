import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectsInforComponent } from './projects-infor.component';

describe('ProjectsInforComponent', () => {
  let component: ProjectsInforComponent;
  let fixture: ComponentFixture<ProjectsInforComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProjectsInforComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProjectsInforComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
