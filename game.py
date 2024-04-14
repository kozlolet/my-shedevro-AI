import tkinter as tk
import random
import pprint

f = open('flag', 'w')
f.write('1')
f.close()

class FlappyBirdGame:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Flappy Bird")
            self.canvas = tk.Canvas(self.root, width=400, height=400)
            self.root.geometry("400x400+100+100")
            self.canvas.pack()

            f = open('flag', 'r')
            flag = f.read()
            f.close()

            self.birdCount = 8
            self.birds = {}

            self.heaves = []


            if flag == '1':
                print('\n')
                print('=====  iteration 1  =====')
                print('')
                for i in range(self.birdCount):
                    self.createpopylity()
                self.ii = 1
            else:
                self.next_popyllity()


            self.bird_rip = 1


            self.rip_birds = []

            self.fitness = {}
            self.grade = {}

            self.kids = []

            # for i in range(self.birdCount):
            #     self.createpopylity()

            self.BirdKeys = list(self.birds.keys())

            self.pipe_top = self.canvas.create_rectangle(400, 0, 420, 150, fill="green")
            self.pipe_bottom = self.canvas.create_rectangle(400, 250, 420, 400, fill="green")

            self.score = 0
            self.score_display = self.canvas.create_text(50, 20, text="Score: 0", anchor="nw")

            self.fall_sp = 0

            self.start_timer()

            self.move_pipe()


        def createpopylity(self):

            self.bird = self.canvas.create_rectangle(50, 200, 70, 220, fill="blue")
            self.birds[self.bird] = 1

            self.heave = []  #random.randint(-1000, 1000)
            self.heave.append(random.uniform(-1, 1)) #bird_y
            self.heave.append(random.uniform(-1, 1)) #pire_y
            self.heave.append(random.uniform(-1, 1)) #pire_x

            self.heaves.append(self.heave)

        def jump(self):
            self.canvas.move(self.BirdKeys[self.i], 0, -10)
            self.fall_sp = 0

        def fall(self):
            self.canvas.move(self.BirdKeys[self.i], 0, self.fall_sp)

        def move_pipe(self):
            if not self.root:
                return

            pipe_speed = 5
            self.canvas.move(self.pipe_top, -pipe_speed, 0)
            self.canvas.move(self.pipe_bottom, -pipe_speed, 0)

            pipe_coords = self.canvas.coords(self.pipe_top)
            if pipe_coords[2] < 0:
                self.reset_pipe()
                self.score += 1
                self.canvas.itemconfig(self.score_display, text="Score: " + str(self.score))

            # Обновляем высотную разницу при каждом обновлении позиции трубы
            self.update_height_difference()


            for i in range(self.birdCount):
                self.calbr = i

                if self.birds[self.BirdKeys[self.calbr]] == 0:
                    continue
                # else:
                # if 0 <= self.calbr < len(self.BirdKeys):
                #     print(i)
                if self.is_collision():
                    if self.bird_rip < self.birdCount:
                        # self.rip_birds.append(self.birds[self.calbr])
                        self.canvas.delete(self.BirdKeys[self.calbr])
                        # self.birds.remove(self.birds[self.calbr])
                        self.birds[self.calbr + 1] = 0
                        # print(self.score)
                        self.bird_rip += 1

                        self.fitness[self.BirdKeys[self.calbr]] = self.score

                    elif list(self.birds.values()).count(1) == 1:
                        self.fitness[self.BirdKeys[self.calbr]] = self.score
                        self.game_over()

            self.root.after(50, self.move_pipe)

        def update_height_difference(self):

            for i in range(len(self.BirdKeys)):
                if self.birds[self.BirdKeys[i]] == 0:
                    continue

                # print('birds    ', self.birds)
                # print('i    ', i)
                bird_coords = self.canvas.coords(self.BirdKeys[i])
                pipe_coords = self.canvas.coords(self.pipe_top)
                pire_y = (pipe_coords[3] + 40)

                if bird_coords:

                    bird_y = bird_coords[1]

                    bird_x = bird_coords[0]
                    pire_x = pipe_coords[2]

                    # print(bird_y)

                    self.i = i

                    self.fall_sp += 0.2

                    self.result = (bird_y * self.heaves[i][0]) + (pire_y * self.heaves[i][1]) + (pire_x * self.heaves[i][2])

                    if self.result > 0:
                        self.jump()

                    # self.root.bind("<space>", self.jump)
                    self.fall()

        def is_collision(self):

            # print('count of birds    ', self.birds)
            # print('calbr    ', self.calbr)
            bird_coords = self.canvas.coords(self.BirdKeys[self.calbr])
            pipe_coords = self.canvas.coords(self.pipe_top)

            # print('---------')
            # print('birds   ', self.birds, '      calbr   ', self.calbr)
            # print('bird coords for ', self.calbr, ' bird:   ', bird_coords)

            if bird_coords:

                if bird_coords[0] < pipe_coords[2] and bird_coords[2] > pipe_coords[0]:
                    if bird_coords[1] < pipe_coords[3] or bird_coords[3] > pipe_coords[1] + 250:
                        return True
                elif bird_coords[1] < 0 or bird_coords[3] > 400:
                    return True

                return False

        def reset_pipe(self):
            pipe_height = random.randint(50, 200)
            self.canvas.coords(self.pipe_top, 400, 0, 420, pipe_height)
            self.canvas.coords(self.pipe_bottom, 400, pipe_height + 100, 420, 400)

        def next_popyllity(self):
            self.ii += 1
            print('\n')
            print('=====  iteration', self.ii, '  =====')
            print('')

            for i in range(self.birdCount):
                self.bird = self.canvas.create_rectangle(50, 200, 70, 220, fill="blue")
                self.birds[self.bird] = 1

            print('birds created    ', self.birds)

            # calculate fitness
            for i in range(len(list(self.fitness.values()))):
                values = list(self.fitness.values())
                value = values[i]

                if max(values) - min(values) == 0:
                    self.grade[self.BirdKeys[i]] = 1
                    continue

                cal = ((value - min(values)) / (max(values) - min(values))) * 9 + 1
                self.grade[self.BirdKeys[i]] = cal

            print('grade   ', self.grade)

            # choice parents
            self.parents = []
            while len(self.parents) != 2:
                for i in list(self.grade.keys())[::-1]:
                    if len(self.parents) != 2:
                        if random.randint(0, 10) <= self.grade[i]:
                            parent = list(self.grade.keys())[i - 1]
                            self.parents.append(parent)
                            if len(self.parents) == 2:
                                if self.parents[0] == self.parents[1]:
                                    self.parents.clear()
                    continue
            print('parents', self.parents)

            # greate kids
            self.kids = []
            while len(self.kids) != 8:
                self.child = []
                for i in range(3):
                    if random.randint(0, 1) == 0:
                        self.child.append(self.heaves1[self.parents[0] - 1][i])
                    else:
                        self.child.append(self.heaves1[self.parents[1] - 1][i])
                self.kids.append(self.child)

            print('kids   ', self.kids)

            mutation_rate = 2
            ii = 0
            for i in range(2):
                if random.randint(0, 1) == 0:
                    for i in range(3):
                        self.kids[random.randint(0, 7)][i] += random.uniform(-1, 1)
                else:
                    for i in range(3):
                        self.kids[random.randint(0, 7)][i] -= random.uniform(-1, 1)

            self.heaves = self.kids.copy()

            # self.heaves[0] = [517, -755, -855]



        def game_over(self):

            self.heaves1 = self.heaves.copy()

            f = open('flag', 'w')
            f.write('0')
            f.close()

            self.stop_timer()

            # Сбросить значения переменных и очистить экран
            self.canvas.delete("all")

            # Сбросить значения переменных
            self.birds.clear()
            self.heaves.clear()
            self.rip_birds.clear()
            self.bird_rip = 1
            self.score = 0

            self.root.destroy()

            # Подготовить новую игру
            self.__init__()

        def start_timer(self):
            self.timer_id = self.root.after(20000, self.game_over)  # Timer for 10 seconds

        def stop_timer(self):
            self.root.after_cancel(self.timer_id)


        def run(self):
            self.root.mainloop()


game = FlappyBirdGame()
game.run()