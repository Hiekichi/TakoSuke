import pyxel

D_NONE  = 0
D_DOWN  = 1
D_UP    = 2
D_RIGHT = 3
D_LEFT  = 4
KEY = [None,pyxel.KEY_DOWN,pyxel.KEY_UP,pyxel.KEY_RIGHT,pyxel.KEY_LEFT]
D =   [[0,0],  [0,1],[0,-1],[1,0],[-1,0]]
GPAD = [None,
        pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,
        pyxel.GAMEPAD1_BUTTON_DPAD_UP,
        pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,
        pyxel.GAMEPAD1_BUTTON_DPAD_LEFT]
LAXIS = [None,
         pyxel.GAMEPAD1_AXIS_LEFTY,pyxel.GAMEPAD1_AXIS_LEFTY,
         pyxel.GAMEPAD1_AXIS_LEFTX,pyxel.GAMEPAD1_AXIS_LEFTX]
LAXIS_RANGE = [None,[20000,36000],[-36000,-20000],[20000,36000],[-36000,-20000]]
POST = [None,0,0,1,-1]

START_STAGE=0

frame_x = 0
stage_w = 512
FRAME_W = 120
FRAME_H = 120
FRAME_LIMIT = 60

enemies = []

class MyChar():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.dir = 4  # 0:下 1:上  2:右  3:左  4:静止状態
        self.post = 1 # 1:右向きジャンプ -1:左向きジャンプ
        self.is_alive = True
        self.kick_cnt = 0
        self.punch_cnt = 0
    def update(self):
        pass
    def draw(self):
        if self.kick_cnt > 0:
            pyxel.blt(self.x-frame_x,self.y, 0, 0,64, 16*self.post,16, 0)
            return
        if self.punch_cnt > 0:
            pyxel.blt(self.x-frame_x,self.y, 0, 0,144, 16*self.post,16, 0)
            return

        if self.dir == D_NONE:
            pyxel.blt(self.x-frame_x,self.y, 0, 0,112, 16*self.post,16, 0)
        else:
            pyxel.blt(self.x-frame_x,self.y, 0, pyxel.frame_count//8%4*16,128, 16*self.post,16, 0)
myChar = MyChar(16,96)


class Enemy():
    def __init__(self,x,y,type) -> None:
        self.x = x
        self.y = y
        self.type = type
        self.post = -1
        self.wp = [64, 0, 0, 0]
    def update(self):
        global myChar
        if myChar.x < self.x:
            self.post = -1
        else:
            self.post = 1
    def draw(self):
            pyxel.blt(self.x-frame_x,self.y, 0, self.wp[self.type]+pyxel.frame_count//8%4*16,128, 16*self.post,16, 0)




class App():
    def __init__(self):
        pyxel.init(120,120,title="TAKOSUKE",fps=48)
        pyxel.load("ane.pyxres")
        self.init_game()
        pyxel.run(self.update,self.draw)

    def init_game(self):
        self.stage_num = 0
        self.init_stage()

    def init_stage(self):
        global enemies
        self.stage_num += 1
        self.cnt = 0
        enemies = [
            Enemy(100,96,0),
            Enemy(120,88,0)
        ]

    def update(self):
        global frame_x,stage_w
        ### ステージごとのカウンター
        self.cnt += 1
        ### マイキャラのイベント処理
        # キック中はプレイヤーが何もできない
        if myChar.kick_cnt > 0:
            myChar.kick_cnt -= 1
        # パンチ中はプレイヤーが何もできない
        elif myChar.punch_cnt > 0:
            myChar.punch_cnt -= 1
        # キック
        elif pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            myChar.kick_cnt = 18
        # パンチ
        elif pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            myChar.punch_cnt = 9
        # 移動用キー入力の判定
        else:
            myChar.dir = D_NONE
            for i in range(1,5):
                if pyxel.btnp(KEY[i]) or (LAXIS_RANGE[i][0] < pyxel.btnv(LAXIS[i]) < LAXIS_RANGE[i][1]) or pyxel.btn(GPAD[i]):
                    myChar.x += D[i][0]
                    myChar.y += D[i][1]
                    myChar.dir = i
                    if POST[i] != 0:
                        myChar.post = POST[i]
            if myChar.x > FRAME_W - FRAME_LIMIT and frame_x != stage_w - FRAME_W:
                frame_x += D[myChar.dir][0]
                if frame_x > stage_w - FRAME_W:
                    frame_x = stage_w - FRAME_W
            if (myChar.x - frame_x) < FRAME_LIMIT and frame_x != 0:
                frame_x += D[myChar.dir][0]
                if frame_x < 0:
                    frame_x = 0
            myChar.x = max(min(stage_w - 16,myChar.x), 0)
            myChar.y = max(min(100,myChar.y), 80)

        ### マイキャラの更新
        myChar.update()
        ### 敵キャラの更新
        for ene in reversed(enemies):
            ene.update()

    def draw(self):
        ### 背景描画
        pyxel.cls(0)
        pyxel.bltm(0,0, 0, frame_x,0, FRAME_W,FRAME_H, 0)
        pyxel.blt(10,10, 2, 0,0, 100,44, 8)

        ### 敵キャラの描画
        for ene in enemies:
            ene.draw()
        ### マイキャラの描画
        myChar.draw()


        ###### デバッグ用 ###########################
        #pyxel.text(10,10, "frame_x:{}".format(frame_x),7)
        #pyxel.text(10,20, "myChar.x:{}".format(myChar.x),7)
        #pyxel.text(10,30, "myChar.y:{}".format(myChar.y),7)
        #pyxel.text(10,40, "myChar.post:{}".format(myChar.post),7)
        #pyxel.text(10,50, "myChar.kick_cnt:{}".format(myChar.kick_cnt),7)

App()

