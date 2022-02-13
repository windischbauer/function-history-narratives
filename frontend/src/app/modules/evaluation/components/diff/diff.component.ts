import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';


@Component({
  selector: 'app-diff',
  templateUrl: './diff.component.html',
  styleUrls: ['./diff.component.scss'],
})
export class DiffComponent implements OnInit, OnChanges {
  @Input() input: string;
  @Input() commitRevString: string;
  @Input() functionName: string;

  outputHtml: string;

  constructor() {
    this.init();
  }

  ngOnInit(): void {
    this.init();
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.init();
  }


  init(): void {
    if (this.input) {
      this.outputHtml = this.input;
    }
  }

}
