import { Component, OnInit } from '@angular/core';
import { StateService } from '@core/services/state.service';
import { Func } from '@models/func';
import { BackendVertexService } from '@core/backend-services/backend-vertex.service';
import { GraphService } from '@core/services/graph.service';
import { ActivatedRoute, Router } from '@angular/router';
import { BackendDiffService } from '@core/backend-services/backend-diff.service';
import { Diff } from '@models/diff';
import * as Diff2Html from 'diff2html';
import { Repo } from '@models/repo';
import { BackendCommitService } from '@core/backend-services/backend-commit.service';
import { Commit } from '@models/commit';
import { BackendFunctionService } from '@core/backend-services/backend-function.service';


@Component({
  selector: 'app-evaluation',
  templateUrl: './evaluation.component.html',
  styleUrls: ['./evaluation.component.scss'],
})
export class EvaluationComponent implements OnInit {
  fname = '';

  graph: { nodes, edges };
  incomingEdges = 0;
  outgoingEdges = 0;
  // diff: Diff;
  outputHtml: string;
  currentDiffCommitRev: string;
  explorationOutputHtml: string;
  explorationCurrentCommitRev: string;
  explorationCommits: Commit[] = [];
  explorationFuncs: Func[] = [];
  explorationFunctionName = '';

  // Options
  depth = 1;
  sliderFunctionVersion: number;
  waiting = -1;

  constructor(
    public stateService: StateService,
    private commitService: BackendCommitService,
    private diffService: BackendDiffService,
    private funcService: BackendFunctionService,
    private graphService: GraphService,
    private vertexService: BackendVertexService,
    private route: ActivatedRoute,
    private router: Router,
  ) {
    this.route.params.subscribe(params => {
      this.fname = params.functionName;
      const f = new Func();
      const r = new Repo();
      f.name = params.functionName;
      r.id = params.repoId;
      this.stateService.selectedRepo = r;

      this.stateService.waitingChange.subscribe(value => {
        this.waiting = value;
        console.log(value);
        if (this.waiting === 0) {
          this.updateGraphAndDiff(this.stateService.selectedFunc);
        }
      });
      this.stateService.getVersionsByFunction(f, r);

    });
  }

  ngOnInit(): void {
  }

  updateGraphAndDiff(func: Func): void {
    this.stateService.selectedFunc = func;
    if (func.name === this.fname) {
      this.getGraphByFunctionVersion(func);
    }
    this.getDiff(func, this.stateService.versionsOfSelectedFunc, false);
    this.getDiff(func, this.explorationFuncs, true);
    this.sliderFunctionVersion = this.stateService.versionsOfSelectedFunc.slice().reverse().findIndex((f) => {
      return f.commit_id <= this.stateService.selectedFunc.commit_id;
    }) + 1;
  }

  getGraphByFunctionVersion(func: Func): void {
    // console.log(`Getting graph for func version ${func.id}`);
    this.vertexService.getVertexByFunction(func).subscribe(vertex => {
      this.stateService.selectedVertex = vertex;
      if (vertex.id) {
        this.vertexService
          .getGraphByVertexAndDepth(this.stateService.selectedVertex, this.stateService.selectedFunc.commit_rev_string, this.depth)
          .subscribe(edges => {
            this.stateService.edges = edges;
            this.countEdges();
            this.graph = this.graphService.transformData(edges, this.stateService.selectedVertex.id);
          });
      }
    });
  }

  changeSelectedFunctionVersion(): void {
    const func = this.stateService.versionsOfSelectedFunc.slice().reverse()[this.sliderFunctionVersion - 1];
    this.updateGraphAndDiff(func);
  }

  countEdges(): void {
    this.incomingEdges = this.stateService.edges.filter(e => e.to_ === this.stateService.selectedVertex.id).length;
    this.outgoingEdges = this.stateService.edges.filter(e => e.from_ === this.stateService.selectedVertex.id).length;
  }

  getDiff(inputFunc: Func, versionsOfInputFunc: Func[], exploratory: boolean): void {
    const selectedFunc = inputFunc;

    const funcs = versionsOfInputFunc.filter(func => {
      return func.change_type.toString() !== 'fcall';
    });

    const nearestFunc = funcs.slice().reverse().find(func => {
      return func.commit_id <= selectedFunc.commit_id;
    });

    if (nearestFunc === undefined) {
      this.explorationCurrentCommitRev = '';
      this.explorationOutputHtml = this.init('');
      return;
    }

    const pastFunc = funcs.slice().reverse().find(func => {
      return func.commit_id < nearestFunc.commit_id;
    });

    this.diffService.getDiff(
      pastFunc === undefined ? '' : pastFunc.commit_rev_string,
      nearestFunc.commit_rev_string,
      this.extractFilename(nearestFunc.name),
      nearestFunc.name,
    ).subscribe(res => {
      if (!exploratory) {
        if (res.diff) {
          this.outputHtml = this.init(res.diff);
        }
        this.currentDiffCommitRev = nearestFunc.commit_rev_string;
      } else {
        if (res.diff) {
          this.explorationOutputHtml = this.init(res.diff);
        }
        this.explorationCurrentCommitRev = nearestFunc.commit_rev_string;
      }
    });
  }


  extractFilename(funcName: string): string {
    let index = funcName.lastIndexOf('.');
    do {
      funcName = funcName.slice(0, index);
      index = funcName.lastIndexOf('.');
      if (index === -1) {
        return funcName.replace(/\./gi, '/');
      }
    } while (funcName.charAt(index + 1) === funcName.charAt(index + 1).toUpperCase());
    return funcName.replace(/\./gi, '/');
  }

  init(diff: string): string {
    return Diff2Html.html(diff, {drawFileList: true, matching: 'lines'});
  }

  getExplorationValuesByVertex(vid: number): void {
    this.commitService.getCommitsByVertex(vid, this.stateService.selectedRepo.id).subscribe(commits => {
      this.explorationCommits = commits;
    });
    this.funcService.getFunctionsByVertex(vid, this.stateService.selectedRepo.id).subscribe(functions => {
      this.explorationFuncs = functions;
      this.explorationFunctionName = functions[0].name;
      this.getDiff(this.stateService.selectedFunc, functions, true);
    });
  }

  goToExploratoryFunction(): void {
    this.router.navigate([`/eval/repo/${this.stateService.selectedRepo.id}/function/${this.explorationFunctionName}`])
      .catch(error => {
        console.log('Something went wrong during routing');
        console.log(error);
      })
      .finally(() => {
        this.resetExplorationValues();
      });
  }

  resetExplorationValues(): void {
    this.explorationFunctionName = '';
    this.explorationCommits = [];
    this.explorationFuncs = [];
    this.explorationOutputHtml = this.init('');
    this.explorationCurrentCommitRev = '';
  }

  /*
   * Note: Possiblity to add another exploration mode, by enabling fetching call graphs on exploration commits
   *  Disable fname check in updateGraphAndDiff. This should in turn most likely also skip on fetching the fcalls.
   */

}
