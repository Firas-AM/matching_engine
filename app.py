from array import array
from flask import Flask, jsonify, request

app = Flask(__name__)

def bubbleSort_sell(array,array2):
    n = len(array)

    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                array2[j], array2[j + 1] = array2[j + 1], array2[j]
                already_sorted = False
        if already_sorted:
            break
    return array,array2


def bubbleSort_buy(alist,alist2):
    for passnum in range(len(alist)-1,0,-1):
        for i in range(passnum):
            if alist[i]<alist[i+1]:
                temp = alist[i]
                alist[i] = alist[i+1]
                alist[i+1] = temp

                temp2 = alist2[i]
                alist2[i] = alist2[i+1]
                alist2[i+1] = temp2
    return(alist,alist2)


buys_price = []
buys_quantity=[]
sells_price=[]
sells_quantity=[]





@app.route('/sell', methods=['POST'])
def sells():
    global buys_price
    global buys_quantity
    global sells_price
    global sells_quantity
    sell_price = request.json['price']
    sell_quantity = request.json['quantity']
    remove_0 = 0
    for i in range (len(buys_price)):
        if sell_price <= buys_price[i] and sell_quantity >0:
            if buys_quantity[i]>=sell_quantity:
                buys_quantity[i]-=sell_quantity
                sell_quantity = 0
                break
            elif buys_quantity[i]<sell_quantity:
                sell_quantity-=buys_quantity[i]
                buys_quantity[i]=0
                remove_0+=1
            else:
                buys_quantity[i]=0   
                sell_quantity=0
                remove_0+=1
                break

    if sell_price in sells_price:
        index = sells_price.index(sell_price)
        sells_quantity[index]+=sell_quantity
    elif sell_quantity>0:
        sells_price.append(sell_price)
        sells_quantity.append(sell_quantity)
        #sort the sells
    sells_price,sells_quantity = bubbleSort_sell(sells_price,sells_quantity)


    if remove_0>0:
        while remove_0>0:
            for i in range (len(buys_price)):
                if buys_quantity[i]==0:
                    buys_price.pop(i)
                    buys_quantity.pop(i)
                    remove_0-=1
                    break

    for i in range (len(buys_price)):
        if buys_quantity[i]==0:
            buys_price.pop(i)
            buys_quantity.pop(i)
    
    for i in range (len(sells_price)):
        if sells_quantity[i]==0:
            sells_price.pop(i)
            sells_quantity.pop(i)
    return "OK"



@app.route('/book', methods=['GET'])
def book():
    buys =[]
    sells =[]
    for i in range(len(buys_price)):
        buys.append({'qty':buys_quantity[i],'prc':buys_price[i]})
    for i in range(len(sells_price)):
        sells.append({'qty':sells_quantity[i],'prc':sells_price[i]})
    return jsonify({'buys':buys,'sells':sells})

@app.route('/buy', methods=['POST'])
def buys():
    global buys_price
    global buys_quantity
    global sells_price
    global sells_quantity
    buy_price = request.json['price']
    buy_quantity = request.json['quantity']
    remove_0 = 0
    for i in range (len(sells_price)):
        if buy_price >= sells_price[i] and buy_quantity >0:
            if sells_quantity[i]>=buy_quantity:
                sells_quantity[i]-=buy_quantity
                buy_quantity = 0
                break
            elif sells_quantity[i]<buy_quantity:
                buy_quantity-=sells_quantity[i]
                sells_quantity[i]=0
                remove_0+=1
            else:
                sells_quantity[i]=0   
                buy_quantity=0
                remove_0+=1
                break

    #if the price is already in the list, add the quantity to the list
    if buy_price in buys_price:
        buys_quantity[buys_price.index(buy_price)]+=buy_quantity
    elif buy_quantity>0:
        buys_price.append(buy_price)
        buys_quantity.append(buy_quantity)
        #sort the array
        buys_price,buys_quantity = bubbleSort_buy(buys_price,buys_quantity)
    
    if remove_0>0:
        while remove_0>0:
            for i in range (len(sells_price)):
                if sells_quantity[i]==0:
                    sells_price.pop(i)
                    sells_quantity.pop(i)
                    remove_0-=1
                    break
    for i in range (len(buys_price)):
        if buys_quantity[i]==0:
            buys_price.pop(i)
            buys_quantity.pop(i)
    
    for i in range (len(sells_price)):
        if sells_quantity[i]==0:
            sells_price.pop(i)
            sells_quantity.pop(i)
    return "OK"
