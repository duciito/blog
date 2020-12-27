import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';
import {first, map} from 'rxjs/operators';
import {AccountService} from '../services/account.service';

/* Prevent logged in users from accessing auth pages. */
@Injectable({
  providedIn: 'root'
})
export class LoggedinGuard implements CanActivate {
  constructor(
    private accountService: AccountService,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot) {
      return this.accountService.isLoggedIn
        .pipe(
          first(),
          map((isLoggedIn: boolean) => {
            if (isLoggedIn) {
              this.router.navigate(['']);
              return false;
            }

            return true;
          })
        );
  }
  
}
