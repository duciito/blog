import {Injectable} from "@angular/core";
import {AccountService} from '../services/account.service';
import {HttpRequest, HttpHandler, HttpErrorResponse} from '@angular/common/http';
import {isNullOrUndefined} from 'util';
import {User} from '../models/user';
import {tap} from 'rxjs/operators';

@Injectable()
export class TokenInterceptor {
  constructor(private accountService: AccountService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler) {

    const token: string = this.accountService.getLocalToken();

    // If no token, just pass it onto the next interceptor.
    if (isNullOrUndefined(token)) {
      return next.handle(req);
    }

    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });

    return next.handle(req).pipe(
      tap(
        () => {},
        (err: any) => {
          if (err instanceof HttpErrorResponse && err.status == 401) {
            // Token has expired.
            this.accountService.logout();
          }
        }
      )
    );
  }
}
