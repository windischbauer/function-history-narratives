import { Injectable } from '@angular/core';
import { HttpService } from '@core/http/http.service';
import { Observable } from 'rxjs';
import { Commit } from '@models/commit';
import { HttpParams } from '@angular/common/http';
import { Repo } from '@models/repo';
import { Func } from '@models/func';

@Injectable({
  providedIn: 'root',
})
export class BackendFunctionService {
  private readonly BASE_URL_FUNCTION = '/function';
  private readonly COMMIT_REV = '/commit' + this.BASE_URL_FUNCTION;

  constructor(
    private http: HttpService,
  ) {
  }

  getFunctions(): Observable<any[]> {
    return this.http.get<any[]>(this.BASE_URL_FUNCTION);
  }

  getFunctionVersions(func: Func, repo: Repo): Observable<Func[]> {
    const params = new HttpParams()
      .set('name', func.name)
      .set('rid', repo.id.toString());
    return this.http.get<Func[]>(this.COMMIT_REV, {params});
  }

  // getCommitsByFunction(item: FunctionListItemDto): Observable<Commit[]> {
  //
  //   const params = new HttpParams()
  //     .set('name', item.name)
  //     .set('parameters', item.parameters);
  //   return this.http.get<Commit[]>(this.BASE_URL_METHOD, {params});
  // }

  // getFunctionByVertexId(vid: number): Observable<Func> {
  //   return this.http.get<Func>(`vertex/${vid}` + this.BASE_URL_FUNCTION);
  // }


  getFunctionsByRepo(repo: Repo): Observable<Func[]> {
    return this.http.get<Func[]>(`/repo/${repo.id}` + this.BASE_URL_FUNCTION + 's');
  }

  getFunctionsByVertex(vid: number, rid: number): Observable<Func[]> {
    const params = new HttpParams()
      .set('rid', rid.toString());
    return this.http.get<Func[]>(`/vertex/${vid}` + this.BASE_URL_FUNCTION, {params});
  }
}

