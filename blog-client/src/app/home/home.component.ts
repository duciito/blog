import { Component, OnInit } from '@angular/core';
import {Observable} from 'rxjs';
import {Post} from '../posts/models/post';
import {BlogPostService} from '../posts/services/blog-post.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  popularPosts$: Observable<Post[]>;

  constructor(
    private blogPostService: BlogPostService
  ) { }

  ngOnInit() {
    this.popularPosts$ = this.blogPostService.hot({nested: true});
  }

}
