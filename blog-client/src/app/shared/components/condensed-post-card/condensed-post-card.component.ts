import { Component, Input, OnInit } from '@angular/core';
import {Post} from 'src/app/posts/models/post';
import {BlogPostService} from 'src/app/posts/services/blog-post.service';

@Component({
  selector: 'app-condensed-post-card',
  templateUrl: './condensed-post-card.component.html',
  styleUrls: ['./condensed-post-card.component.scss']
})
export class CondensedPostCardComponent implements OnInit {

  @Input() post: Post;

  constructor(public blogPostService: BlogPostService) { }

  ngOnInit(): void {
  }

}
