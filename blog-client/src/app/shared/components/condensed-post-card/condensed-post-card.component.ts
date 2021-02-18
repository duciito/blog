import { Component, Input, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import {Post} from 'src/app/posts/models/post';
import {BlogPostService} from 'src/app/posts/services/blog-post.service';

@Component({
  selector: 'app-condensed-post-card',
  templateUrl: './condensed-post-card.component.html',
  styleUrls: ['./condensed-post-card.component.scss']
})
export class CondensedPostCardComponent implements OnInit {

  @Input() post: Post;

  constructor(
    private router: Router,
    public blogPostService: BlogPostService
  ) { }

  ngOnInit(): void {
  }

  goToPost() {
    this.router.navigate([`posts/${this.post.id}`], {
      state: {post: this.post}
    });
  }
}
