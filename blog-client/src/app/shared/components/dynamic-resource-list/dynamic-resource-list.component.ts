import { Component, Input, OnInit } from '@angular/core';
import {ApiResourceLoader} from '../../utils/api-resource-loader';

@Component({
  selector: 'app-dynamic-resource-list',
  templateUrl: './dynamic-resource-list.component.html',
  styleUrls: ['./dynamic-resource-list.component.scss']
})
export class DynamicResourceListComponent implements OnInit {
  @Input() resourceLoader: ApiResourceLoader<any>;
  @Input() infiniteScroll?: boolean = false;

  constructor() { }

  ngOnInit(): void {
  }

}
