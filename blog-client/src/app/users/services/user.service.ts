import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Router} from '@angular/router';
import {Observable} from 'rxjs';
import {User} from 'src/app/core/models/user';
import {addExtraParams} from 'src/app/shared/utils/add-extra-params';
import {environment} from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private usersEndpoint: string = `${environment.baseApiUrl}/users/`;

  constructor(
    private http: HttpClient,
    private router: Router
  ) { }

  getAll(extraParams?: any): Observable<User[]> {
    let url = addExtraParams(this.usersEndpoint, extraParams);
    return this.http.get<User[]>(this.usersEndpoint);
  }

  get(id: number, extraParams?: any): Observable<User> {
    let url = addExtraParams(`${this.usersEndpoint}${id}/`, extraParams);
    return this.http.get<User>(url);
  }

  follow(id: number) {
    let url = `${this.usersEndpoint}${id}/follow/`;
    return this.http.post(url, null);
  }

  unfollow(id: number) {
    let url = `${this.usersEndpoint}${id}/unfollow/`;
    return this.http.post(url, null);
  }
}
