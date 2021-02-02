export interface EditableModel {
  id?: number;
  creator: number;
  text?: string;
  posted_at?: Date;
  edited_at?: Date;
  total_votes?: number;
  voted?: boolean;
}
