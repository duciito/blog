import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {QuillModule} from 'ngx-quill';

import { PostsRoutingModule } from './posts-routing.module';
import {CreatePostComponent} from './components/create-post/create-post.component';
import {MaterialModule} from '../shared/modules/material.module';
import {HttpClientModule} from '@angular/common/http';
import {ReactiveFormsModule} from '@angular/forms';
import { ViewPostComponent } from './components/view-post/view-post.component';
import { NoSanitizePipe } from './pipes/no-sanitize.pipe';
import {CommentsModule} from '../comments/comments.module';
import {SharedModule} from '../shared/shared.module';
import {InfiniteScrollModule} from 'ngx-infinite-scroll';
import { PostCondensedCardComponent } from './components/post-condensed-card/post-condensed-card.component';


@NgModule({
  declarations: [
    CreatePostComponent,
    ViewPostComponent,
    NoSanitizePipe,
    PostCondensedCardComponent
  ],
  imports: [
    CommonModule,
    PostsRoutingModule,
    ReactiveFormsModule,
    QuillModule.forRoot(),
    MaterialModule,
    CommentsModule,
    SharedModule,
    InfiniteScrollModule
  ],
  exports: [
    PostCondensedCardComponent
  ]
})
export class PostsModule { }
