import {EditableModel} from 'src/app/shared/models/editable-model';

export interface Post extends EditableModel {
  category?: number;
  title: string;
  thumbnail: File | string;
  article_content_ids?: number[];
  total_votes?: number;
  saved?: boolean;
}
