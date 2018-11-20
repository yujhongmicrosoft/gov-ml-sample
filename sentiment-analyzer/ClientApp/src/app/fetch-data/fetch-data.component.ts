import { Component, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { SentimentApi } from './api.service';
import { Model } from './predData';

@Component({
  selector: 'app-fetch-data',
  templateUrl: './fetch-data.component.html',
  styleUrls: ['./fetch-data.component.css']
})
export class SentimentDataComponent {
  public text: string;
  public predData: Model.PredData;
  public prediction = "2.0";

  constructor(private api: SentimentApi) { }
  ngOnInit() {

  }

  makePrediction() {
    this.api.getPrediction(this.text).subscribe(data => {
      this.predData = (<Model.PredData>data);
      this.prediction = (<Model.PredData>data).prediction;

    });
  }

  getPredClass() {
    if (this.predData != null) {
      if (this.predData.prediction === "0.0") {
        return 'table-danger';
      }
      else {
        return 'table-success';
      }
    }   
  }
}
