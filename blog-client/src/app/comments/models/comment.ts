import {EditableModel} from 'src/app/shared/models/editable-model';

export interface Comment extends EditableModel {
  article: number;
}
