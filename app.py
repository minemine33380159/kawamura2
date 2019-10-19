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
    speech = "���ʃR���N���[�g�A�����F���CW5/16(2��5��)�C�c�[���E���[���F�P�ǃp�C�v(��48.6)�A���e����ݗ�3mm�Ƃ��āA�ǌ^�g�`�F�b�N���܂��B")
                
    # �����ǂݍ���
    H = params.get("unit-length")  # �Ǎ�
    T = params.get("unit-length1")    # �ǌ�
    L0 = params.get("unit-length2")    # �ǒ���
    S = params.get("unit-speed")    # �ō��ݑ���
    w0 = 2.3*9.81/1000    # �R���N���[�g�P�ʑ̐Ϗd��

    Ls = params1.get("unit-length3")     # �Z�p���[�^�[�Ԋu
    Lt = params1.get("unit-length4")     # �c�[���Ԋu
    Ly = params1.get("unit-length5")    # ���[���Ԋu
    
    
    if H > 4.0:
        speech += "�ō��ݍ���4m�ȏ�͑Ő݂ł��܂���B�Čv�悵�Ă��������B"
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
        
    speech = "���L�����Ōv�Z���܂��B"\
             "����:{}m\n".format(H) + \
             "����:{}m\n".format(T) + \
             "����:{}m\n".format(L0) + \
             "�ō��ݑ���:{}m/s\n".format(S) + \
             "�z�u�Ԋu"\
             "�@�Z�p���[�^�[�Ԋu:{}mm\n".format(Ls) + \
             "�@�c�[���Ԋu:{}mm\n".format(Lt) + \
             "�@���[���Ԋu:{}mm\n".format(Ly) + \
             "�R���N���[�g�P�ʑ̐Ϗd��:2.3tf/����" + \
             "����:{}kN/����".format(P) )

    return speech

  # ����
    # ������
    E = 5600    # �����O���m/mm2
    I = 1440    # �f�ʓ񎟃��[�����gmm4
    z = 240    # �f�ʌW��mm3
    fb = 14    # ���e�Ȃ����͂m/mm2
    Bmax = 3    # ���e����ݗ�mm

    # �Z�p���[�^�[
    Ft=13720    # ���e������N/�{
    
    # �c�[�����[��
    zt = 3830    # �f�ʌW��mm3(�c�[��)
    zy = 3830*2    # �f�ʌW��mm3(���[��)
    fbt = 240   # ���e�Ȃ����͂m/mm2
    It = 93200    # �f�ʓ񎟃��[�����gmm4
    Et = 210000    # �����O���m/mm2


def makeWebhookResult_mm(params):
    # ������
    w = P * 10    # �׏dN/mm
    M = 1/8 * w * Lt * Lt    # �Ȃ����[�����g
    A = M/z    # �Ȃ�����
    B = 5 * w * Lt * Lt * Lt * Lt / (384 * E * I)    # �����

    # �Z�p���[�^�[
    A1 = Ls * Ly�@    # ���S�ʐ�
    T = P * A1    # ������

    # �c�[��
    wt = P * Lt    # �׏dN/mm
    Mt = wt * Ly * Ly / 8    # �Ȃ����[�����g
    At = Mt / zt    # �Ȃ�����
    Bt = 5 * wt * Ly * Ly * Ly * Ly / (384 * Et * It)    # �����

    # ���[��
    wy = P * Ly    # �׏dN/mm
    My = wy * Ls * Ls / 8    # �Ȃ����[�����g
    Ay = My / zy    # �Ȃ�����
    By = 5 * wy * Ls * Ls * Ls * Ls / (384 * Et * It * 2)    # �����
    
    return A , B , T , At , Bt ,  Ay ,  By


def return_pattern(check_list, fall):
    speech = ""
    later_flag = False

    # ������
    if A < fb:
        speech += "�����̋Ȃ���OK�ł��B"
    else:
        speech += "�����̋Ȃ���NG�ł��B�Čv�悵�Ă��������B"
        later_flag = True

    if B < Bmax:
        speech += "�����̂���݂�OK�ł��B"
    else:
        speech += "�����̂���݂�NG�ł��B�Čv�悵�Ă��������B"
        later_flag = True       

    # �Z�p���[�^�[
    if T < Ft:
        speech += "�Z�p���[�^�[�̈�����OK�ł��B"
    else:
        speech += "�Z�p���[�^�[�̈�����NG�ł��B�Čv�悵�Ă��������B"
        later_flag = True

    # �c�[��
    if At < fbt:
        speech += "�c�[���̋Ȃ���OK�ł��B"
    else:
        speech += "�c�[���̋Ȃ���NG�ł��B�Čv�悵�Ă��������B"
        later_flag = True

    if Bt < Bmax:
        speech += "�c�[���̂���݂�OK�ł��B"
    else:
        speech += "�c�[���̂���݂�NG�ł��B�Čv�悵�Ă��������B"
        later_flag = True

    # ���[��
    if Ay < fbt:
        speech += "���[���̋Ȃ���OK�ł��B"
    else:
        speech += "���[���̋Ȃ���NG�ł��B�Čv�悵�Ă��������B"
        later_flag = True

    if By < Bmax:
        speech += "���[���̂���݂�OK�ł��B"
    else:
        speech += "���[���̂���݂�NG�ł��B�Čv�悵�Ă��������B"
        later_flag = True
   
    return speech

if __name__ == '__main__':
    app.run(debug=False)