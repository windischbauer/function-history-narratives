import { Injectable } from '@angular/core';
import { HttpService } from '@core/http/http.service';
import { Observable } from 'rxjs';
import { User } from '@models/user';
import { HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class BackendUserService {
  private readonly BASE_URL_USER = '/user';

  constructor(
    private http: HttpService,
  ) {
  }

  getUser(id: string | number): Observable<User> {
    return this.http.get<User>(this.BASE_URL_USER + '/' + id);
  }

  getUsersByRepo(rid: number): Observable<User[]> {
    return this.http.get<User[]>(`/repo/${rid}` + this.BASE_URL_USER);
  }
}
