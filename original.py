#!/usr/bin/env python3
import MeCab
mecab = MeCab.Tagger()

# si = ['시', 'EP']
si = ['시', 'EP', '*'] # TODO: last *

replace = {
    "hae": {
        "Inflect": {
            # 해요체
            "해요/XSV+EF": ["해", "XSV+EF"],
            "해요/VV+EF": ["해", "VV+EF"],
            "해요/XSV+EC": ["해", "XSV+EC"],
            "해요/VV+EC": ["해", "VV+EC"],
            "지요/VCP+EF": ["지", "VCP+EF"],
            "예요/VCP+EF": ["야", "VCP+EF"],
            "네요/VCP+EF": ["네", "VCP+EF"],
            "세요/EP+EF": ["어", "EF"],
            "군요/VCP+EF": ["군", "VCP+EF"],
            "한대요/VX+EF": ["한대", "VX+EF"],
            "그래요/VV+EF": ["그래", "VV+EF"],
            "그래요/VA+EC": ["그래", "VA+EC"],
            # ㅂ니다체
            "합니다/XSV+EF": ["해", "XSV+EF"],
            "합니다/XSA+EF": ["해", "XSA+EF"],
            "합니다/VV+EF": ["해", "VV+EF"],
            "합니다/VX+EF": ["해", "VX+EF"],
            "합니다만/VX+EF": ["하는데", "VX+EF"],
            "입니다/VCP+EF": ["이다", "VCP+EF"],
            "됩니다/XSV+EF": ["돼", "XSV+EF"],
            "겁니다/NNB+VCP+EF": ["거야", "NNB+VCP+EF"],
            
            "십시오/EP+EF": ["어", "EF"],
            
            "으신/EP+ETM": ["은", "ETM"],
            "저/NP": ["나", "NP"]
        },
        "어요/EF": ["어", "EF"],
        "ㅓ요/EF": ["어", "EF"],
        "아요/EF": ["아", "EF"],
        "ㅏ요/EF": ["아", "EF"],
        "지요/EF": ["지", "EF"],
        "죠/EF": ["지", "EF"],
        "에요/EF": ["야", "EF"],
        "군요/EF": ["군", "EF"],
        "네요/EF": ["네", "EF"],
        "더군요/EF": ["더군", "EF"],
        "요/EF": ["", ""],
        "요/JX": ["야", 'EF'],
        "ᆫ대요/EF": ["ㄴ대", "EF"],
        "는지요/EF": ["는지", "EF"],
        "거든요/EF": ["거든", "EF"],
        "다지요/EF": ["다지", "EF"],
        "ᆫ대요/EC": ["ㄴ대", "EC"],
        "는데요/EF": ["는데", "EF"],
        "ᆯ까요/EF": ["ㄹ까", "EF"],
        # EF 끝이 요로 끝나면 제거.

        "습니다/EF": ["다", "EF"],
        # 입니다/EF": ["이다", "EF"], # 앞 음절의 받침여부 따져서 다-이다 분화
        "ᄇ니다/EF": ["ㄴ다", "EF"],
        "ㅂ니다/EF": ["ㄴ다", "EF"],
        "ᄇ시다/EF": ["자", "EF"],
        "답니다/EF": ["단다", "EF"],
        "ᆫ답니다/EF": ["ㄴ단다", "EF"],
        "는답니다/EF": ["는단다", "EF"],

        "ᄇ시오/EF": ["어", "EF"],

        "드리/VX": ["주", "VX"],
        # 계시/VX": ["있", "VX"], 계신다, 계십니다 등 처리리
        "제/NP": ["내", "NP"],
        "저희/NP": ["우리", "NP"]
    }
}
# 요로 끝나는 EF는 코드로 처리 가능.

shorten = {
    "vowel": {
        "ㅗ+ㅏ": "ㅘ",
        "ㅜ+ㅓ": "ㅝ",
        "ㅣ+ㅓ": "ㅕ"
    },
    "하/VV+아/EF": "해",
    "하/VV+었/EP": "했",
    "하/VV+어/EF": "해",
    "하/VX+아/EF": "해",
    "하/VX+어/EF": "해",
    "주/VX+어/EF": "줘",
    "보/VX+어/EF": "봐",
    "지/VX+어/EF": "져",
    "하/VV+ㄴ대/EF": "한대",
    "하/XSV+아/EF": "해",
    "하/XSV+어/EF": "해",
    "하/XSA+아/EF": "해",
    "하/XSA+어/EF": "해",
    "되/VV+어/EF": "돼",
    "되/XSV+어/EF": "돼"
}

def parse(string): # mecab 형태소 분석
    ret = []
    for line in mecab.parse(string).split(sep='\n'):
        line = line.split()
        if line[0]=="EOS":
            break
        tmp = [line[0]]
        tmp.extend(line[1].split(','))
        ret.append(tmp)
    return ret

