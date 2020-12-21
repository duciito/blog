import { Component, OnInit } from '@angular/core';
import {FormBuilder, Validators, FormGroup} from '@angular/forms';
import {AccountService} from '../services/account.service';
import {Router} from '@angular/router';
import {User} from '../models/user';
import {first} from 'rxjs/operators';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss', '../../styles/common/auth-form.scss']
})
export class RegisterComponent implements OnInit {

  form: FormGroup;
  serverErrors: any = {};

  constructor(
    private accountService: AccountService,
    private formBuilder: FormBuilder,
    private router: Router
  ) { }

  ngOnInit() {
    this.form = this.formBuilder.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      profileDescription: ['', [Validators.required, Validators.minLength(50)]]
    });
  }

  get f() { return this.form.controls; }

  submit() {
    if (this.form.invalid) {
      return;
    }

    const formData = this.form.value;
    const user: User = {
      username: formData.username,
      email: formData.email,
      password: formData.password,
      first_name: formData.firstName,
      last_name: formData.lastName,
      profile_description: formData.profileDescription,
    };

    this.accountService.register(user)
      .pipe(first())
      .subscribe(
        data => {
          // TODO: check if needed.
          // this.form.reset();
          this.router.navigate(['login'], {queryParams: {afterSignUp: true}});
        },
        error => {
          this.serverErrors = error.error;
          console.log(this.serverErrors);
        }
      )
  }
}
