import {Injectable} from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '@env/environment';

/**
 * Prefixes all requests with `environment.apiUrl`.
 */
@Injectable({
  providedIn: 'root',
})
export class ApiPrefixInterceptor implements HttpInterceptor {

  constructor() {
  }

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    if (!/^(http|https):/i.test(request.url)) {
      request = request.clone({
        url: environment.apiUrl + request.url,
      });
    }
    return next.handle(request);
  }
}
