import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';
import {FollowableServiceMixin} from 'src/app/shared/mixins/followable-service-mixin';
import {environment} from 'src/environments/environment';
import {Category} from '../models/category';

@Injectable({
  providedIn: 'root'
})
export class CategoryService extends FollowableServiceMixin {
  constructor(
    http: HttpClient
  ) {
    super(http, `${environment.baseApiUrl}/categories/`);
  }

  getAll(): Observable<Category[]> {
    return this.http.get<Category[]>(this.endpoint);
  }

  get(id: number): Observable<Category> {
    return this.http.get<Category>(`${this.endpoint}${id}/`);
  }
}
