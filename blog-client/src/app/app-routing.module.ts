import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {LoginComponent} from './login/login.component';
import {RegisterComponent} from './register/register.component';
import {AuthGuard} from './helpers/auth.guard';
import {HomeComponent} from './home/home.component';
import {LoggedinGuard} from './helpers/loggedin.guard';
import {CreatePostComponent} from './create-post/create-post.component';


const routes: Routes = [
  {path: '' , redirectTo: '/home', pathMatch: 'full'},
  {path: 'home', component: HomeComponent, canActivate: [AuthGuard]},
  {path: 'create-post', component: CreatePostComponent, canActivate: [AuthGuard]},
  {path: 'login', component: LoginComponent, canActivate: [LoggedinGuard]},
  {path: 'register', component: RegisterComponent, canActivate: [LoggedinGuard]},
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
