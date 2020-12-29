export interface Post {
  id?: number;
  creator_id: number;
  category_id: number;
  title: string;
  // Most of the time text is only needed for detail pages.
  text?: string;
  posted_at?: Date;
  edited_at?: Date;
  thumbnail: string;
}
