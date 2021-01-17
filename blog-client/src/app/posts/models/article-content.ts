export interface ArticleContent {
  id?: number;
  article_id?: number;
  content_type: "image" | "video";
  // URL
  file: any;
  guid?: string;
}
