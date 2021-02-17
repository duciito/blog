import { Component, Input, OnInit } from '@angular/core';
import {VotableServiceMixin} from '../../mixins/votable-service-mixin';
import {EditableModel} from '../../models/editable-model';

@Component({
  selector: 'app-like-section',
  templateUrl: './like-section.component.html',
  styleUrls: ['./like-section.component.scss']
})
export class LikeSectionComponent implements OnInit {

  @Input() model: EditableModel;
  @Input() service: VotableServiceMixin;
  @Input() compact: boolean = false;

  constructor() { }

  ngOnInit(): void {
  }

  vote() {
    /* debugger; */
    const voteFunc = (this.model.voted
      ? this.service.unvote
      : this.service.vote).bind(this.service);

    voteFunc(this.model.id)
      .subscribe(
        () => {
          this.model.voted = !this.model.voted;

          // Increase or decrease total vote count.
          this.model.total_votes = this.model.voted
            ? this.model.total_votes + 1
            : this.model.total_votes - 1;
        }
      );
  }
}
