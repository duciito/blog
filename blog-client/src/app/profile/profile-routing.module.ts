import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ProfileComponent} from './components/profile/profile.component';
import {SavedPostsComponent} from './components/saved-posts/saved-posts.component';

const routes: Routes = [
  {path: ':id', component: ProfileComponent},
  {path: 'saved', component: SavedPostsComponent},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProfileRoutingModule { }
