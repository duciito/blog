import {Injectable} from "@angular/core";
import {AccountService} from '../services/account.service';
import {HttpRequest, HttpHandler} from '@angular/common/http';
import {isNullOrUndefined} from 'util';
import {User} from '../models/user';

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
        Authorization: `Bearer: ${token}`
      }
    });
    return next.handle(req);
  }
}
