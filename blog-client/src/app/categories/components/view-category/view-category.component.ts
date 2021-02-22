import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Observable} from 'rxjs';
import {map, tap} from 'rxjs/operators';
import {Post} from 'src/app/posts/models/post';
import {BlogPostService} from 'src/app/posts/services/blog-post.service';
import {PaginatedResponse} from 'src/app/shared/models/paginated-response';
import {Category} from '../../models/category';
import {CategoryService} from '../../services/category.service';

@Component({
  selector: 'app-view-category',
  templateUrl: './view-category.component.html',
  styleUrls: ['./view-category.component.scss']
})
export class ViewCategoryComponent implements OnInit {

  category$: Observable<Category>;
  latestPosts$: Observable<Post[]>;
  popularPosts$: Observable<Post[]>;

  constructor(
    public categoryService: CategoryService,
    private route: ActivatedRoute,
    private blogPostService: BlogPostService
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];

    if (id) {
      this.category$ = this.categoryService.get(id)
        .pipe(tap((category: Category) => {
          this.popularPosts$ = this.blogPostService.hot({
            nested: true,
            category_id: category.id
          }).pipe(map((response: PaginatedResponse<Post>) => {
            return response.results;
          }));
        }));
    }
  }

}
