import {HttpClient} from '@angular/common/http';

export class VotableServiceMixin {
  constructor (
    protected http: HttpClient,
    protected endpoint: string
  ) {}

  vote(id: number) {
    return this.http.post(`${this.endpoint}${id}/vote/`, null);
  }

  unvote(id: number) {
    return this.http.post(`${this.endpoint}${id}/unvote/`, null);
  }

}
