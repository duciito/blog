import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {FileValidator} from 'ngx-material-file-input';
import {ToastrService} from 'ngx-toastr';
import {Observable} from 'rxjs';
import {Category} from '../models/category';
import {BlogPostService} from '../services/blog-post.service';
import {CategoryService} from '../services/category.service';
import Quill from 'quill';
import {ImageHandler, Options} from 'ngx-quill-upload';
import {ArticleContent} from '../models/article-content';
import ImageResize from 'quill-image-resize';
import {first} from 'rxjs/operators';

Quill.register('modules/imageHandler', ImageHandler);
Quill.register('modules/imageResize', ImageResize);

@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.scss']
})
export class CreatePostComponent implements OnInit {

  readonly acceptedImgFormats: string[] = ['image/png', 'image/jpg', 'image/jpeg'];
  form: FormGroup;
  categories$: Observable<Category[]>;
  temporaryContents: ArticleContent[] = [];

  quillOptions = {
    imageHandler: {
      upload: file => {
        // Image handler only works with promises
        return new Promise((resolve, reject) => {
          if (this.acceptedImgFormats.includes(file.type)) {
            const articleContent = {
              file: file,
              content_type: "image"
            } as ArticleContent;

            return this.blogPostService.uploadContent(articleContent)
            .pipe(first())
            .subscribe(
              (content: ArticleContent) => {
                this.temporaryContents.push(content);
                resolve(content.file);
              },
              error => {
                reject("Image failed to upload.");
                this.toastr.error("Image failed to upload. Please try again.");
              }
            )
          }
          else {
            reject("Unsupported format");
            this.toastr.error("Unsupported image format.");
          }
        });
      },
      accepts: this.acceptedImgFormats
    } as Options,
    imageResize: true
  };

  contentChanged($event) {console.log($event);}

  constructor(
    private blogPostService: BlogPostService,
    private categoryService: CategoryService,
    private formBuilder: FormBuilder,
    private router: Router,
    private toastr: ToastrService
  ) { }

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      title: ['', [Validators.required, Validators.minLength(10)]],
      category_id: [null, Validators.required],
      thumbnail: [null, [
        Validators.required,
        // Max 5MB for thumbnails
        FileValidator.maxContentSize(5242880)
      ]],
      text: ['']
    });

    this.categories$ = this.categoryService.getAll();
  }

  get f() {return this.form.controls;}

  submit() {
    if (this.form.invalid) {
      return;
    }
  }
}
