import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';
import {VotableServiceMixin} from 'src/app/shared/mixins/votable-service-mixin';
import {addExtraParams} from 'src/app/shared/utils/add-extra-params';
import {environment} from 'src/environments/environment';
import {Comment} from '../models/comment';

@Injectable({
  providedIn: 'root'
})
export class CommentService extends VotableServiceMixin {

  constructor(
    http: HttpClient
  ) {
    super(http, `${environment.baseApiUrl}/comments/`);
  }

  create(comment: Comment) {
    return this.http.post(this.endpoint, comment);
  }

  getAll(extraParams?: any): Observable<Comment[]> {
    const url = addExtraParams(this.endpoint, extraParams);
    return this.http.get<Comment[]>(url);
  }
}
