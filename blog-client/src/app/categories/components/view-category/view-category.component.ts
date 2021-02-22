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

  category: Category;
  latestPosts: Post[];
  latestPostsUrl: string;
  latestPostsLoading: boolean = false;
  popularPosts: Post[];
  popularPostsUrl: string;
  popularPostsLoading: boolean = false;

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

          // Get popular posts for this category.
          this.loadPopularPosts();
        });
    }
  }

  loadPopularPosts() {
    // The posts page could only be null if we have reached the end.
    if (!this.popularPostsLoading && this.popularPostsUrl !== null) {
      this.popularPostsLoading = true;

      this.blogPostService.hot({
        nested: true,
        category_id: this.category.id
      }).subscribe((response: PaginatedResponse<Post>) => {
        this.popularPosts = (this.popularPosts || []).concat(response.results);
        this.popularPostsUrl = response.next;
        this.popularPostsLoading = false;
      });
    }
  }

  loadLatestPosts() {
    // TODO: Get them with a custom URL like we do in comments.getAll

  }

}
