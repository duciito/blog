import {HttpClient} from '@angular/common/http';

export class FollowableServiceMixin {
  constructor (
    protected http: HttpClient,
    protected endpoint: string
  ) {}

  follow(id: number) {
    let url = `${this.endpoint}${id}/follow/`;
    return this.http.post(url, null);
  }

  unfollow(id: number) {
    let url = `${this.endpoint}${id}/unfollow/`;
    return this.http.post(url, null);
  }

}
