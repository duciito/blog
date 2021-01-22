import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {Post} from '../../models/post';
import {BlogPostService} from '../../services/blog-post.service';

@Component({
  selector: 'app-view-post',
  templateUrl: './view-post.component.html',
  styleUrls: ['./view-post.component.scss']
})
export class ViewPostComponent implements OnInit {

  post: Post;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private blogPostService: BlogPostService
  ) { }

  ngOnInit(): void {
    // Test if some post data has already been sent with route.
    const routerState = this.router.getCurrentNavigation().extras.state;
    const id = this.route.snapshot.queryParams['id'];

    if (routerState.createdPost) {
      this.post = routerState.createdPost;

      if (!this.post.text) {
        this.blogPostService.getArticleText(this.post.id)
          .subscribe(text => this.post.text = text);
      }
    }
    else if (id) {
      this.blogPostService.get(id)
        .subscribe(post => this.post = post);
    }
  }

}
