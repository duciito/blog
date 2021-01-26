import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Router} from '@angular/router';
import {Observable} from 'rxjs';
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
    const formData = this._transformToFormData(post);
    return this.http.post<Post>(this.articlesEndpoint, formData);
  }

  get(id: number, extraParams?: any): Observable<Post> {
    let url = `${this.articlesEndpoint}${id}/`;

    if (extraParams) {
      for (const key in extraParams) {
        url += `?${key}=${extraParams[key]}`;
      }
    }

    return this.http.get<Post>(url);
  }

  getArticleText(id: number) {
    return this.http.get<string>(`${this.articlesEndpoint}${id}/text`);
  }

  uploadContent(articleContent: ArticleContent) {
    const formData = this._transformToFormData(articleContent);
    return this.http.post(this.articleContentEndpoint, formData);
  }

  removeContent(id: number) {
    return this.http.delete(`${this.articleContentEndpoint}${id}/`);
  }

  _transformToFormData(content: any): FormData {
    // Transform object/model to formData.
    const formData = new FormData();

    for (const key in content) {
      if (content[key] instanceof File) {
        const file = content[key];
        formData.append(key, file, file.name);
      }
      formData.append(key, content[key]);
    }

    return formData;
  }
}
