import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  constructor(private activate:ActivatedRoute) { }

  ngOnInit() {
    // @ts-ignore
    this.page = this.activate.firstChild.url.value[0].path;
  }

  page:string = '';

  handle(index: string): void {
  }
}
