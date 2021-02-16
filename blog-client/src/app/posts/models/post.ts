import {Category} from 'src/app/categories/models/category';
import {EditableModel} from 'src/app/shared/models/editable-model';

export interface Post extends EditableModel {
  category?: number | Category;
  title: string;
  thumbnail: File | string;
  article_content_ids?: number[];
  total_votes?: number;
  saved?: boolean;
}
