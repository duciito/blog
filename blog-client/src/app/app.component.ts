import { Component } from '@angular/core';
import {Observable} from 'rxjs';
import {AccountService} from './core/services/account.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  isLoggedIn$: Observable<boolean> = this.accountService.isLoggedIn;

  constructor(private accountService: AccountService) {}

  logout() {
    this.accountService.logout();
  }
}
