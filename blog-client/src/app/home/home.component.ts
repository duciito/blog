import { Component, OnInit } from '@angular/core';
import {Post} from '../posts/models/post';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  popularPosts: Post[];

  constructor() { }

  ngOnInit() {
  }

}
