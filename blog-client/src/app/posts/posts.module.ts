import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {QuillModule} from 'ngx-quill';

import { PostsRoutingModule } from './posts-routing.module';
import {CreatePostComponent} from './components/create-post/create-post.component';
import {MaterialModule} from '../shared/modules/material.module';
import {HttpClientModule} from '@angular/common/http';
import {ReactiveFormsModule} from '@angular/forms';
import { ViewPostComponent } from './components/view-post/view-post.component';


@NgModule({
  declarations: [
    CreatePostComponent,
    ViewPostComponent
  ],
  imports: [
    CommonModule,
    PostsRoutingModule,
    ReactiveFormsModule,
    QuillModule.forRoot(),
    MaterialModule
  ]
})
export class PostsModule { }
