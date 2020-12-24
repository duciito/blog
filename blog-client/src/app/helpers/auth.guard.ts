import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import {AccountService} from '../services/account.service';
import {map, first} from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(
    private accountService: AccountService,
    private router: Router
  ) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot) {
      return this.accountService.isLoggedIn
        .pipe(
          first(),
          map((isLoggedIn: boolean) => {
            if (!isLoggedIn) {
              this.router.navigate(['login'], {queryParams: {returnUrl: state.url}});
              return false;
            }

            return true;
          })
        );
  }
}
