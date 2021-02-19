import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ViewCategoryComponent} from './components/view-category/view-category.component';

const routes: Routes = [
  {path: ':id', component: ViewCategoryComponent},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CategoriesRoutingModule { }
