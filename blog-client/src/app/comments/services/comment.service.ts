import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {environment} from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CommentService {

  private commentsEndpoint: string = `${environment.baseApiUrl}/comments/`;

  constructor(
    private http: HttpClient
  ) { }

  getAll(extraParams?: any) {

  }
}
