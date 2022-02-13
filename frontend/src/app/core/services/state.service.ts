import { Injectable } from '@angular/core';
import { Edge } from '@models/edge';
import { Vertex } from '@models/vertex';
import { Func } from '@models/func';
import { Repo } from '@models/repo';
import { Commit } from '@models/commit';
import { User } from '@models/user';
import { Subject } from 'rxjs';
import { BackendFunctionService } from '@core/backend-services/backend-function.service';
import { BackendCommitService } from '@core/backend-services/backend-commit.service';
import { BackendUserService } from '@core/backend-services/backend-user.service';

@Injectable({
  providedIn: 'root',
})
export class StateService {

  private _repos: Repo[] = [];
  private _selectedRepo: Repo = undefined;
  private _functions: Func[] = [];
  private _selectedFunc: Func = undefined;
  private _versionsOfSelectedFunc: Func[] = [];
  private _commits: Commit[] = [];
  private _selectedCommit: Commit;
  private _selectedVertex: Vertex;
  private _edges: Edge[] = [];
  private _userList: User[] = [];

  private _waiting = 0;
  waitingChange: Subject<number> = new Subject<number>();
  versionsOfSelectedFuncChange: Subject<Func[]> = new Subject<Func[]>();
  commitsChange: Subject<Commit[]> = new Subject<Commit[]>();


  constructor(
    private commitService: BackendCommitService,
    private functionService: BackendFunctionService,
    private userService: BackendUserService,
  ) {
    this.versionsOfSelectedFuncChange.subscribe((value) => {
      this._versionsOfSelectedFunc = value;
    });
    this.commitsChange.subscribe((value) => {
      this._commits = value;
    });
    this.waitingChange.subscribe((value) => {
      this._waiting = value;
    });
  }

  set waiting(value: number) {
    this._waiting += value;
    this.waitingChange.next(this._waiting);
  }

  /**
   * Gets all versions of a specific function and then routes the user to the evaluation page.
   *
   * @param func to be queried against
   * @param repo to be queried against
   */
  getVersionsByFunction(func: Func, repo: Repo): void {
    this.waiting = 1;
    this.functionService.getFunctionVersions(func, repo).subscribe(funcs => {
      this.versionsOfSelectedFunc = funcs;
      this.selectedFunc = funcs[funcs.length - 1];
      this.waiting = 1;
      this.userService.getUsersByRepo(repo.id).subscribe(users => {
        this.userList = users;
        this.waiting = -1;
      });
      this.getCommitsByFunction(this.selectedFunc, repo);
      this.waiting = -1;
    });
  }

  /**
   * Gets all commits where the selected function was changed.
   *
   * @param func to be queried against
   * @param repo to be queried against
   */
  getCommitsByFunction(func: Func, repo: Repo): void {
    this.waiting = 1;
    this.commitService.getCommitsByFunction(func, repo).subscribe(commits => {
      this.commits = commits;
      this.waiting = -1;
    });
  }

  get repos(): Repo[] {
    return this._repos;
  }

  set repos(value: Repo[]) {
    this._repos = value;
  }

  get selectedRepo(): Repo {
    return this._selectedRepo;
  }

  set selectedRepo(value: Repo) {
    this._selectedRepo = value;
  }

  get functions(): Func[] {
    return this._functions;
  }

  set functions(value: Func[]) {
    this._functions = value;
  }

  get selectedFunc(): Func {
    return this._selectedFunc;
  }

  set selectedFunc(value: Func) {
    this._selectedFunc = value;
  }

  get versionsOfSelectedFunc(): Func[] {
    return this._versionsOfSelectedFunc;
  }

  set versionsOfSelectedFunc(value: Func[]) {
    this._versionsOfSelectedFunc = value;
    this.versionsOfSelectedFuncChange.next(this._versionsOfSelectedFunc);
  }

  get commits(): Commit[] {
    return this._commits;
  }

  set commits(value: Commit[]) {
    const sorted = value.sort((a: Commit, b: Commit) => a.id > b.id ? -1 : a.id < b.id ? 1 : 0);
    this._commits = sorted;
    this.commitsChange.next(this._commits);
  }

  get selectedCommit(): Commit {
    return this._selectedCommit;
  }

  set selectedCommit(value: Commit) {
    this._selectedCommit = value;
  }

  get selectedVertex(): Vertex {
    return this._selectedVertex;
  }

  set selectedVertex(value: Vertex) {
    this._selectedVertex = value;
  }

  get edges(): Edge[] {
    return this._edges;
  }

  set edges(value: Edge[]) {
    this._edges = value;
  }

  get userList(): User[] {
    return this._userList;
  }

  set userList(value: User[]) {
    this._userList = value;
  }

}
