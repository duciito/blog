import { Component, OnDestroy, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {FileValidator} from 'ngx-material-file-input';
import {ToastrService} from 'ngx-toastr';
import {Observable} from 'rxjs';
import {Category} from '../models/category';
import {BlogPostService} from '../services/blog-post.service';
import {CategoryService} from '../services/category.service';
import Quill from 'quill';
import {ImageFormat} from './image-format';
import {ImageHandler, Options} from 'ngx-quill-upload';
import {ArticleContent} from '../models/article-content';
import ImageResize from 'quill-image-resize';
import {first} from 'rxjs/operators';
import {Post} from '../models/post';
import {defaultErrorHandler} from '../helpers/default-error-handler';

Quill.register('modules/imageHandler', ImageHandler);
Quill.register('modules/imageResize', ImageResize);
Quill.register(ImageFormat, true);

// Force quill to use inline styling.
const DirectionAttribute = Quill.import('attributors/attribute/direction');
Quill.register(DirectionAttribute,true);

const AlignClass = Quill.import('attributors/class/align');
Quill.register(AlignClass,true);

const BackgroundClass = Quill.import('attributors/class/background');
Quill.register(BackgroundClass,true);

const ColorClass = Quill.import('attributors/class/color');
Quill.register(ColorClass,true);

const DirectionClass = Quill.import('attributors/class/direction');
Quill.register(DirectionClass,true);

const FontClass = Quill.import('attributors/class/font');
Quill.register(FontClass,true);

const SizeClass = Quill.import('attributors/class/size');
Quill.register(SizeClass,true);

const AlignStyle = Quill.import('attributors/style/align');
Quill.register(AlignStyle,true);

const BackgroundStyle = Quill.import('attributors/style/background');
Quill.register(BackgroundStyle,true);

const ColorStyle = Quill.import('attributors/style/color');
Quill.register(ColorStyle,true);

const DirectionStyle = Quill.import('attributors/style/direction');
Quill.register(DirectionStyle,true);

const FontStyle = Quill.import('attributors/style/font');
Quill.register(FontStyle,true);

const SizeStyle = Quill.import('attributors/style/size');
Quill.register(SizeStyle,true);

@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.scss']
})
export class CreatePostComponent implements OnInit, OnDestroy {

  readonly acceptedImgFormats: string[] = ['image/png', 'image/jpg', 'image/jpeg'];
  form: FormGroup;
  categories$: Observable<Category[]>;
  temporaryContents: ArticleContent[] = [];
  thumbnailFile: File;

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
      title: ['', [Validators.required, Validators.minLength(3)]],
      category: [null, Validators.required],
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

    const formData = Object.assign(
      this.form.value,
      {thumbnail: this.thumbnailFile}
    );

    const post = this.temporaryContents.length 
      ? Object.assign(
          // Asssign all images uploaded in editor
          // to associate with the newly created article
          // on the back-end.
          {article_content_ids: this.temporaryContents.map(content => content.id)},
          formData
        ) as Post
      : formData;

    this.blogPostService.create(post)
      .pipe(first())
      .subscribe(
        data => {
          // Empty temporary contents so that they don't get deleted
          // when the redirect below happens (it calls ngOnDestroy).
          this.temporaryContents = [];
          this.router.navigate(['']);
          this.toastr.success("Successfully created a new blog post!");
        },
        error => {
          if (error.status.startsWith('5')) {
            // There may be some cases where it's already been cleand up
            // by the server since it's an atomic transaction.
            this.cleanUpImgOrphans();
            this.toastr.error('Please try again later', 'Server error');
          }
          else {
            defaultErrorHandler(error, this.toastr);
          }
        }
      )
  }

  onThumbnailSelect(event) {
    // Write thumbnail to actual File object on change.
    if (event.target.files.length) {
      this.thumbnailFile = event.target.files[0];
    }
  }

  cleanUpImgOrphans() {
    if (this.temporaryContents.length) {
      for (const content of this.temporaryContents) {
        this.blogPostService.removeContent(content.id).subscribe();
      }
    }
  }

  ngOnDestroy() {
    this.cleanUpImgOrphans();
  }
}
