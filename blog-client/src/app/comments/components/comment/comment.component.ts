import { Component, Input, OnInit } from '@angular/core';
import {User} from 'src/app/core/models/user';
import {Comment} from '../../models/comment';

@Component({
  selector: 'app-comment',
  templateUrl: './comment.component.html',
  styleUrls: ['./comment.component.scss']
})
export class CommentComponent implements OnInit {

  @Input() comment: Comment;
  @Input() loggedUserId: number;
  @Input() articleCreatorId: number;
  userType: string;

  constructor() { }

  ngOnInit(): void {
    const creator = this.comment.creator as User;

    if (creator.id === this.loggedUserId) {
      this.userType = 'you';
    }
    else if (creator.id === this.articleCreatorId) {
      this.userType = 'author';
    }
  }

}
