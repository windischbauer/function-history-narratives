import { AfterViewInit, Component, EventEmitter, Input, OnChanges, OnInit, Output, ViewChild } from '@angular/core';
import { Func } from '@models/func';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { Event } from '@angular/router';

@Component({
  selector: 'app-function',
  templateUrl: './function.component.html',
  styleUrls: ['./function.component.scss'],
})
export class FunctionComponent implements AfterViewInit, OnChanges {
  @Input() functions: Func[] = [];
  @Output() selectedFuncEmitter: EventEmitter<Func> = new EventEmitter<Func>();
  @Output() clearFuncsEmitter: EventEmitter<any> = new EventEmitter<any>();

  // Options
  @Input() excludeTests = true;
  @Input() excludeEmptyBodies = true;

  funcDataSource: MatTableDataSource<Func>;

  constructor() {
  }

  ngAfterViewInit(): void {
    this.funcDataSource = new MatTableDataSource<Func>(this.functions);
    this.funcDataSource.filterPredicate = (data: Func, filter: string) => {
      if (this.excludeEmptyBodies) {
        if (!data.body) {
          return false;
        }
      }
      if (this.excludeTests) {
        if (data.name.includes('tests.')) {
          return false;
        }
      }
      return true;
    };
    this.funcDataSource.sort = this.tableSort;
    this.applyFilter();
  }

  ngOnChanges(): void {
    this.applyFilter();
  }

  @ViewChild(MatSort) tableSort: MatSort;

  emitFunction(func: Func): void {
    this.selectedFuncEmitter.emit(func);
  }

  clearFuncs(): void {
    this.clearFuncsEmitter.emit();
  }

  isExcluded(func: Func): boolean {
    return func.name.includes('tests.') && this.excludeTests;
  }

  applyFilter(): void {
    this.funcDataSource.filter = 'applyFilter';
  }

}
