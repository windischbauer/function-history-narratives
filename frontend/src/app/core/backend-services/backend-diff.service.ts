import { Injectable } from '@angular/core';
import { HttpService } from '@core/http/http.service';
import { Observable } from 'rxjs';
import { HttpParams } from '@angular/common/http';
import { Diff } from '@models/diff';

@Injectable({
  providedIn: 'root',
})
export class BackendDiffService {
  private readonly BASE_URL_DIFF = '/diff';

  constructor(
    private http: HttpService,
  ) {
  }

  getDiff(commitRevStringA: string, commitRevStringB: string, filename: string, funcName: string): Observable<Diff> {
    const params = new HttpParams()
      .set('crs_a', commitRevStringA)
      .set('crs_b', commitRevStringB)
      .set('filename', filename)
      .set('func_name', funcName);
    return this.http.get<Diff>(this.BASE_URL_DIFF, {params});
  }
}
