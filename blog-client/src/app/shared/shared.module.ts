import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LikeSectionComponent } from './components/like-section/like-section.component';
import {MaterialModule} from './modules/material.module';
import { CondensedPostCardComponent } from './components/condensed-post-card/condensed-post-card.component';
import {RouterModule} from '@angular/router';
import { FollowButtonComponent } from './components/follow-button/follow-button.component';

@NgModule({
  declarations: [
    LikeSectionComponent,
    CondensedPostCardComponent,
    FollowButtonComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    MaterialModule
  ],
  exports: [
    LikeSectionComponent,
    CondensedPostCardComponent,
    FollowButtonComponent
  ]
})
export class SharedModule { }
