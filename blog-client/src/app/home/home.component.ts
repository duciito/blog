import { Component, OnInit } from '@angular/core';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {Post} from '../posts/models/post';
import {BlogPostService} from '../posts/services/blog-post.service';
import {PaginatedResponse} from '../shared/models/paginated-response';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  popularPosts$: Observable<Post[]>;
  postsFromFollowing$: Observable<Post[]>;

  constructor(
    private blogPostService: BlogPostService
  ) { }

  ngOnInit() {
    const customPostsObservable = (action: string) => {
      return this.blogPostService[action]({
        nested: true,
        page_size: '3',
        desc_order: true
      })
        .pipe(map((response: PaginatedResponse<Post>) => {
          return response.results;
        }));
    };

    this.popularPosts$ = customPostsObservable('hot');
    this.postsFromFollowing$ = customPostsObservable('recentFromFollowing');
  }
}
