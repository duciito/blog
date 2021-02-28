import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ProfileRoutingModule } from './profile-routing.module';
import { ProfileComponent } from './components/profile/profile.component';
import { SavedPostsComponent } from './components/saved-posts/saved-posts.component';
import {SharedModule} from '../shared/shared.module';
import {MaterialModule} from '../shared/modules/material.module';


@NgModule({
  declarations: [ProfileComponent, SavedPostsComponent],
  imports: [
    CommonModule,
    ProfileRoutingModule,
    SharedModule,
    MaterialModule
  ]
})
export class ProfileModule { }
