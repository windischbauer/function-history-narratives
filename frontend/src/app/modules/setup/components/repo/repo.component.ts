import { AfterViewInit, Component, EventEmitter, Input, OnChanges, OnInit, Output, ViewChild } from '@angular/core';
import { Repo } from '@models/repo';
import { SubstringService } from '@core/services/substring.service';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { MatSort, Sort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-repo',
  templateUrl: './repo.component.html',
  styleUrls: ['./repo.component.scss'],
})
export class RepoComponent implements OnChanges {
  @Input() repos: Repo[] = [];
  @Input() fullPath = false;
  @Output() selectedRepo: EventEmitter<Repo> = new EventEmitter<Repo>();

  dataSource: MatTableDataSource<Repo>;

  constructor() {
  }

  ngOnChanges(): void {
    this.dataSource = new MatTableDataSource<Repo>(this.repos);
    this.dataSource.sort = this.sort;
  }

  @ViewChild(MatSort) sort: MatSort;

  emitRepo(repo: Repo): void {
    this.selectedRepo.emit(repo);
  }
}
