import { Component } from '@angular/core';
import {AccountService} from './services/account.service';
import {Observable} from 'rxjs';

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
