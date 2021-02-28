import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Router} from '@angular/router';
import {Observable} from 'rxjs';
import {User} from 'src/app/core/models/user';
import {FollowableServiceMixin} from 'src/app/shared/mixins/followable-service-mixin';
import {addExtraParams} from 'src/app/shared/utils/add-extra-params';
import {environment} from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService extends FollowableServiceMixin {
  constructor(
    http: HttpClient
  ) {
    super(http, `${environment.baseApiUrl}/users/`);
  }

  getAll(extraParams?: any): Observable<User[]> {
    let url = addExtraParams(this.endpoint, extraParams);
    return this.http.get<User[]>(url);
  }

  get(id: number, extraParams?: any): Observable<User> {
    let url = addExtraParams(`${this.endpoint}${id}/`, extraParams);
    return this.http.get<User>(url);
  }

  followers(
    id: number,
    extraParams?: any,
    customUrl?: string
  ): Observable<User[]> {
    let url = customUrl ?? addExtraParams(
      `${this.endpoint}${id}/followers`, extraParams
    );
    return this.http.get<User[]>(url);
  }

  followedUsers(
    id: number,
    extraParams?: any,
    customUrl?: string
  ): Observable<User[]> {
    let url = customUrl ?? addExtraParams(
      `${this.endpoint}${id}/followed_users`, extraParams
    );
    return this.http.get<User[]>(url);
  }
}
