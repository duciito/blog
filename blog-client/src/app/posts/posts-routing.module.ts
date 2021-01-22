import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {CreatePostComponent} from './components/create-post/create-post.component';
import {ViewPostComponent} from './components/view-post/view-post.component';

const routes: Routes = [
  {path: 'create', component: CreatePostComponent},
  {path: ':id', component: ViewPostComponent},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PostsRoutingModule { }
