import { Injectable } from '@angular/core';
import {environment} from 'src/environments/environment';
import {HttpClient} from '@angular/common/http';
import {User} from '../models/user';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {Router} from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AccountService {

  private authEndpoint: string = `${environment.baseApiUrl}/auth/`;

  constructor(
    private http: HttpClient,
    private router: Router
  ) { }

  getLocalToken(): string {
    const user: User = JSON.parse(localStorage.getItem('user'));
    return user ? user.token : null;
  }

  login(email: string, password: string) {
    return this.http.post<User>(
      `${this.authEndpoint}login/`,
      { email, password }
    ).pipe(
      map((user: User) => {
        // Save the user in local storage
        localStorage.setItem('user', JSON.stringify(user));
        return user;
      })
    );
  }

  register(user: User){
    return this.http.post(`${this.authEndpoint}signup/`, user);
  }

  logout() {
    // Remove from local storage instead of deauthing with the server.
    localStorage.removeItem('user');
    this.router.navigate(['login'])
  }
}
