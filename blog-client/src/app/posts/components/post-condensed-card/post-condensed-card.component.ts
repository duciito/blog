import { Component, Input, OnInit } from '@angular/core';
import {Post} from '../../models/post';

@Component({
  selector: 'app-post-condensed-card',
  templateUrl: './post-condensed-card.component.html',
  styleUrls: ['./post-condensed-card.component.scss']
})
export class PostCondensedCardComponent implements OnInit {

  @Input() post: Post;

  constructor() { }

  ngOnInit(): void {
  }

}
