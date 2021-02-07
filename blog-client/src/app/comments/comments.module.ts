import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreateCommentComponent } from './components/create-comment/create-comment.component';
import {FormsModule} from '@angular/forms';
import {MaterialModule} from '../shared/modules/material.module';



@NgModule({
  declarations: [CreateCommentComponent],
  imports: [
    CommonModule,
    FormsModule,
    MaterialModule
  ],
  exports: [
    CreateCommentComponent
  ]
})
export class CommentsModule { }
