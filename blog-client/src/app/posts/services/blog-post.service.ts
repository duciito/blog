import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';
import {VotableServiceMixin} from 'src/app/shared/mixins/votable-service-mixin';
import {PaginatedResponse} from 'src/app/shared/models/paginated-response';
import {addExtraParams} from 'src/app/shared/utils/add-extra-params';
import {environment} from 'src/environments/environment';
import {ArticleContent} from '../models/article-content';
import {Post} from '../models/post';

@Injectable({
  providedIn: 'root'
})
export class BlogPostService extends VotableServiceMixin {

  private articleContentEndpoint: string = `${environment.baseApiUrl}/article_contents/`;

  constructor(
    http: HttpClient
  ) {
    super(http, `${environment.baseApiUrl}/articles/`);
  }

  create(post: Post) {
    const formData = this._transformToFormData(post);
    return this.http.post<Post>(this.endpoint, formData);
  }

  get(id: number, extraParams?: any): Observable<Post> {
    const url = addExtraParams(`${this.endpoint}${id}/`, extraParams);
    return this.http.get<Post>(url);
  }

  hot(extraParams?: any): Observable<PaginatedResponse<Post>> {
    // Gets popular posts as determined by the API.
    const url = addExtraParams(this.endpoint + 'hot/', extraParams);
    return this.http.get<PaginatedResponse<Post>>(url);
  }

  recentFromFollowing(extraParams?: any): Observable<PaginatedResponse<Post>> {
    // Gets popular posts as determined by the API.
    const url = addExtraParams(this.endpoint + 'recent_from_following/', extraParams);
    return this.http.get<PaginatedResponse<Post>>(url);
  }

  save(id: number) {
    return this.http.post(`${this.endpoint}${id}/save/`, null);
  }

  unsave(id: number) {
    return this.http.post(`${this.endpoint}${id}/unsave/`, null);
  }

  getArticleText(id: number) {
    return this.http.get<string>(`${this.endpoint}${id}/text`);
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
