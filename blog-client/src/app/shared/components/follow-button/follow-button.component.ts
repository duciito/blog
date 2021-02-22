import { Component, Input, OnInit } from '@angular/core';
import {FollowableServiceMixin} from '../../mixins/followable-service-mixin';

@Component({
  selector: 'app-follow-button',
  templateUrl: './follow-button.component.html',
  styleUrls: ['./follow-button.component.scss']
})
export class FollowButtonComponent implements OnInit {
  @Input() model: any;
  @Input() service: FollowableServiceMixin;

  constructor() { }

  ngOnInit(): void {
  }

  follow() {
    const followFunc = (this.model.followed
      ? this.service.unfollow
      : this.service.follow).bind(this.service);

    followFunc(this.model.id)
      .subscribe(
        () => {
          this.model.followed = !this.model.followed;

          // Increase or decrease total followers count.
          this.model.total_followers = this.model.followed
            ? this.model.total_followers + 1
            : this.model.total_followers - 1;
        }
      );
  }
}
