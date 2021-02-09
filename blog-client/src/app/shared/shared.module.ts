import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LikeSectionComponent } from './components/like-section/like-section.component';
import {MaterialModule} from './modules/material.module';



@NgModule({
  declarations: [LikeSectionComponent],
  imports: [
    CommonModule,
    MaterialModule
  ],
  exports: [
    LikeSectionComponent
  ]
})
export class SharedModule { }