def plains(parsed): # 형태소 배열에서 표현형만 남겨 배열로 전환
    return [i[0] for i in parsed]

def isInflect(morpheme): # 활용형인지 검사
    return morpheme[5]=="Inflect"

def breakInflect(inflect): # 활용형 해체
    uncombined = inflect[8].split(sep='+')
    results = []
    for m in uncombined:
        results.append(m.split(sep='/'))
    return results

# STringifY MORpheme. 표현형/품사 꼴로 반환
def styMor(mor):
    return mor[0] + '/' + mor[1]

# 표현형과 품사를 정의된 패턴 목록에서 비교
def isSame(mor, lib):
    return lib.get(styMor(mor))!=None

# 형태소의 표현형만 붙여서 반환
def assembly(morphemes):
    string = ""
    for m in morphemes:
        string += m[0]
    return string

# '표현형/품사' 꼴로 만들고 +로 붙여 반환
def normalizeMorphemes(mor):
    string = []
    for m in mor:
        string.append(styMor(m))
    return '+'.join(string)


Chos = [ "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ" ]
Jungs = [ "ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ" ]
Jongs = [ "", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ" ]

def jaso(hangul): # 자소 분해
    code = ord(hangul) - 0xAC00
    jong = code%28
    jung = ((code-jong)//28)%21
    cho = (((code-jong)//28)-jung)//21
    return Chos[cho], Jungs[jung], Jongs[jong]

def glue(cho, jung, jong): # 자소 합체
    return chr(0xAC00 + ((Chos.index(cho)*21)+Jungs.index(jung))*28+Jongs.index(jong))


def haeche(original: str):
    _input = original
    # _input = input()
    output = _input

    parsed = parse(_input)
    originlen = 0
    originpos = 0
    extra = 0
    positions = []
    lastpos = 0

    for i in range(len(parsed)):
        # 원본 문장에서 각 형태소의 위치 저장
        positions.append(lastpos := _input.index(parsed[i][0], lastpos))

        originlen = len(parsed[i][0])
        originpos = positions[i] + extra

        # 활용형의 분리
        bricks = False # 활용형을 분해했을 때는 배열로 사용됨.
        if isInflect(parsed[i]): #  활용형 여부
            newstr = "" # 새로 교체된 문자열
            newmor = "" # 새로 교체된 형태소
            flag = False # 교체되었는지 여부를 나타내는 플래그 변수
            
            #  조건 검사
            if isSame(parsed[i], replace["hae"]["Inflect"]): # 활용형 자체가 사전에 정의되었나
                newstr = replace["hae"]["Inflect"][styMor(parsed[i])][0]
                newmor = replace["hae"]["Inflect"][styMor(parsed[i])]
                flag = True # 교체됨
            else: # 정의되지 않았다면 활용형을 분해해서 각 형태소를 조건 검사
                bricks = breakInflect(parsed[i])
                for b in range(len(bricks)):
                    if str(bricks[b]) == str(si): # TODO: what about last *?
                        # bricks = bricks.splice(b-1, 1) #  선어말어미 -시-의 삭제
                        del bricks[b] # TODO why b-1?
                    if isSame(bricks[b], replace["hae"]): #  분해된 각 형태소를 사전 정의된 패턴으로 검사
                        bricks[b] = replace["hae"][styMor(bricks[b])]
                        flag = True #  교체 가능

            #  음운 축약
            if flag: #  교체가 일어났을 때
                if bricks: #  활용형을 분해했을 때
                    if shorten.get(normalizeMorphemes(bricks)): #  정규화된 형태소 조각들의 축약 패턴이 정의되어 있다면
                        newstr = shorten[normalizeMorphemes(bricks)] #  축약된 형태로 교체
                    # TODO: this is never True, unshift returns int. I'll comment it out for now
                    # elif len(bricks) == 1 and shorten[normalizeMorphemes(bricks.unshift(parsed[i-1]))]: #  앞 형태소를 합쳐서 보기
                    #     if shorten.get( normalizeMorphemes([parsed[i-1], newmor ]) ): #  앞 형태소를 합쳐서 보기
                    #         newstr = shorten[ normalizeMorphemes([parsed[i-1], newmor ]) ] # TODO: newmor is not defined
                    #         originpos -= parsed[i-1][0].length
                    #         originlen += parsed[i-1][0].length
                    #     else: print([parsed[i-1], newmor])
                    else: #  분해, 치환되었지만 축약이 정의되지 않은 상태 : 특수 조건들
                        shortflag = False #  축약 여부 플래그 변수
                        print(bricks)
                        apjaso = jaso(bricks[0][0].slice(-1)) #  동사 어간의 마지막 음절을 자소 분해
                        if(apjaso[2] == '' and bricks[1][1][0] == 'E'): #  동사 어간 마지막 음절의 받침이 없고 어미가 뒤에 붙음
                            #  ㄴ다, ㅂ니다 등 축약
                            if(Jongs.index(bricks[1][0][0]) != -1): #  어미 첫자가 그냥 자음일 때
                                newstr = bricks[0][0].slice(0, -1) + glue(apjaso[0], apjaso[1], bricks[1][0][0]) + bricks[1][0][1:]
                                shortflag = True
                            elif(bricks[0][1][0] == 'V'): #  동사 어간이 -2음절- 이상 # /*bricks[0][0].length > 1 && */
                                #  모음 축약 : 어간 마지막 음절에 받침이 없고 어미가 모음으로 시작하면 모음축약
                                ejaso = jaso(bricks[1][0][0]) #  어미 첫자의 자소 분해
                                if(ejaso[0] == 'ㅇ'): #  어미가 모음으로 시작
                                    newvowel = shorten["vowel"][apjaso[1]+'+'+ejaso[1]] #  새로 축약된 모음
                                    if(newvowel):
                                        newstr = bricks[0][0].slice(0, -1) + glue(apjaso[0], newvowel, ejaso[2]) + bricks[1][0][1:] #  새 이중모음을 넣어 교체
                                        shortflag = True

                        if(not shortflag): newstr = assembly(bricks) #  어떤 경우에도 해당되지 않으면 그냥 강제로 붙임. (예외)
                else:
                    #  활용형을 분해하지 않았음
                    if (shorten[ normalizeMorphemes([parsed[i-1], newmor ]) ] ): #  앞 형태소를 합쳐서 보기
                        newstr = shorten[ normalizeMorphemes([parsed[i-1], newmor ]) ]
                        originpos -= len(parsed[i-1][0])
                        originlen += len(parsed[i-1][0])
                    else: print([parsed[i-1], newmor])

                #  전체 문장에서 바뀐 문자열로 교체함.
                output = output[0:originpos] + newstr + output[originpos + originlen:]
                extra += len(newstr) - originlen
        #  활용형

        #  활용형이 아님
        if(str(parsed[i]) == str(si)): #  선어말어미 -시- 제거
            output = output[0:originpos] + output[originpos+originlen:]
            extra -= originlen
        if(isSame(parsed[i], replace["hae"])): #  해요체 => 해체
            output = output[0:originpos] + replace["hae"][styMor(parsed[i])][0] + output[originpos+originlen:]
            extra += len(replace["hae"][styMor(parsed[i])][0]) - originlen
        #  활용형이 아님

        return output

if __name__=="__main__":
# _input = input("asdf: ")
    _input = "해요체는 말끝에 '-요'를 붙여요. 이뿐이에요. 하지만 친근한 느낌을 주고, 요새 격식이 많이 허물어져서 그런지 사회에서는 사용이 많이 늘어나고 있어요. 특히 구어체에서 주로 사용하죠. 경우에 따라 정중도를 높이기 위해 중간중간 합쇼체를 섞어 쓰기도 해요. 어떤 말이 합쇼체로 바뀌는 지 아시는 분은 추가 부탁드려요. 만화나 애니메이션의 여자들 중 상대 불문하고 존댓말을 사용하는 경우는 대개 해요체를 쓰는데, 해요체도 격식은 없지만 엄연한 존댓말이니 유의하시기 바라요. 왠지 남녀탐구생활이 떠오르는 말투지만 신경쓰지 않도록 해요. 신경쓰면 지는 거예요. 이 문장을 보기전까지는 그냥 평범하게 읽고 있었는데 갑자기 남녀탐구생활 나레이션목소리로 자동재생되는건 그냥 기분 탓이에요.강원도 사투리로 말할 때 '-요'를 붙이기도 한대요.대한민국 국군에서는 상급자에게 해요체를 쓰면 안되고 꼭 다나까체로 써야 한다고 알려져 있어요. 하지만 군대에 해요체가 아예 없다고 하는건 옳지 않아요. 장교가 나이차가 많은 연장자 부사관에게 해요체를 쓰기도 하기 때문이지요. 그리고 병 계급끼리라도 아저씨끼리는 해요체를 써도 돼요. 참고로 요즘 되요라고 많이 쓰는데요, 돼요라고 해야 맞는 거예요. 왜냐하면 돼요는 '되어요'를 축약해서 쓰는거라 그래요. 이 내용에 대해 더 알고 싶거나 헷갈리면 되와 돼의 구분을 참고해 주세요.되요 해도 되요? 안 돼요! 돼요라고 해야 돼요. 사족으로 어떤 회사의 실험실에 있는 터릿이 이 말투를 사용해서 굉장히 귀엽다고 해요. 당연히 영어에선 해요체가 없으니 번역팀의 의도겠지요? 마지막으로 이 문서는 해요체로 작성되어 있다고 해요. 이는 나무 위키의 암묵의 룰이라고 해요. 충분히 알아 볼 수 있으니 굳이 해설을 따로 쓸 필요는 없어요."
    output = haeche(_input)
    print(output)
