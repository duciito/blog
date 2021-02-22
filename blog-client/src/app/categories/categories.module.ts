import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CategoriesRoutingModule } from './categories-routing.module';
import { ViewCategoryComponent } from './components/view-category/view-category.component';
import {SharedModule} from '../shared/shared.module';
import {MaterialModule} from '../shared/modules/material.module';


@NgModule({
  declarations: [ViewCategoryComponent],
  imports: [
    CommonModule,
    CategoriesRoutingModule,
    SharedModule,
    MaterialModule
  ]
})
export class CategoriesModule { }
