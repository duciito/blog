import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Router} from '@angular/router';
import {environment} from 'src/environments/environment';
import {ArticleContent} from '../models/article-content';
import {Post} from '../models/post';

@Injectable({
  providedIn: 'root'
})
export class BlogPostService {

  private articlesEndpoint: string = `${environment.baseApiUrl}/articles/`;
  private articleContentEndpoint: string = `${environment.baseApiUrl}/article_contents/`;

  constructor(
    private http: HttpClient,
    private router: Router
  ) { }

  create(post: Post) {
    return this.http.post<Post>(this.articlesEndpoint, post);
  }

  uploadContent(articleContent: ArticleContent) {
    const formData = new FormData();

    for (const key in articleContent) {
      if (key == 'file') {
        const file = articleContent[key];
        formData.append(key, file, file.name);
      }
      formData.append(key, articleContent[key]);
    }

    return this.http.post(this.articleContentEndpoint, formData);
  }

  removeContent(id: number) {
    return this.http.delete(this.articleContentEndpoint + id);
  }
}
