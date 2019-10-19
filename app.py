# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os

from flask import Flask
from flask import request
from flask import make_response, jsonify

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    print(req.get("action"))
    if req.get("action") == "check-katawaku":
        params = req.get("parameters")
        res = makeWebhookResult(params)
    else:
        res = {}

    return res


def makeWebhookResult(params):
    speech = "普通コンクリート、せき板：合板，W5/16(2分5厘)，縦端太・横端太：単管パイプ(φ48.6)、許容たわみ量3mmとして、壁型枠チェックします。")
                
    # 条件読み込み
    H = params.get("unit-length")  # 壁高
    T = params.get("unit-length1")    # 壁厚
    L0 = params.get("unit-length2")    # 壁長さ
    S = params.get("unit-speed")    # 打込み速さ
    w0 = 2.3*9.81/1000    # コンクリート単位体積重量

    Ls = params1.get("unit-length3")     # セパレーター間隔
    Lt = params1.get("unit-length4")     # 縦端太間隔
    Ly = params1.get("unit-length5")    # 横端太間隔
    
    
    if H > 4.0:
        speech += "打込み高さ4m以上は打設できません。再計画してください。"
     else:
      if S < 10:
        if H > 1.5:
         P = w0 * H
        elif H < 1.5:
           if L0 < 3.0:
              P = 1.5 * w0 + 0.2 * w0 * (H - 1.5)
           elif L0 > 3.0:
              P = 1.5 * w0
       elif S < 20:
         if H < 2.0:
            P = w0 * H
         elif H > 2.0:
           if L0 <= 3.0:
              P = 2.0 * w0 + 0.4 * w0 * (H - 2.0)
           elif L0 > 3.0:
              P = 2.0 * w0
       else:
         P = w * H
        
    speech = "下記条件で計算します。"\
             "高さ:{}m\n".format(H) + \
             "厚さ:{}m\n".format(T) + \
             "長さ:{}m\n".format(L0) + \
             "打込み速さ:{}m/s\n".format(S) + \
             "配置間隔"\
             "　セパレーター間隔:{}mm\n".format(Ls) + \
             "　縦端太間隔:{}mm\n".format(Lt) + \
             "　横端太間隔:{}mm\n".format(Ly) + \
             "コンクリート単位体積重量:2.3tf/立米" + \
             "側圧:{}kN/平米".format(P) )

    return speech

  # 条件
    # せき板
    E = 5600    # ヤング率Ｎ/mm2
    I = 1440    # 断面二次モーメントmm4
    z = 240    # 断面係数mm3
    fb = 14    # 許容曲げ応力Ｎ/mm2
    Bmax = 3    # 許容たわみ量mm

    # セパレーター
    Ft=13720    # 許容引張力N/本
    
    # 縦端太横端太
    zt = 3830    # 断面係数mm3(縦端太)
    zy = 3830*2    # 断面係数mm3(横端太)
    fbt = 240   # 許容曲げ応力Ｎ/mm2
    It = 93200    # 断面二次モーメントmm4
    Et = 210000    # ヤング率Ｎ/mm2


def makeWebhookResult_mm(params):
    # せき板
    w = P * 10    # 荷重N/mm
    M = 1/8 * w * Lt * Lt    # 曲げモーメント
    A = M/z    # 曲げ応力
    B = 5 * w * Lt * Lt * Lt * Lt / (384 * E * I)    # たわみ

    # セパレーター
    A1 = Ls * Ly　    # 負担面積
    T = P * A1    # 引張力

    # 縦端太
    wt = P * Lt    # 荷重N/mm
    Mt = wt * Ly * Ly / 8    # 曲げモーメント
    At = Mt / zt    # 曲げ応力
    Bt = 5 * wt * Ly * Ly * Ly * Ly / (384 * Et * It)    # たわみ

    # 横端太
    wy = P * Ly    # 荷重N/mm
    My = wy * Ls * Ls / 8    # 曲げモーメント
    Ay = My / zy    # 曲げ応力
    By = 5 * wy * Ls * Ls * Ls * Ls / (384 * Et * It * 2)    # たわみ
    
    return A , B , T , At , Bt ,  Ay ,  By


def return_pattern(check_list, fall):
    speech = ""
    later_flag = False

    # せき板
    if A < fb:
        speech += "せき板の曲げはOKです。"
    else:
        speech += "せき板の曲げはNGです。再計画してください。"
        later_flag = True

    if B < Bmax:
        speech += "せき板のたわみはOKです。"
    else:
        speech += "せき板のたわみはNGです。再計画してください。"
        later_flag = True       

    # セパレーター
    if T < Ft:
        speech += "セパレーターの引張はOKです。"
    else:
        speech += "セパレーターの引張はNGです。再計画してください。"
        later_flag = True

    # 縦端太
    if At < fbt:
        speech += "縦端太の曲げはOKです。"
    else:
        speech += "縦端太の曲げはNGです。再計画してください。"
        later_flag = True

    if Bt < Bmax:
        speech += "縦端太のたわみはOKです。"
    else:
        speech += "縦端太のたわみはNGです。再計画してください。"
        later_flag = True

    # 横端太
    if Ay < fbt:
        speech += "横端太の曲げはOKです。"
    else:
        speech += "横端太の曲げはNGです。再計画してください。"
        later_flag = True

    if By < Bmax:
        speech += "横端太のたわみはOKです。"
    else:
        speech += "横端太のたわみはNGです。再計画してください。"
        later_flag = True
   
    return speech

if __name__ == '__main__':
    app.run(debug=False)