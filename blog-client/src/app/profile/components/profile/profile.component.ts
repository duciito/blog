import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Subject} from 'rxjs';
import {User} from 'src/app/core/models/user';
import {AccountService} from 'src/app/core/services/account.service';
import {Post} from 'src/app/posts/models/post';
import {BlogPostService} from 'src/app/posts/services/blog-post.service';
import {ApiResourceLoader} from 'src/app/shared/utils/api-resource-loader';
import {UserService} from 'src/app/users/services/user.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  user$: Subject<User> = new Subject<User>();
  userPostsLoader: ApiResourceLoader<Post>;
  followersLoader: ApiResourceLoader<User>;
  followedUsersLoader: ApiResourceLoader<User>;

  constructor(
    private route: ActivatedRoute,
    private userService: UserService,
    private blogPostService: BlogPostService,
    private accountService: AccountService
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];
    const loggedUser = this.accountService.getLoggedInUser();

    this.user$.subscribe(this.setRelatedData);

    if (!id || id == loggedUser.id) {
      // Allow navigating to own profile with no ID.
      this.user$.next(loggedUser);
    }
    else if (id) {
      this.userService.get(id).subscribe(this.user$);
    }
  }

  setRelatedData(user: User) {
    // Get all user posts in descending order.
    this.userPostsLoader = new ApiResourceLoader<Post>(
      pageUrl => this.blogPostService.getAll(
        {user_id: user.id, desc_order: true},
        pageUrl
      )
    );
    // Get all followers for that user.
    this.followersLoader = new ApiResourceLoader<User>(
      pageUrl => this.userService.followers(
        user.id,
        undefined,
        pageUrl
      )
    );
    // Get users they're following.
    this.followedUsersLoader = new ApiResourceLoader<User>(
      pageUrl => this.userService.followedUsers(
        user.id,
        undefined,
        pageUrl
      )
    );
  }

}
