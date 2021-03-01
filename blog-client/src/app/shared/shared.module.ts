import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LikeSectionComponent } from './components/like-section/like-section.component';
import {MaterialModule} from './modules/material.module';
import { CondensedPostCardComponent } from './components/condensed-post-card/condensed-post-card.component';
import {RouterModule} from '@angular/router';
import { FollowButtonComponent } from './components/follow-button/follow-button.component';
import { DynamicResourceListComponent } from './components/dynamic-resource-list/dynamic-resource-list.component';
import { EmptyMessageComponent } from './components/empty-message/empty-message.component';
import {InfiniteScrollModule} from 'ngx-infinite-scroll';

@NgModule({
  declarations: [
    LikeSectionComponent,
    CondensedPostCardComponent,
    FollowButtonComponent,
    DynamicResourceListComponent,
    EmptyMessageComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    MaterialModule,
    InfiniteScrollModule
  ],
  exports: [
    LikeSectionComponent,
    CondensedPostCardComponent,
    FollowButtonComponent,
    DynamicResourceListComponent,
    EmptyMessageComponent
  ]
})
export class SharedModule { }
