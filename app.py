from flask import Flask,request,jsonify
import requests,json

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    data  = request.get_json()
    print(type(data))
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency =  data['queryResult']['parameters']['currency-name']    
    
    converion_amt = fetch_conversion_factor(source_currency,target_currency,amount)
    final_amt = round(converion_amt,2)
    response = { "fulfillmentText":"{} {} is {} {}".format(amount,source_currency,final_amt,target_currency)}
    return jsonify(response)

def fetch_conversion_factor(source,target,amount):
    url = "https://api.apilayer.com/currency_data/convert?to={}&from={}&amount={}".format(target,source,amount)
    payload = {}
    headers= {"apikey": "i0CGJDtJ9L6v6mIib0pGfjHZmmtN1QLN"}

    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    result = response.text

    res = json.loads(result)
    amt = res['result']
    return amt

   


if __name__ == "__main__":
    app.run(debug=True) 