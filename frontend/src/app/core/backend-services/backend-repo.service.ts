import { Injectable } from '@angular/core';
import { HttpService } from '@core/http/http.service';
import { Observable } from 'rxjs';
import { Repo } from '@models/repo';
import { Func } from '@models/func';

@Injectable({
  providedIn: 'root',
})
export class BackendRepoService {
  private readonly BASE_URL_REPO = '/repo';
  private readonly BASE_URL_GIT = '/git';
  private readonly BASE_URL_GRAPH = '/graph';

  constructor(
    private http: HttpService,
  ) {
  }

  createVersionControl(path: { path }): Observable<Repo> {
    return this.http.post<Repo>(this.BASE_URL_GIT, path);
  }

  getRepos(): Observable<Repo[]> {
    return this.http.get<Repo[]>(this.BASE_URL_REPO);
  }

  createRepo(repo: Repo): Observable<Repo> {
    return this.http.post<Repo>(this.BASE_URL_REPO, repo);
  }

  generateCallGraphs(repo: Repo): Observable<any> {
    return this.http.post<any>(this.BASE_URL_GRAPH + `/${repo.id}`, {});
  }

}
