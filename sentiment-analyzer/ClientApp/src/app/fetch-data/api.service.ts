import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { HttpParams } from "@angular/common/http";
import { Model } from './predData';

@Injectable()
export class SentimentApi {

  constructor(private http: HttpClient) { }

  getPrediction(input) {
    const myheader = new HttpHeaders().set("Content-Type", 'application/json')
    let body = new HttpParams();
    let inputText = new Model.Input();
    inputText.text = input;
    return this.http.post('/api/Sentiment/predict', JSON.stringify(inputText), {
      headers: myheader});
  }
}
