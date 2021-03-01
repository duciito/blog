import {PaginatedResponse} from '../models/paginated-response';

export class ApiResourceLoader<T> {
  resourceArr: T[];
  resourceUrl: string;
  resourceLoading: boolean = false;

  constructor(private resourceFetchMethod: Function) {
  }

  loadMore() {
    // The resource page could only be null if we have reached the end.
    if (!this.resourceLoading && this.resourceUrl !== null) {
      this.resourceLoading = true;

      this.resourceFetchMethod(this.resourceUrl)
        .subscribe((response: PaginatedResponse<T>) => {
          this.resourceArr = (this.resourceArr || []).concat(response.results);
          this.resourceUrl = response.next;
          this.resourceLoading = false;
        });
    }
  }

  insertAtStart(obj: T) {
    this.resourceArr.unshift(obj);
  }

  getSimplifiedObj(): {
    arr: T[],
    url: string,
    loading: boolean
  } {
    return {
      arr: this.resourceArr,
      url: this.resourceUrl,
      loading: this.resourceLoading
    };
  }
}
