import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import {AccountService} from '../services/account.service';

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
      const token: string = this.accountService.getLocalToken();

      if (token) {
        return true;
      }

      this.router.navigate(['login'], {queryParams: {returnUrl: state.url}});
      return false;
  }
  
}
