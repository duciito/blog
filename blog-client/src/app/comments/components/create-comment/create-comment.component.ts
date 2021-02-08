import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
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
  @Output() commentCreated = new EventEmitter<Comment>();
  comment: Comment;

  constructor(
    private commentService: CommentService
  ) {}

  ngOnInit(): void {
    this.comment = {
      creator: this.loggedUser.id,
      article: this.articleId
    } as Comment;
  }

  submit(form: NgForm) {
    if (form.valid) {
      this.commentService.create(this.comment)
        .subscribe((comment: Comment) => {
          // Reset for subsequent comments if any.
          this.comment.text = undefined;
          this.commentCreated.emit(comment);
        });
    }
  }

}
