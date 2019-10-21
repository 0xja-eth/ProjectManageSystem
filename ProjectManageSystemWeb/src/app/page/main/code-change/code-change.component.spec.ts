import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CodeChangeComponent } from './code-change.component';

describe('CodeChangeComponent', () => {
  let component: CodeChangeComponent;
  let fixture: ComponentFixture<CodeChangeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CodeChangeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CodeChangeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
