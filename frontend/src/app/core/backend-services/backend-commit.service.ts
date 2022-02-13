import { Injectable } from '@angular/core';
import { HttpService } from '@core/http/http.service';
import { Commit } from '@models/commit';
import { Observable } from 'rxjs';
import { HttpParams } from '@angular/common/http';
import { Func } from '@models/func';
import { Repo } from '@models/repo';

@Injectable({
  providedIn: 'root',
})
export class BackendCommitService {
  private readonly BASE_URL_COMMIT = '/commit';
  private readonly BASE_URL_VERTEX = '/vertex';
  private readonly COMMIT_BY_FUNCTION = '/function' + this.BASE_URL_COMMIT;
  private commitCounter = 0;

  constructor(
    private http: HttpService,
  ) {
  }

  getInitialCommits(): Observable<Commit[]> {
    this.commitCounter = 0;
    const params: HttpParams = new HttpParams()
      .set('page', String(this.commitCounter));
    return this.http.get<Commit[]>(this.BASE_URL_COMMIT, {params});
  }

  loadMore(): Observable<Commit[]> {
    this.commitCounter += 1;
    console.log(this.commitCounter);
    const params: HttpParams = new HttpParams()
      .set('page', String(this.commitCounter));
    console.log(params);
    return this.http.get<Commit[]>(this.BASE_URL_COMMIT, {params});
  }

  getCommitsByFunction(func: Func, repo: Repo): Observable<Commit[]> {
    const params: HttpParams = new HttpParams()
      .set('function_name', func.name)
      .set('rid', repo.id.toString());
    return this.http.get<Commit[]>(this.COMMIT_BY_FUNCTION, {params});
  }

  getCommitsByVertex(vid: number, rid: number): Observable<Commit[]> {
    const params: HttpParams = new HttpParams()
      .set('rid', rid.toString());
    return this.http.get<Commit[]>(this.BASE_URL_VERTEX + `/${vid}` + this.BASE_URL_COMMIT, {params});
  }

  print(message: string): void {
    console.log('COMMITSERVICE logs: ' + message);
  }

  // getFunctionVersions(func: Func): Observable<Func[]> {
  //   const params: HttpParams = new HttpParams()
  //     .set('name', func.name);
  //   return this.http.get<Func[]>(this.BASE_URL_COMMIT + '/functions', {params});
  // }

}
