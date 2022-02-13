import {
  Inject,
  Injectable,
  InjectionToken,
  Injector,
  Optional,
} from '@angular/core';
import {
  HttpClient,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { ApiPrefixInterceptor } from '@core/interceptors/api-prefix.interceptor';
import { ErrorHandlerInterceptor } from '@core/interceptors/error-handler.interceptor';
import { Observable } from 'rxjs';

/**
 * From @angular/common/http/src/interceptor: allows chaining interceptors
 */
class HttpInterceptorHandler implements HttpHandler {
  constructor(
    private next: HttpHandler,
    private interceptor: HttpInterceptor,
  ) {
  }

  handle(request: HttpRequest<any>): Observable<HttpEvent<any>> {
    return this.interceptor.intercept(request, this.next);
  }
}

/**
 * Allows overriding default dynamic interceptors that can be disabled with the HttpService extension.
 * Except for very specific needs, you should better configure these interceptors directly in the constructor below
 * for better readability.
 *
 * For static interceptors that should always be enabled (like ApiPrefixInterceptor), use the standard
 * HTTP_INTERCEPTORS token.
 */
export const HTTP_DYNAMIC_INTERCEPTORS = new InjectionToken<HttpInterceptor>(
  'HTTP_DYNAMIC_INTERCEPTORS',
);

/**
 * This service is used for http requests and automatically include defined interceptors.
 */
@Injectable({
  providedIn: 'root',
})
export class HttpService extends HttpClient {
  constructor(
    private httpHandler: HttpHandler,
    private injector: Injector,
    @Optional()
    @Inject(HTTP_DYNAMIC_INTERCEPTORS)
    private interceptors: HttpInterceptor[],
  ) {
    super(httpHandler);

    this.interceptors = [
      this.injector.get(ApiPrefixInterceptor),
      this.injector.get(ErrorHandlerInterceptor),
    ];
  }

  request(method?: any, url?: any, options?: any): any {
    const handler = this.interceptors.reduceRight(
      (next, interceptor) => new HttpInterceptorHandler(next, interceptor),
      this.httpHandler,
    );
    return new HttpClient(handler).request(method, url, options);
  }
}
