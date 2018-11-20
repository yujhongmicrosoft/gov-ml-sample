using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Text;
using Newtonsoft.Json;

namespace sentiment_analyzer.Controllers
{
    public class RawInput
    {
        [JsonProperty(PropertyName = "text")]
        public string Text { get; set; }
    }

    public class RawPrediction
    {
        [JsonProperty(PropertyName = "prediction")]
        public string Prediction { get; set; }
        [JsonProperty(PropertyName = "predictionVector")]
        public string[] PredictionVector { get; set; }
    }

    [Route("api/[controller]")]
    public class SentimentController : Controller
    {
        private static readonly HttpClient client = new HttpClient();


        [HttpPost("predict")]
        public async Task<IActionResult> GetPrediction([FromBody] RawInput input)
        {
            var jsonInput = "{" + "\"" + input.Text + "\"" + "}";
            var content = new StringContent(jsonInput, Encoding.UTF8, "application/json");
            var response = await client.PostAsync("http://bridgedemo.usgovvirginia.cloudapp.usgovcloudapi.net:8003/predict", content);
            var rawpred = await response.Content.ReadAsStringAsync();
            var predString = Regex.Matches(rawpred, @"(?<=probability=DenseVector\()(.*)", RegexOptions.IgnoreCase);
            var predictionVector = Regex.Matches(predString[0].ToString(), @"(?<=\[)(.*)(?=\]\),)", RegexOptions.IgnoreCase);
            var prediction = Regex.Matches(predString[0].ToString(), @"(?<=prediction=)(.*)(?=\))", RegexOptions.IgnoreCase);
            RawPrediction pred = new RawPrediction();
            pred.Prediction = prediction[0].ToString();
            pred.PredictionVector = predictionVector[0].ToString().Split(",");
            return Ok(pred);
        }

  
    }
}
