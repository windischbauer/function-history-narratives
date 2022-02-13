import { Injectable } from '@angular/core';
import { HttpService } from '@core/http/http.service';
import { Repo } from '@models/repo';
import { Observable } from 'rxjs';
import { HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class BackendGitService {
  private readonly BASE_URL_VC = '/git';

  constructor(
    private http: HttpService,
  ) {
  }

  // getVersionControl(): Observable<Repo[]> {
  //   return this.http.get<Repo[]>(this.BASE_URL_VC);
  // }

}
