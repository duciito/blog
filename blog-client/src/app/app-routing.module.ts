import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {AuthGuard} from './core/guards/auth.guard';
import {LoggedinGuard} from './core/guards/loggedin.guard';
import {HomeComponent} from './home/home.component';


const routes: Routes = [
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: HomeComponent,
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
  // TODO: add profile component
  /* {path: 'profile', component: null, canActivate: [AuthGuard]}, */
  // Redirect to home for all undefined paths.
  {path: '**', redirectTo: ''}
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
