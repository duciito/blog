import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {AuthGuard} from './core/guards/auth.guard';
import {LoggedinGuard} from './core/guards/loggedin.guard';

const routes: Routes = [
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    loadChildren: () => import('src/app/home/home.module').then(m => m.HomeModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'auth',
    loadChildren: () => import('src/app/auth/auth.module').then(m => m.AuthModule),
    canActivate: [LoggedinGuard]
  },
  {
    path: 'posts',
    loadChildren: () => import('src/app/posts/posts.module').then(m => m.PostsModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'categories',
    loadChildren: () => import('src/app/categories/categories.module').then(m => m.CategoriesModule),
    canActivate: [AuthGuard]
  },
  // Redirect to home for all undefined paths.
  {path: '**', redirectTo: ''}
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
