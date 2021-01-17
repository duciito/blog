import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {CreatePostComponent} from './components/create-post/create-post.component';

const routes: Routes = [
  {path: 'create', component: CreatePostComponent},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PostsRoutingModule { }
