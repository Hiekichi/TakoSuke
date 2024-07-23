import pyxel

D_NONE  = 0

KEY = [None,pyxel.KEY_DOWN,pyxel.KEY_UP,pyxel.KEY_RIGHT,pyxel.KEY_LEFT]
D =   [[0,0],  [0.5,1],[-0.5,-1],[1,0],[-1,0]]
GPAD = [None,
        pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,
        pyxel.GAMEPAD1_BUTTON_DPAD_UP,
        pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,
        pyxel.GAMEPAD1_BUTTON_DPAD_LEFT]
LAXIS = [None,
         pyxel.GAMEPAD1_AXIS_LEFTY,pyxel.GAMEPAD1_AXIS_LEFTY,
         pyxel.GAMEPAD1_AXIS_LEFTX,pyxel.GAMEPAD1_AXIS_LEFTX]
LAXIS_RANGE = [None,[20000,36000],[-36000,-20000],[20000,36000],[-36000,-20000]]

START_STAGE=0

frame_x = 0
stage_w = 2048
FRAME_W = 120
FRAME_H = 120
FRAME_LIMIT = 88

wspeed = 2

tarus = [ [], [], [], [], [] ]

class MyChar():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.is_run = False
        self.jump_cnt = 0
        self.flash_cnt = 0
        self.tumble_cnt = 0
        self.slow_cnt = 0
    def update(self):
        if self.tumble_cnt > 0:
            pass
        elif self.is_run:
            self.x += wspeed
    def draw(self):
        # ジャンプ中
        if self.jump_cnt > 24:
            pyxel.blt(self.x-frame_x,self.y+3, 0, 16+(2-(self.jump_cnt-24)//8)*16,48, 16,16, 7)
            pyxel.blt(self.x-frame_x,self.y-48+self.jump_cnt, 0, 0,48, 16,16, 7)
        elif self.jump_cnt > 0:
            pyxel.blt(self.x-frame_x,self.y+3, 0, 16+self.jump_cnt//8*16,48, 16,16, 7)
            pyxel.blt(self.x-frame_x,self.y-self.jump_cnt, 0, 0,48, 16,16, 7)
        # 転倒中
        elif self.tumble_cnt > 0:
            if pyxel.frame_count//4%2==0:
                pyxel.blt(self.x-frame_x,self.y+3, 0, 16,16, 16,16, 7)
                pyxel.blt(self.x-frame_x,self.y, 0, 0,64, 16,16, 7)
        # 走り中
        elif self.is_run:
            if self.flash_cnt==0 or pyxel.frame_count%2==0:
                pyxel.blt(self.x-frame_x,self.y+3, 0, 16,16, 16,16, 7)
                pyxel.blt(self.x-frame_x,self.y, 0, pyxel.frame_count//8%4*16,32, 16,16, 7)
        # 開始待ち中
        else:
            pyxel.blt(self.x-frame_x,self.y+3, 0, 16,16, 16,16, 7)
            pyxel.blt(self.x-frame_x,self.y, 0, 0,16, 16,16, 7)
myChar = MyChar(12,59)

class Taru():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.is_alive= True
    def update(self):
        self.x -= 0.5
        if self.x - frame_x < -16:
            self.is_alive = False
    def draw(self):
        pyxel.blt(self.x-frame_x,self.y, 0, 80+(4000-self.x)//2%8*10,16, 10,12, 7)




class App():
    def __init__(self):
        pyxel.init(120,120,title="MetroX",fps=48)
        pyxel.load("runner.pyxres")
        self.init_game()
        pyxel.run(self.update,self.draw)

    def init_game(self):
        self.stage_num = 0
        self.init_stage()

    def init_stage(self):
        global tarus
        self.stage_num += 1
        self.cnt = 0
        self.gamestart_cnt = 144
        tarus = [
             [Taru(200,60),Taru(420,60),Taru(500,60),Taru(800,60),Taru(1200,60),Taru(1400,60)],
             [Taru(204,68),             Taru(504,68),Taru(804,68),Taru(1234,68),Taru(1404,68)],
             [             Taru(428,76),Taru(508,76),Taru(808,76),Taru(1268,76),Taru(1408,76)],
             [Taru(212,84),             Taru(512,84)             ,Taru(1242,84),Taru(1412,84)],
             [Taru(216,92),                          Taru(816,92),Taru(1216,92),Taru(1416,92)]
        ]

    def update(self):
        global frame_x,stage_w,tarus,wspeed
        ### ステージごとのカウンター
        self.cnt += 1
        ### 床に沿って移動速度を変更
        if myChar.jump_cnt == 0:
            tile = pyxel.tilemaps[0].pget((myChar.x+12)//8,(myChar.y+16)//8)
            if 21<=tile[1]<=22:
                myChar.slow_cnt = 48
                wspeed = 1
        if myChar.slow_cnt > 0:
            myChar.slow_cnt -= 1
            if myChar.slow_cnt == 0:
                wspeed = 2
        ### マイキャラのイベント処理
        # ゲーム開始カウントダウン
        if self.gamestart_cnt > 0:
            self.gamestart_cnt -= 1
            if self.gamestart_cnt == 0:
                myChar.is_run = True
            return
        # 無敵状態（かな？）のカウントダウン
        if myChar.flash_cnt > 0:
            myChar.flash_cnt -= 1
        # 転んでる最中はプレイヤーが何もできない
        if myChar.tumble_cnt > 0:
            myChar.tumble_cnt -= 1
            #myChar.x += 1
        # ジャンプ中はプレイヤーが何もできない
        elif myChar.jump_cnt > 0:
            myChar.jump_cnt -= 1
            #myChar.x += 1
        # ジャンプ
        elif pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.KEY_SPACE):
            myChar.jump_cnt = 48
        # 移動用キー入力の判定
        else:
            for i in range(1,3):
                if pyxel.btn(KEY[i]) or (LAXIS_RANGE[i][0] < pyxel.btnv(LAXIS[i]) < LAXIS_RANGE[i][1]) or pyxel.btn(GPAD[i]):
                    myChar.y += D[i][1]
                    myChar.y = max(min(83,myChar.y), 51)
                    if 51 < myChar.y < 83:
                        myChar.x += D[i][0]

        ### マイキャラの更新
        myChar.update()

        # キャラ移動に沿った背景スクロール処理
        if myChar.x-frame_x > FRAME_W - FRAME_LIMIT and frame_x != stage_w - FRAME_W:
            frame_x += wspeed
            if frame_x > stage_w - FRAME_W:
                frame_x = stage_w - FRAME_W
        # ステージ両端における移動可能範囲の処理
        myChar.x = max(min(stage_w - 16,myChar.x), 0)

        ### 樽の更新
        for tarurec in tarus:
            for taru in reversed(tarurec):
                taru.update()
                if not taru.is_alive:
                    tarurec.remove(taru)
        
        ### 当たり判定
        if myChar.jump_cnt == 0:
            lane = (myChar.y-46)//8 #どのレーンを走ってるか？
            # 樽
            for taru in tarus[lane]:
                if abs((taru.x-5)-(myChar.x-8)) < 10:
                    #myChar.flash_cnt = 48
                    myChar.tumble_cnt = 36

    def draw(self):
        ### 背景描画
        pyxel.cls(0)
        #pyxel.bltm(0,0, 0, frame_x,128*8, FRAME_W,FRAME_H)
        pyxel.bltm(0,0, 0, frame_x,0, FRAME_W,FRAME_H)
        #pyxel.blt(10,10, 2, 0,0, 100,44, 8)

        ### 樽の描画
        for i in range(5):
            for taru in tarus[i]:
                taru.draw()
        ### マイキャラの描画
        myChar.draw()

        if self.gamestart_cnt > 0:
            pyxel.text(50,20, "READY\n\n  {}".format(self.gamestart_cnt//48+1),8)

        ###### デバッグ用 ###########################
        #pyxel.text(10,10, "frame_x:{}".format(frame_x),7)
        pyxel.text(10,10, "TILE: {}".format(pyxel.tilemaps[0].pget((myChar.x+12)//8,(myChar.y+16)//8)),7)
        pyxel.text(10,20, "x:  {}".format((myChar.x+12)//8),7)
        pyxel.text(10,30, "y:  {}".format((myChar.y+16)//8),7)
        #pyxel.text(10,20, "myChar.x:{}".format(myChar.x),7)
        #pyxel.text(70,20, "myChar.x-frame_x:\n{}".format(myChar.x-frame_x),7)
        #pyxel.text(10,30, "myChar.y:{}".format(myChar.y),7)
        #pyxel.text(10,30, "myChar.tumble_cnt:{}".format(myChar.tumble_cnt),7)
        #pyxel.text(10,40, "Lane:{}".format((myChar.y-46)//8),7)
        #pyxel.text(10,50, "myChar.jump_cnt:{}".format(myChar.jump_cnt),7)

App()

