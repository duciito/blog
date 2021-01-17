import { Component, OnInit } from '@angular/core';
import {FormBuilder, Validators, FormGroup} from '@angular/forms';
import {Router} from '@angular/router';
import {first} from 'rxjs/operators';
import {ToastrService} from 'ngx-toastr';
import {AccountService} from 'src/app/core/services/account.service';
import {User} from 'src/app/core/models/user';
import {defaultErrorHandler} from 'src/app/shared/utils/default-error-handler';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss', '../../../../styles/common/auth-form.scss']
})
export class RegisterComponent implements OnInit {

  form: FormGroup;

  constructor(
    private accountService: AccountService,
    private formBuilder: FormBuilder,
    private router: Router,
    private toastr: ToastrService
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
          this.router.navigate(['auth/login', {afterSignUp: true}]);
        },
        error => defaultErrorHandler(error, this.toastr)
      )
  }
}
