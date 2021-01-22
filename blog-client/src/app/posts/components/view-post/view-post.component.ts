import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {Subject, Observable} from 'rxjs';
import {first} from 'rxjs/operators';
import {Category} from 'src/app/categories/models/category';
import {CategoryService} from 'src/app/categories/services/category.service';
import {User} from 'src/app/core/models/user';
import {UserService} from 'src/app/users/services/user.service';
import {Post} from '../../models/post';
import {BlogPostService} from '../../services/blog-post.service';

@Component({
  selector: 'app-view-post',
  templateUrl: './view-post.component.html',
  styleUrls: ['./view-post.component.scss']
})
export class ViewPostComponent implements OnInit {

  _routerStatePost: Post;
  post$: Subject<Post> = new Subject<Post>();
  creator$: Observable<User>;
  category$: Observable<Category>;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private blogPostService: BlogPostService,
    private userService: UserService,
    private categoryService: CategoryService
  ) {
    const routerState = this.router.getCurrentNavigation().extras.state;

    if (routerState && routerState.createdPost) {
      this._routerStatePost = routerState.createdPost;
    }
  }

  ngOnInit(): void {
    // Test if some post data has already been sent with route.
    const id = this.route.snapshot.params['id'];

    this.post$.asObservable()
      .pipe(first())
      .subscribe(post => {
        this.setRelatedData(post);
      });

    if (this._routerStatePost) {
      // Populates user and category
      this.post$.next(this._routerStatePost);

    }
    else if (id) {
      this.blogPostService.get(id, {full_data: true}).subscribe(this.post$);
    }
  }

  setRelatedData(post: Post) {
    if (!post.text) {
      this.blogPostService.getArticleText(post.id)
        .subscribe(text => {
          // Set text and update.
          post.text = text;
          this.post$.next(post);
        });
    }

    this.creator$ = this.userService.get(post.creator);
    if (post.category) {
      this.category$ = this.categoryService.get(post.category);
    }
  }
}
