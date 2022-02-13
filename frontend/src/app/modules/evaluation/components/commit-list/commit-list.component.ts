import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Commit } from '@models/commit';
import { Func } from '@models/func';
import { User } from '@models/user';
import { StateService } from '@core/services/state.service';
import { ChangeType } from '@models/change-type';
import { find } from 'rxjs/operators';

@Component({
  selector: 'app-commit-list',
  templateUrl: './commit-list.component.html',
  styleUrls: ['./commit-list.component.scss'],
})
export class CommitListComponent implements OnInit {
  @Input() commits: Commit[] = [];
  @Input() exploratoryCommits: Commit[] = [];
  @Input() functions: Func[] = [];
  @Input() exploratoryFunctions: Func[] = [];
  @Input() selectedFunc: Func;
  @Output() funcEmitter: EventEmitter<Func> = new EventEmitter<Func>();
  // @Output() exploratoryFuncEmitter: EventEmitter<Func> = new EventEmitter<Func>();

  // Options
  excludeFcalls = false;
  fcallCount = 0;

  constructor(
    private stateService: StateService,
  ) {
  }

  ngOnInit(): void {
  }

  emitFunc(commit: Commit): void {
    // if (!commit.exploratory) {
    let func = this.functions.find(f => f.commit_rev_string === commit.rev_string);
    // console.log(`Emitting function ${func.id}`);
    if (!func) {
      func = this.exploratoryFunctions.find(f => f.commit_rev_string === commit.rev_string);
    }
    this.funcEmitter.emit(func);
    // }
  }

  isSelected(commit: Commit): boolean {
    return commit.rev_string === this.selectedFunc.commit_rev_string;
  }

  getUser(id: string | number): User {
    return this.stateService.userList.find(u => u.id === id);
  }

  getChangeType(commit: Commit): string {
    if (commit.exploratory === true) {
      return this.exploratoryFunctions.find((f: Func) => f.commit_rev_string === commit.rev_string).change_type.toString();
    } else {
      return this.functions.find((f: Func) => f.commit_rev_string === commit.rev_string).change_type.toString();
    }
    // return this.functions.find((f: Func) => f.commit_rev_string === commit.rev_string).change_type.toString();
  }

  isExcluded(commit: Commit): boolean {
    if (this.excludeFcalls) {
      if (this.getChangeType(commit) === 'fcall') {
        return true;
      }
    }
    return false;
  }

  getHighlight(commit: Commit, text: boolean): string {
    let highlight = '';
    switch (this.getChangeType(commit)) {
      case 'introduced':
        highlight += 'highlight-introduced' + (text ? '-text' : '');
        break;
      case 'param':
        highlight += 'highlight-param' + (text ? '-text' : '');
        break;
      case 'body':
        highlight += 'highlight-body' + (text ? '-text' : '');
        break;
      case 'multi':
        highlight += 'highlight-multi' + (text ? '-text' : '');
        break;
      case 'fcall':
        highlight += 'highlight-fcall' + (text ? '-text' : '');
        break;
    }
    if (!text) {
      if (this.isSelected(commit)) {
        highlight += ' selected';
      }
    }
    return highlight;
  }

  mergeCommitLists(): Commit[] {
    this.fcallCount = this.functions.filter(f => f.change_type.toString() === 'fcall').length;
    const merged = this.exploratoryCommits.map(f => {
      f.exploratory = true;
      return f;
    });
    // Note: can possibly be improved
    return merged.concat(this.commits).sort((a: Commit, b: Commit) => a.id > b.id ? -1 : a.id < b.id ? 1 : 0);
  }

}
