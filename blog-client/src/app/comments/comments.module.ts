import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreateCommentComponent } from './components/create-comment/create-comment.component';
import {FormsModule} from '@angular/forms';
import {MaterialModule} from '../shared/modules/material.module';
import { CommentComponent } from './components/comment/comment.component';



@NgModule({
  declarations: [CreateCommentComponent, CommentComponent],
  imports: [
    CommonModule,
    FormsModule,
    MaterialModule
  ],
  exports: [
    CreateCommentComponent,
    CommentComponent
  ]
})
export class CommentsModule { }
