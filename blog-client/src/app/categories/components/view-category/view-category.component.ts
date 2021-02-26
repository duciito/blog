import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Observable} from 'rxjs';
import {map, tap} from 'rxjs/operators';
import {Post} from 'src/app/posts/models/post';
import {BlogPostService} from 'src/app/posts/services/blog-post.service';
import {PaginatedResponse} from 'src/app/shared/models/paginated-response';
import {ApiResourceLoader} from 'src/app/shared/utils/api-resource-loader';
import {Category} from '../../models/category';
import {CategoryService} from '../../services/category.service';

@Component({
  selector: 'app-view-category',
  templateUrl: './view-category.component.html',
  styleUrls: ['./view-category.component.scss']
})
export class ViewCategoryComponent implements OnInit {

  category: Category;
  latestPostsLoader: ApiResourceLoader<Post>;
  popularPostsLoader: ApiResourceLoader<Post>;

  constructor(
    public categoryService: CategoryService,
    private route: ActivatedRoute,
    private blogPostService: BlogPostService
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];

    if (id) {
      this.categoryService.get(id)
        .subscribe((category: Category) => {
          this.category = category;
          const httpConfig = {
            nested: true,
            category_id: this.category.id,
            page_size: 3
          };

          // Initialize post sections loaders.
          this.latestPostsLoader = new ApiResourceLoader<Post>(
            pageUrl => this.blogPostService.getAll(
              Object.assign(httpConfig, {desc_order: true}),
              pageUrl
            )
          );
          this.popularPostsLoader = new ApiResourceLoader<Post>(
            pageUrl => this.blogPostService.hot(httpConfig, pageUrl)
          );

          // Get latest posts for this category.
          this.latestPostsLoader.loadMore();
          // Get popular posts for this category.
          this.popularPostsLoader.loadMore();
        });
    }
  }
}
