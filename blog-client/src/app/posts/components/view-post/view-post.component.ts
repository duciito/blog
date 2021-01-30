import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
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

  post: Post;
  creator: User;
  category: Category;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private blogPostService: BlogPostService,
    private userService: UserService,
    private categoryService: CategoryService
  ) {
    // Test if some post data has already been sent with route.
    const routerState = this.router.getCurrentNavigation().extras.state;

    if (routerState && routerState.createdPost) {
      this.post = routerState.createdPost;
    }
  }

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];

    if (this.post) {
      // Populates user and category
      this.setRelatedData();

    }
    else if (id) {
      // Do a full fetch of the article.
      this.blogPostService.get(id, {full_data: true})
        .subscribe(post => {
          this.post = post;
          this.setRelatedData();
        });
    }
  }

  setRelatedData() {
    if (!this.post.text) {
      this.blogPostService.getArticleText(this.post.id)
        .subscribe(text => {
          this.post.text = text;
        });
    }

    this.userService.get(this.post.creator)
      .subscribe(user => this.creator = user);

    if (this.post.category) {
      this.categoryService.get(this.post.category)
      .subscribe(category => this.category = category);
    }
  }

  vote() {
    const voteFunc = (this.post.voted
      ? this.blogPostService.unvote
      : this.blogPostService.vote).bind(this.blogPostService);

    voteFunc(this.post.id)
      .subscribe(
        () => {
          this.blogPostService.get(this.post.id, {full_data: true})
            .subscribe(post => this.post = post);
        }
      );
  }
}
