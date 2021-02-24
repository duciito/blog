import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Observable} from 'rxjs';
import {User} from 'src/app/core/models/user';
import {AccountService} from 'src/app/core/services/account.service';
import {Post} from 'src/app/posts/models/post';
import {BlogPostService} from 'src/app/posts/services/blog-post.service';
import {UserService} from 'src/app/users/services/user.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  user: User;
  userPosts$: Observable<Post[]>;
  followers$: Observable<User[]>;
  followedUsers$: Observable<User[]>;

  constructor(
    private route: ActivatedRoute,
    private userService: UserService,
    private blogPostService: BlogPostService,
    private accountService: AccountService
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];
    const loggedUser = this.accountService.getLoggedInUser();

    if (!id || id == loggedUser.id) {
      // Allow navigating to own profile with no ID.
      this.user = loggedUser;
    }
    else if (id) {
      this.userService.get(id)
        .subscribe(user => {
          this.user = user;
        });
    }
  }

}
