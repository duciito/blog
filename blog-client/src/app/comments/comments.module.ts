import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreateCommentComponent } from './components/create-comment/create-comment.component';
import {FormsModule} from '@angular/forms';
import {MaterialModule} from '../shared/modules/material.module';
import { CommentComponent } from './components/comment/comment.component';
import {SharedModule} from '../shared/shared.module';



@NgModule({
  declarations: [CreateCommentComponent, CommentComponent],
  imports: [
    CommonModule,
    FormsModule,
    MaterialModule,
    SharedModule
  ],
  exports: [
    CreateCommentComponent,
    CommentComponent
  ]
})
export class CommentsModule { }
