import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';
import {addExtraParams} from 'src/app/shared/utils/add-extra-params';
import {environment} from 'src/environments/environment';
import {Comment} from '../models/comment';

@Injectable({
  providedIn: 'root'
})
export class CommentService {

  private commentsEndpoint: string = `${environment.baseApiUrl}/comments/`;

  constructor(
    private http: HttpClient
  ) { }

  create(comment: Comment) {
    return this.http.post(this.commentsEndpoint, comment);
  }

  getAll(extraParams?: any): Observable<Comment[]> {
    const url = addExtraParams(this.commentsEndpoint, extraParams);
    return this.http.get<Comment[]>(url);
  }
}
