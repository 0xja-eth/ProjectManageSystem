import {Component, forwardRef, Inject, OnInit} from '@angular/core';
import {FormBuilder, FormGroup} from '@angular/forms';

@Component({
  selector: 'app-code-change',
  templateUrl: './code-change.component.html',
  styleUrls: ['./code-change.component.css']
})
export class CodeChangeComponent implements OnInit {

  private codeForm: FormGroup;

  constructor(@Inject(forwardRef(() => FormBuilder)) private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.codeForm = this.formBuilder.group({
      nickName: [''],
      password_old: [''],
      password_new: [''],
      new_again: [''],
    });
  }

  submit(): void {
    console.log(this.codeForm.value);
  }
}
