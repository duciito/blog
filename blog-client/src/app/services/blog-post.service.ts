import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Router} from '@angular/router';
import {environment} from 'src/environments/environment';
import {Post} from '../models/post';

@Injectable({
  providedIn: 'root'
})
export class BlogPostService {

  private articlesEndpoint: string = `${environment.baseApiUrl}/articles/`;

  constructor(
    private http: HttpClient,
    private router: Router
  ) { }

  create(post: Post) {
    return this.http.post(this.articlesEndpoint, post);
  }
}
