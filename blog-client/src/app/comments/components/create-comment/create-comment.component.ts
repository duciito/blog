import { Component, Input, OnInit } from '@angular/core';
import {NgForm} from '@angular/forms';
import {User} from 'src/app/core/models/user';
import {Comment} from '../../models/comment';
import {CommentService} from '../../services/comment.service';

@Component({
  selector: 'app-create-comment',
  templateUrl: './create-comment.component.html',
  styleUrls: ['./create-comment.component.scss']
})
export class CreateCommentComponent implements OnInit {

  @Input() loggedUser: User;
  @Input() articleId: number;
  comment: Comment;

  constructor(
    private commentService: CommentService
  ) {}

  ngOnInit(): void {
    this.comment = {
      text: '',
      creator: this.loggedUser.id,
      article: this.articleId
    } as Comment;
  }

  submit(form: NgForm) {
    if (form.valid) {
      this.commentService.create(this.comment)
        .subscribe(success => {
          // Reset for subsequent comments if any.
          this.comment.text = '';
        });
    }
  }

}
