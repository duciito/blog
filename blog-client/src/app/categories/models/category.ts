import {FollowableModel} from 'src/app/shared/models/followable-model';

export interface Category extends FollowableModel {
  id?: number;
  name: string;
}
