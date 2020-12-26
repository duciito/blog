import { Component, OnInit } from '@angular/core';
import {AccountService} from '../services/account.service';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Router, ActivatedRoute} from '@angular/router';
import {first} from 'rxjs/operators';
import {ToastrService} from 'ngx-toastr';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss', '../../styles/common/auth-form.scss']
})
export class LoginComponent implements OnInit {

  form: FormGroup;
  returnUrl: string;

  constructor(
    private accountService: AccountService,
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private toastr: ToastrService
  ) { }

  ngOnInit() {
    this.form = this.formBuilder.group({
      email: ['', Validators.required],
      password: ['', Validators.required]
    });

    // Get return url or redirect to home if none
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '';

    if (this.route.snapshot.params['afterSignUp']) {
      this.toastr.success("You registered successfully. You can now login.");
    }
  }

  get f() {return this.form.controls;}

  submit() {
    if (this.form.invalid) {
      return;
    }

    this.accountService.login(this.f.email.value, this.f.password.value)
      .pipe(first())
      .subscribe(
        data => {
          this.router.navigate([this.returnUrl]);
        },
        error => {
          const errors: any = [...Object.values(error.error || error)].reduce(
            (acc: string[], val: string) => acc.concat(val), []
          );

          errors.forEach(error => this.toastr.error(error));
        }
      )
  }

}
