# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 00:35:48 2018

@author: miyazawa kazuya
"""
#参考：https://swap.tech/whitepaper/


import hashlib

class Tradedemo2(object):
    def __init__(self):
        self.owner = set()
        self.walletlist = []
        self.takerorderlist = []
        self.makerorderlist = []
        self.intentlist = []
        #a-b a1単位あたりのbの価格
        self.rate = {
                "money1-money2":2, 
                }
        
    #メイカーに送るテイカー側の注文
    #テイカーのアドレス、テイカーが払うトークン、メイカーが払う量、メイカーが払うトークン    
    def takerorder(self, taker, takertoken, makeramount, makertoken, number=None, takeramount=None):
        if number != None:
            for i in self.intentlist:
                if i["number"] == number:
                    if i["takerrate"] != None:
                        takeramount = makeramount*i["takerrate"]
        takerorder ={
                "taker":taker, 
                "takertoken":takertoken, 
                "makeramount":makeramount, 
                "makertoken":makertoken, 
                "takeramount":takeramount, 
                "number":number, 
                }
        self.takerorderlist.append(takerorder)
        return takerorder
    
    #メイカーからテイカーへの注文承諾　これ送ることでテイカーは取引できるようになる
    #メイカーのアドレス、テイカーが払うトークン、メイカーが払う量、メイカーが払うトークン、テイカーが払う量、テイカーのアドレス、パスワード
    def makerorder(self, maker, takertoken, makeramount, makertoken, takeramount, taker, password):
        makerorder ={
                "maker":maker, 
                "takertoken":takertoken, 
                "makeramount":makeramount, 
                "makertoken":makertoken, 
                "takeramount":takeramount, 
                "taker":taker, 
                "password":password, 
                }
        self.makerorderlist.append(makerorder)
        return makerorder

    #メイカーが取引の意思を示す メイカーのアドレス、メイカーが払うトークン、テイカーが払うトークン、意思番号、パスワード
    #、メイカーが最大で払えるトークン量、テイカーが払うトークンのメイカーが払うトークン比(レート) この2つは公開自由
    #レート例：メイカーbtc,テイカーjpy 1btc100万円みたいな
    def addintent(self, maker, makertoken, takertoken, number, password, maxmakeramount=None, takerrate=None):
        password = f'{password}'.encode()
        addintent = {
                "number":number, 
                "maker":maker, 
                "makertoken":makertoken, 
                "takertoken":takertoken, 
                "maxmakeramount":maxmakeramount, 
                "takerrate":takerrate, 
                "password": hashlib.sha256(password).hexdigest()
                }
        self.intentlist.append(addintent)
        return addintent
    
    #意思の取り消し 取引意思表明の時と引数同じ
    def removeintent(self, maker, makertoken, takertoken, number, password, makeramount=None, maxmakeramount=None, takerrate=None):
        password = f'{password}'.encode()
        removeintent = {
                "number":number, 
                "maker":maker, 
                "makertoken":makertoken, 
                "takertoken":takertoken, 
                "maxmakeramount":maxmakeramount, 
                "takerrate":takerrate, 
                "password": hashlib.sha256(password).hexdigest()
                }
        for i in self.intentlist:
            if i == removeintent:
                self.intentlist.remove(i)

    #メイカーの取引意思のリスト
    def watchintent(self):
        return self.intentlist
    
    #特定トークンを取引する意思のあるメイカーを見つける 最低限の販売トークン量と最大限のトークンレート
    #Noneがあるかないかで条件分岐
    def findintent(self, makertoken, takertoken, loweramount=None, upperrate=None):
        findlist = [["number", "maker", "maxmakeramount", "takerrate"]]
        for i in self.intentlist:
            if loweramount==None and upperrate==None: 
                if i["makertoken"] == makertoken and i["takertoken"] == takertoken:
                    findlist.append([i["number"],i["maker"],i["maxmakeramount"],i["takerrate"]])
            elif loweramount==None:
                if i["makertoken"] == makertoken and i["takertoken"] == takertoken and i["takerrate"]<=upperrate:
                    findlist.append([i["number"],i["maker"],i["maxmakeramount"],i["takerrate"]])
            elif upperrate==None:
                if i["makertoken"] == makertoken and i["takertoken"] == takertoken and i["maxmakeramount"]>=loweramount:
                    findlist.append([i["number"],i["maker"],i["maxmakeramount"],i["takerrate"]])
            else:
                if i["makertoken"] == makertoken and i["takertoken"] == takertoken and i["maxmakeramount"]>=loweramount and i["takerrate"]<=upperrate:
                    findlist.append([i["number"],i["maker"],i["maxmakeramount"],i["takerrate"]])
        return findlist
    
    def makewallet(self, owner, money1, money2):
        #wallet作る 誰が、いくら持っているかは打ち込む
        wallet = {
                "owner":owner, 
                "m1":money1, 
                "m2":money2, 
                }
        #walletlistに作ったウォレット保存
        self.walletlist.append(wallet)
        return wallet
    
    def checkwallet(self, checkowner):
        #ウォレットチェック
        #所持ウォレット数
        num = 0
        #所持ウォレットリスト
        cwlist = []    
        #もしウォレットの所持者名あっていればリストに加える
        for w in self.walletlist:
            if w["owner"] == checkowner:
                num += 1
                cwlist.append(w)
            
        if num == 0:
            return "You have no wallet!"
        else:
            return cwlist
   

    def trademoney(self, password):
        #makerorderのパスワード入れてその情報使って取引
        for o in self.makerorderlist:
            if o["password"] == password:
                maker = o["maker"]
                takertoken = o["takertoken"]
                makeramount = o["makeramount"]
                makertoken = o["makertoken"]
                takeramount = o["takeramount"]
                taker = o["taker"]
        takerwallet = None
        makerwallet = None

        #送り主のウォレットと交換してくれる側のウォレットget　セキュリティとかはとりあえず無視　複数ウォレットもとりあえず無視
        for w in self.walletlist:
            if w["owner"] == taker:
                takerwallet = w
            if w["owner"] == maker:
                makerwallet = w
        #もしウォレットなかったら終わり
        if takerwallet is None:
            return "You have no wallet!"
        if makerwallet is None:
            return "There is no maker's wallet."
        #送る金持ってなかったり交換する金なかったら終わり
        if takertoken in takerwallet == False:
            return "You have no sendmoney."
        if makertoken in makerwallet == False:
            return "Maker has no changemoney."
        if takeramount > takerwallet[takertoken]:
            return "You don't have sufficient changemoney."
        if makeramount > makerwallet[makertoken]:
            return "Maker doesn't have sufficient sendmoney."
        #もし受け取る通貨のウォレットなかったら作らないと とりあえずエラーでいい
        if makertoken in takerwallet == False:
            return "You don't have gettoken wallet"
        if takertoken in makerwallet == False:
            return "Maker doesn't sendtoken wallet"
        
        takerwallet[makertoken] = takerwallet[makertoken]+makeramount
        makerwallet[makertoken] = makerwallet[makertoken]-makeramount
        
        takerwallet[takertoken] = takerwallet[takertoken]-takeramount
        makerwallet[takertoken] = makerwallet[takertoken]+takeramount
        
        return "Trade!"
        
   
     
tradedemo = Tradedemo2()

tradedemo.makewallet("p1",10,10)
#tradedemo1.makewallet("p1",10,10)
tradedemo.makewallet("p2",10,10)
tradedemo.makewallet("p3",10,10)
tradedemo.makewallet("p4",10,10)
tradedemo.makewallet("p5",10,10)
print(tradedemo.checkwallet("p1"))
print(tradedemo.checkwallet("p2"))



print(tradedemo.addintent("p1", "m1", "m2", 1, "pass1"))
print(tradedemo.addintent("p2", "m1", "m2", 2, "pass2", 1))
print(tradedemo.watchintent())
tradedemo.removeintent("p1", "m1", "m2", 1, "pass1")
print(tradedemo.watchintent())
print(tradedemo.addintent("p3", "m1", "m2", 3, "pass2", 3, 2))
print(tradedemo.addintent("p4", "m1", "m2", 4, "pass2", 5, 2))
print(tradedemo.addintent("p5", "m1", "m2", 5, "pass2", 10, 3))
print(tradedemo.watchintent())
print(tradedemo.findintent("m1", "m2", 2, 2.5))
print(tradedemo.takerorder("p1", "m1", 2, "m2", 3))
print(tradedemo.makerorder("p3", "m1", 2, "m2", 4, "p1", "pa1"))
print(tradedemo.trademoney("pa1"))
print(tradedemo.checkwallet("p1"))
print(tradedemo.checkwallet("p3"))




