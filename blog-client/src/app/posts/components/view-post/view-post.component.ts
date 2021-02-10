import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ToastrService} from 'ngx-toastr';
import {BehaviorSubject} from 'rxjs';
import {switchMap, tap} from 'rxjs/operators';
import {Category} from 'src/app/categories/models/category';
import {CategoryService} from 'src/app/categories/services/category.service';
import {CommentService} from 'src/app/comments/services/comment.service';
import {User} from 'src/app/core/models/user';
import {AccountService} from 'src/app/core/services/account.service';
import {UserService} from 'src/app/users/services/user.service';
import {Post} from '../../models/post';
import {BlogPostService} from '../../services/blog-post.service';
import {Comment} from 'src/app/comments/models/comment';

@Component({
  selector: 'app-view-post',
  templateUrl: './view-post.component.html',
  styleUrls: ['./view-post.component.scss']
})
export class ViewPostComponent implements OnInit {

  post: Post;
  creator: User;
  category: Category;
  following$: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  loggedUser: User;
  comments: Comment[];

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    public blogPostService: BlogPostService,
    private userService: UserService,
    private categoryService: CategoryService,
    private accountService: AccountService,
    private commentService: CommentService,
    private toastr: ToastrService
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

    this.loggedUser = this.accountService.getLoggedInUser();
  }

  setRelatedData() {
    if (!this.post.text) {
      this.blogPostService.getArticleText(this.post.id)
        .subscribe(text => {
          this.post.text = text;
        });
    }

    if (this.post.category) {
      this.categoryService.get(this.post.category)
      .subscribe(category => this.category = category);
    }

    // Set creator and then get logged user's additional info.
    this.userService.get(this.post.creator as number)
      .pipe(
        switchMap(creator => {
          this.creator = creator;
          return this.userService.get(this.loggedUser.id, {extra_info: true});
        })
      )
      .subscribe(user => {
        // Update following button content
        if (user.followed_users.includes(this.creator.id)) {
          this.following$.next(true);
        }
      })

    // Get post's comments.
    this.commentService.getAll({
      article_id: this.post.id,
      nested_creator: true,
      newest_first: true
    })
      .subscribe(response => this.comments = response.results);
  }

  followCreator() {
    const following = this.following$.value;
    const followFunc = (following
      ? this.userService.unfollow
      : this.userService.follow).bind(this.userService);

    // Follow/unfollow based on subject value.
    followFunc(this.creator.id)
      .subscribe(success => {
        this.following$.next(!following);
        this.toastr.info(
          `"${this.creator.username}" has been
          ${following ? 'removed from' : 'added to'} your followed users`,
          'User action'
        );
      });
  }

  save() {
    const saveFunc = (this.post.saved
      ? this.blogPostService.unsave
      : this.blogPostService.save).bind(this.blogPostService);

    saveFunc(this.post.id)
      .subscribe(success => {
        this.post.saved = !this.post.saved;
        this.toastr.info(
          `"${this.post.title}" has been
          ${this.post.saved ? 'added to' : 'removed from'} your saved articles`,
          'Article action'
        );
      });

  }

  onCommentCreated(comment: Comment) {
    // Add comment on top of list.
    if (typeof(comment.creator) !== 'object') {
      comment.creator = this.loggedUser;
    }
    this.comments.unshift(comment);
  }
}
