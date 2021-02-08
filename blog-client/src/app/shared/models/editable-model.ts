import {User} from 'src/app/core/models/user';

export interface EditableModel {
  id?: number;
  creator: number | User;
  text?: string;
  posted_at?: Date;
  edited_at?: Date;
  total_votes?: number;
  voted?: boolean;
}
