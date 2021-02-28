import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
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
  user: User;
  userPostsLoader: ApiResourceLoader<Post>;
  followersLoader: ApiResourceLoader<User>;
  followedUsersLoader: ApiResourceLoader<User>;

  constructor(
    public userService: UserService,
    private route: ActivatedRoute,
    private blogPostService: BlogPostService,
    private accountService: AccountService
  ) { }

  ngOnInit(): void {
    let id = this.route.snapshot.params['id'];
    if (!id) {
      // Allow navigating to own profile with no ID.
      id = this.accountService.getLoggedInUser().id;
    }

    this.userService.get(id, {extra_info: true}).subscribe(user => {
      this.user = user;
      this.setRelatedData();
    });
  }

  setRelatedData() {
    // Get all user posts in descending order.
    this.userPostsLoader = new ApiResourceLoader<Post>(
      pageUrl => this.blogPostService.getAll(
        {
          user_id: this.user.id,
          desc_order: true,
          page_size: 5
        },
        pageUrl
      )
    );
    // Get all followers for that user.
    this.followersLoader = new ApiResourceLoader<User>(
      pageUrl => this.userService.followers(
        this.user.id,
        undefined,
        pageUrl
      )
    );
    // Get users they're following.
    this.followedUsersLoader = new ApiResourceLoader<User>(
      pageUrl => this.userService.followedUsers(
        this.user.id,
        undefined,
        pageUrl
      )
    );
  }

}
