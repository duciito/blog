import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {ToastrModule} from 'ngx-toastr';
import {CoreModule} from './core/core.module';
import {MaterialModule} from './shared/modules/material.module';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    CoreModule,
    ToastrModule.forRoot({
      timeOut: 6300,
      positionClass: 'toast-bottom-right',
      preventDuplicates: true
    }),
    MaterialModule
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
