# -*- coding:  utf-8 -*-
'''
Created on Sun Mar  4 00: 35: 48 2018

@author:  miyazawa kazuya
'''
#参考：https: //swap.tech/whitepaper/


import hashlib

class tradeDemo2(object):

    def __init__(self):
        self.owner = set()
        self.walletList = []
        self.takerOrderList = []
        self.makerOrderList = []
        self.intentList = []

        #a-b a1単位あたりのbの価格
        self.rate = {
            'money1-money2': 2,
        }


    #メイカーに送るテイカー側の注文
    #テイカーのアドレス、テイカーが払うトークン、メイカーが払う量、メイカーが払うトークン
    def takerOrder(self, taker, takerToken, makerAmount, makerToken, number=None, takerAmount=None):
        if number != None:
            for i in self.intentList:
                if i['number'] == number and i['takerRate'] != None:
                    takerAmount = makerAmount * i['takerRate']

        takerOrder = {
            'taker': taker,
            'takerToken': takerToken,
            'makerAmount': makerAmount,
            'makerToken': makerToken,
            'takerAmount': takerAmount,
            'number': number
        }

        self.takerOrderList.append(takerOrder)
        return takerOrder


    #メイカーからテイカーへの注文承諾　これ送ることでテイカーは取引できるようになる
    #メイカーのアドレス、テイカーが払うトークン、メイカーが払う量、メイカーが払うトークン、テイカーが払う量、テイカーのアドレス、パスワード
    def makerOrder(self, maker, takerToken, makerAmount, makerToken, takerAmount, taker, password):
        makerOrder = {
            'maker': maker,
            'takerToken': takerToken,
            'makerAmount': makerAmount,
            'makerToken': makerToken,
            'takerAmount': takerAmount,
            'taker': taker,
            'password': password
        }

        self.makerOrderlist.append(makerOrder)
        return makerOrder


    #メイカーが取引の意思を示す メイカーのアドレス、メイカーが払うトークン、テイカーが払うトークン、意思番号、パスワード
    #、メイカーが最大で払えるトークン量、テイカーが払うトークンのメイカーが払うトークン比(レート) この2つは公開自由
    #レート例：メイカーbtc,テイカーjpy 1btc100万円みたいな
    def addIntent(self, maker, makerToken, takerToken, number, password, maxMakerAmount=None, takerRate=None):
        password = f'{password}'.encode()
        addIntent = {
            'number': number,
            'maker': maker,
            'makerToken': makerToken,
            'takerToken': takerToken,
            'maxMakerAmount': maxMakerAmount,
            'takerRate': takerRate,
            'password':  hashlib.sha256(password).hexdigest()
        }

        self.intentList.append(addIntent)
        return addIntent


    #意思の取り消し 取引意思表明の時と引数同じ
    def removeIntent(self, maker, makerToken, takerToken, number, password, makerAmount=None, maxMakerAmount=None, takerRate=None):
        password = f'{password}'.encode()
        removeIntent = {
            'number': number,
            'maker': maker,
            'makerToken': makerToken,
            'takerToken': takerToken,
            'maxMakerAmount': maxMakerAmount,
            'takerRate': takerRate,
            'password':  hashlib.sha256(password).hexdigest()
        }

        for i in self.intentList:
            if i == removeIntent:
                self.intentList.remove(i)


    #メイカーの取引意思のリスト
    def watchIntent(self):
        return self.intentList


    #特定トークンを取引する意思のあるメイカーを見つける 最低限の販売トークン量と最大限のトークンレート
    #Noneがあるかないかで条件分岐
    def findIntent(self, makerToken, takerToken, lowerAmount=None, upperRate=None):
        findlist = [['number', 'maker', 'maxMakerAmount', 'takerRate']]

        for i in self.intentList:
            if lowerAmount==None and upperRate==None:
                if i['makerToken'] == makerToken and i['takerToken'] == takerToken:
                    findlist.append([i['number'],i['maker'],i['maxMakerAmount'],i['takerRate']])
            elif lowerAmount==None:
                if i['makerToken'] == makerToken and i['takerToken'] == takerToken and i['takerRate']<=upperRate:
                    findlist.append([i['number'],i['maker'],i['maxMakerAmount'],i['takerRate']])
            elif upperRate==None:
                if i['makerToken'] == makerToken and i['takerToken'] == takerToken and i['maxMakerAmount']>=lowerAmount:
                    findlist.append([i['number'],i['maker'],i['maxMakerAmount'],i['takerRate']])
            else:
                if i['makerToken'] == makerToken and i['takerToken'] == takerToken and i['maxMakerAmount']>=lowerAmount and i['takerRate']<=upperRate:
                    findlist.append([i['number'],i['maker'],i['maxMakerAmount'],i['takerRate']])

        return findlist


    def makeWallet(self, owner, money1, money2):
        #wallet作る 誰が、いくら持っているかは打ち込む
        wallet = {
            'owner': owner,
            'm1': money1,
            'm2': money2
        }

        #walletListに作ったウォレット保存
        self.walletList.append(wallet)
        return wallet


    def checkWallet(self, checkOwner):
        #ウォレットチェック
        #所持ウォレット数
        num = 0
        #所持ウォレットリスト
        cwlist = []
        #もしウォレットの所持者名あっていればリストに加える
        for w in self.walletList:
            if w['owner'] == checkOwner:
                num += 1
                cwlist.append(w)

        if num == 0:
            return 'You have no wallet!'
        else:
            return cwlist


    def trademoney(self, password):
        #makerOrderのパスワード入れてその情報使って取引
        for o in self.makerOrderlist:
            if o['password'] == password:
                maker = o['maker']
                takerToken = o['takerToken']
                makerAmount = o['makerAmount']
                makerToken = o['makerToken']
                takerAmount = o['takerAmount']
                taker = o['taker']
        takerWallet = None
        makerWallet = None

        #送り主のウォレットと交換してくれる側のウォレットget　セキュリティとかはとりあえず無視　複数ウォレットもとりあえず無視
        for w in self.walletList:
            if w['owner'] == taker:
                takerWallet = w
            if w['owner'] == maker:
                makerWallet = w
        #もしウォレットなかったら終わり
        if takerWallet is None:
            return 'You have no wallet!'
        if makerWallet is None:
            return 'There is no maker\'s wallet.'
        #送る金持ってなかったり交換する金なかったら終わり
        if takerToken in takerWallet == False:
            return 'You have no sendmoney.'
        if makerToken in makerWallet == False:
            return 'Maker has no changemoney.'
        if takerAmount > takerWallet[takerToken]:
            return 'You don\'t have sufficient changemoney.'
        if makerAmount > makerWallet[makerToken]:
            return 'Maker doesn\'t have sufficient sendmoney.'
        #もし受け取る通貨のウォレットなかったら作らないと とりあえずエラーでいい
        if makerToken in takerWallet == False:
            return 'You don\'t have gettoken wallet'
        if takerToken in makerWallet == False:
            return 'Maker doesn\'t sendtoken wallet'

        takerWallet[makerToken] = takerWallet[makerToken] + makerAmount
        makerWallet[makerToken] = makerWallet[makerToken] - makerAmount

        takerWallet[takerToken] = takerWallet[takerToken] - takerAmount
        makerWallet[takerToken] = makerWallet[takerToken] + takerAmount

        return 'Trade!'
