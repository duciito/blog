import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Router} from '@angular/router';
import {Observable} from 'rxjs';
import {User} from 'src/app/core/models/user';
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
    let url = this._addExtraParams(this.usersEndpoint, extraParams);
    return this.http.get<User[]>(this.usersEndpoint);
  }

  get(id: number, extraParams?: any): Observable<User> {
    let url = this._addExtraParams(`${this.usersEndpoint}${id}/`, extraParams);
    return this.http.get<User>(url);
  }

  _addExtraParams(url, extraParams) {
    if (extraParams) {
      for (const key in extraParams) {
        url += `?${key}=${extraParams[key]}`;
      }
    }

    return url;
  }
}
