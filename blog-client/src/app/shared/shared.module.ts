import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LikeSectionComponent } from './components/like-section/like-section.component';
import {MaterialModule} from './modules/material.module';
import { CondensedPostCardComponent } from './components/condensed-post-card/condensed-post-card.component';

@NgModule({
  declarations: [
    LikeSectionComponent,
    CondensedPostCardComponent
  ],
  imports: [
    CommonModule,
    MaterialModule
  ],
  exports: [
    LikeSectionComponent,
    CondensedPostCardComponent
  ]
})
export class SharedModule { }
