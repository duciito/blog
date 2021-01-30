export interface Post {
  id?: number;
  creator: number;
  category?: number;
  title: string;
  // Most of the time text is only needed for detail pages.
  text?: string;
  posted_at?: Date;
  edited_at?: Date;
  thumbnail: File | string;
  article_content_ids?: number[];
  total_votes?: number;
  voted?: boolean;
}
