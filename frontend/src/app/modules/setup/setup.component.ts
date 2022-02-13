import { Component, OnInit } from '@angular/core';
import { StateService } from '@core/services/state.service';
import { Repo } from '@models/repo';
import { BackendRepoService } from '@core/backend-services/backend-repo.service';
import { Func } from '@models/func';
import { BackendFunctionService } from '@core/backend-services/backend-function.service';
import { BackendGitService } from '@core/backend-services/backend-git.service';
import { Router } from '@angular/router';
import { BackendCommitService } from '@core/backend-services/backend-commit.service';
import { BackendUserService } from '@core/backend-services/backend-user.service';

@Component({
  selector: 'app-setup',
  templateUrl: './setup.component.html',
  styleUrls: ['./setup.component.scss'],
})
export class SetupComponent implements OnInit {
  // Input
  repoFormValue = '';
  waiting = false;

  // Options
  generateCallgraphs = true;
  excludeTests = true;
  excludeEmptyBodies = true;
  fullPath = false;

  constructor(
    public stateService: StateService,
    private commitService: BackendCommitService,
    private functionService: BackendFunctionService,
    private repoService: BackendRepoService,
    private userService: BackendUserService,
    private router: Router,
  ) {
  }

  ngOnInit(): void {
    this.getRepos();
    // Caching code - Not really necessary
    if (this.stateService.functions.length === 0) {
      if (this.stateService.selectedRepo != null) {
        this.getFunctionsByRepo(this.stateService.selectedRepo);
      }
    }
  }

  /**
   * Fetches the Repos from the backend
   */
  getRepos(): void {
    this.repoService.getRepos().subscribe(repos => {
      this.stateService.repos = repos;
      this.waiting = false;
    });
  }

  /**
   * Gets all functions contained in a repo from the backend
   * and starts querying all relevant users.
   *
   * @param repo to be queried against
   */
  getFunctionsByRepo(repo: Repo): void {
    this.waiting = true;
    this.functionService.getFunctionsByRepo(repo).subscribe(funcs => {
      this.stateService.selectedRepo = repo;
      this.stateService.functions = funcs;
      this.waiting = false;
    });
  }

  setSelectedFunctionAndRouteToEval(func: Func): void {
    this.stateService.selectedFunc = func;
    this.routeToEvaluationPage();
  }


  // getVersionsByFunction(func: Func): void {
  //   this.waiting = true;
  //   this.functionService.getFunctionVersions(func, this.stateService.selectedRepo).subscribe(funcs => {
  //     this.stateService.versionsOfSelectedFunc = funcs;
  //     this.stateService.selectedFunc = funcs[funcs.length - 1];
  //     this.userService.getUsersByRepo(this.stateService.selectedRepo.id).subscribe(users => {
  //       this.stateService.userList = users;
  //     });
  //     // this.getCommitsByFunction(this.stateService.selectedFunc);
  //   });
  // }


  // getCommitsByFunction(func: Func): void {
  //   this.commitService.getCommitsByFunction(func, this.stateService.selectedRepo).subscribe(commits => {
  //     this.stateService.commits = commits;
  //     this.stateService.selectedFunc = func;
  //     this.routeToEvaluationPage();
  //   });
  // }

  /**
   * Creates a new repo in the backend and starts the pre-analysis.
   * The path needs to be an absolute path.
   *
   * @param path where the repo is located
   */
  createGitRepo(path: string): void {
    this.waiting = true;
    this.repoService.createVersionControl({path}).subscribe(
      r => {
        console.log(r);
        if (this.generateCallgraphs) {
          this.repoService.generateCallGraphs(r).subscribe(() => {
            this.waiting = false;
            this.getRepos();
          });
        } else {
          this.waiting = false;
          this.getRepos();
        }
      }, error => {
        this.waiting = false;
      });
  }

  /**
   * Starts the graph analysis in the backend. Takes up the majority of the time.
   */
  startAnalysis(repo: Repo): void {
    return;
  }

  clearFunctions(): void {
    this.stateService.functions = [];
  }

  emptyBodyCount(): number {
    return this.stateService.functions.filter(f => f.body == null).length;
  }

  testCount(): number {
    return this.stateService.functions.filter(f => f.name.match('tests.')).length;
  }

  private routeToEvaluationPage(): void {
    // Route to eval page
    this.router.navigate([`/eval/repo/${this.stateService.selectedRepo.id}/function/${this.stateService.selectedFunc.name}`])
      .catch(err => {
        console.log('Something went wrong during routing');
        console.log(err);
      })
      .finally(() => {
        this.waiting = false;
      });
  }
}
