import { Injectable } from '@angular/core';
import { HttpService } from '@core/http/http.service';
import { Observable } from 'rxjs';
import { Func } from '@models/func';
import { HttpParams } from '@angular/common/http';
import { Vertex } from '@models/vertex';
import { Edge } from '@models/edge';

@Injectable({
  providedIn: 'root',
})
export class BackendVertexService {
  private readonly BASE_URL_VERTEX = '/vertex';
  private readonly VERTEX_FUNCTION = this.BASE_URL_VERTEX + '/function';

  constructor(
    private http: HttpService,
  ) {
  }

  getVertex(): Observable<Vertex[]> {
    return this.http.get<Vertex[]>(this.BASE_URL_VERTEX);
  }

  getVertexByFunction(func: Func): Observable<Vertex> {
    return this.http.get<Vertex>(this.VERTEX_FUNCTION + `/${func.id}`);
  }

  getGraphByVertex(vertex: Vertex): Observable<Edge[]> {
    return this.http.get<Edge[]>(this.BASE_URL_VERTEX + `/${vertex.id}/edges`);
  }

  getGraphByVertexAndDepth(vertex: Vertex, commitRevString: string, depth: number): Observable<Edge[]> {
    const params = new HttpParams()
      .set('depth', String(depth))
      .set('commit_rev_string', commitRevString);
    return this.http.get<Edge[]>(this.BASE_URL_VERTEX + `/${vertex.id}/edges/`, {params});
  }

}
