import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';
import {environment} from 'src/environments/environment';
import {Category} from '../models/category';

@Injectable({
  providedIn: 'root'
})
export class CategoryService {

  private categoriesEndpoint: string = `${environment.baseApiUrl}/categories/`;

  constructor(
    private http: HttpClient
  ) { }

  getAll(): Observable<Category[]> {
    return this.http.get<Category[]>(this.categoriesEndpoint);
  }

  get(id: number): Observable<Category> {
    return this.http.get<Category>(`${this.categoriesEndpoint}${id}/`);
  }
}
